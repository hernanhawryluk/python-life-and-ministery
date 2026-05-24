import os
import sqlite3
import datetime
import shutil
import json
from copy import deepcopy
from src.scheduler.ranking import ASSIGNATION_FIELDS, DEFAULT_RANKING_SETTINGS, FIELD_INDEX, sort_witnesses
from src.scheduler.rules import ASSIGNATION_QUERIES, WITNESS_GROUPS
from src.utils.switchers import assignment_label, meeting_switcher, school_switcher

class DataBase:
    def __init__(self):
        self.table_name = os.path.join("data", "witnesses.db")
        
    def create_database(self):
        os.makedirs("data", exist_ok=True)
        db_connection = sqlite3.connect(self.table_name)
        c = db_connection.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS Witnesses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, 
                phone TEXT, 
                gender TEXT, 
                role TEXT, 
                exclude BOOLEAN, 
                custom BOOLEAN, 
                companion_only BOOLEAN, 
                replacements BOOLEAN, 
                replacements_date DATE DEFAULT NULL,
                initial_pray DATE DEFAULT NULL, 
                ending_pray DATE DEFAULT NULL,
                read_bible DATE DEFAULT NULL, 
                first DATE DEFAULT NULL, 
                revisit DATE DEFAULT NULL, 
                course DATE DEFAULT NULL, 
                explain DATE DEFAULT NULL,
                speech DATE DEFAULT NULL, 
                companion_male DATE DEFAULT NULL, 
                companion_female DATE DEFAULT NULL,
                read_book DATE DEFAULT NULL, 
                treasures DATE DEFAULT NULL, 
                pearls DATE DEFAULT NULL, 
                book DATE DEFAULT NULL, 
                random_1 DATE DEFAULT NULL, 
                random_2 DATE DEFAULT NULL,
                masters DATE DEFAULT NULL,
                presidency DATE DEFAULT NULL, 
                needs DATE DEFAULT NULL,
                last_assignation DATE DEFAULT NULL,
                last_assignment_type TEXT DEFAULT NULL
                )""")
        c.execute("""CREATE TABLE IF NOT EXISTS Meetings(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start DATE UNIQUE,
                week_label TEXT
                )""")
        c.execute("""CREATE TABLE IF NOT EXISTS Assignments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER,
                assignment_type TEXT,
                assignment_label TEXT,
                titular_id INTEGER,
                companion_id INTEGER DEFAULT NULL,
                position INTEGER,
                FOREIGN KEY(meeting_id) REFERENCES Meetings(id),
                FOREIGN KEY(titular_id) REFERENCES Witnesses(id),
                FOREIGN KEY(companion_id) REFERENCES Witnesses(id)
                )""")
        c.execute("""CREATE TABLE IF NOT EXISTS SchedulerSettings(
                key TEXT PRIMARY KEY,
                value TEXT
                )""")
        self._ensure_column(c, "Witnesses", "last_assignment_type", "TEXT DEFAULT NULL")
        self._ensure_default_settings(c)
        self._backfill_last_assignment_type(c)
        self._migrate_log_history(c)
        self._normalize_log_week_starts(c)
        self._rebuild_assignment_cache(c)
        db_connection.commit()
        c.close()
        db_connection.close()


    def _ensure_column(self, cursor, table, column, definition):
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        if column not in columns:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


    def _backfill_last_assignment_type(self, cursor):
        cursor.execute("SELECT * FROM Witnesses WHERE last_assignation IS NOT NULL AND last_assignment_type IS NULL")
        for witness in cursor.fetchall():
            last_assignation = witness[29]
            inferred_assignment = None
            for assignment in ASSIGNATION_FIELDS:
                if witness[FIELD_INDEX[assignment]] == last_assignation:
                    inferred_assignment = assignment
                    break
            if inferred_assignment:
                cursor.execute(
                    "UPDATE Witnesses SET last_assignment_type = ? WHERE id = ?",
                    (inferred_assignment, witness[0])
                )


    def _ensure_default_settings(self, cursor):
        defaults = {
            "avoid_same_last_assignment": "1",
            "rotation_priority": DEFAULT_RANKING_SETTINGS["rotation_priority"],
            "avoid_same_assignment_weeks": str(DEFAULT_RANKING_SETTINGS["avoid_same_assignment_weeks"]),
            "avoid_multiple_assignments_weeks": str(DEFAULT_RANKING_SETTINGS["avoid_multiple_assignments_weeks"]),
            "avoid_frequent_companions": "0",
            "frequent_companion_weeks": "0",
            "avoid_school_participation_weeks": str(DEFAULT_RANKING_SETTINGS["avoid_school_participation_weeks"]),
        }
        for key, value in defaults.items():
            cursor.execute(
                "INSERT OR IGNORE INTO SchedulerSettings (key, value) VALUES (?, ?)",
                (key, value)
            )


    def _read_scheduler_settings(self, cursor):
        return {
            "avoid_same_last_assignment": True,
            "rotation_priority": "last_assignment",
            "avoid_same_assignment_weeks": 5,
            "avoid_multiple_assignments_weeks": 1,
            "avoid_frequent_companions": False,
            "frequent_companion_weeks": 0,
            "avoid_school_participation_weeks": 5,
        }


    def _migrate_log_history(self, cursor):
        if os.path.abspath(self.table_name) != os.path.abspath(os.path.join("data", "witnesses.db")):
            return
        file_path = os.path.join("data", "meetings.log")
        if not os.path.exists(file_path):
            return
        cursor.execute("SELECT COUNT(*) FROM Assignments")
        if cursor.fetchone()[0] > 0:
            return

        self.create_backup("before_log_migration")
        week_label = None
        week_counter = 0
        position = 0
        with open(file_path, "r") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                if line == "-------------------------------":
                    week_label = None
                    position = 0
                    continue
                if line.startswith("Semana"):
                    week_counter += 1
                    week_label = line
                    week_start = (datetime.date(1900, 1, 1) + datetime.timedelta(days=(week_counter - 1) * 7)).isoformat()
                    cursor.execute(
                        "INSERT OR IGNORE INTO Meetings (week_start, week_label) VALUES (?, ?)",
                        (week_start, week_label)
                    )
                    continue
                if week_label and ": " in line:
                    self._migrate_log_assignment(cursor, week_label, line, position)
                    position += 1


    def _migrate_log_assignment(self, cursor, week_label, line, position):
        assignment_text, names_text = line.split(": ", 1)
        names = names_text.split(" - ", 1)
        titular = names[0].strip()
        companion = names[1].strip() if len(names) == 2 else ""
        if not titular:
            return

        try:
            assignment = school_switcher(assignment_text)
        except KeyError:
            try:
                assignment = meeting_switcher(assignment_text)
            except KeyError:
                return

        cursor.execute("SELECT id FROM Meetings WHERE week_label = ?", (week_label,))
        meeting_row = cursor.fetchone()
        cursor.execute("SELECT id FROM Witnesses WHERE name = ?", (titular,))
        titular_row = cursor.fetchone()
        if not meeting_row or not titular_row:
            return
        companion_id = None
        if companion:
            cursor.execute("SELECT id FROM Witnesses WHERE name = ?", (companion,))
            companion_row = cursor.fetchone()
            companion_id = companion_row[0] if companion_row else None
        cursor.execute(
            "INSERT INTO Assignments (meeting_id, assignment_type, assignment_label, titular_id, companion_id, position) VALUES (?, ?, ?, ?, ?, ?)",
            (meeting_row[0], assignment, assignment_text, titular_row[0], companion_id, position)
        )


    def _normalize_log_week_starts(self, cursor):
        cursor.execute("SELECT id, week_start FROM Meetings WHERE week_start LIKE 'log:%' ORDER BY week_start ASC")
        rows = cursor.fetchall()
        for index, (meeting_id, _) in enumerate(rows):
            week_start = (datetime.date(1900, 1, 1) + datetime.timedelta(days=index * 7)).isoformat()
            cursor.execute("UPDATE Meetings SET week_start = ? WHERE id = ?", (week_start, meeting_id))


    def _rebuild_assignment_cache(self, cursor):
        for assignment in ASSIGNATION_FIELDS:
            cursor.execute(f"UPDATE Witnesses SET {assignment} = NULL")
        cursor.execute("UPDATE Witnesses SET last_assignation = NULL, last_assignment_type = NULL")
        cursor.execute(
            """SELECT m.week_start, a.assignment_type, a.titular_id, a.companion_id
               FROM Assignments a
               JOIN Meetings m ON m.id = a.meeting_id
               ORDER BY m.week_start ASC, a.position ASC"""
        )
        for week_start, assignment, titular_id, companion_id in cursor.fetchall():
            if assignment in ASSIGNATION_FIELDS:
                cursor.execute(
                    f"UPDATE Witnesses SET {assignment} = ?, last_assignation = ?, last_assignment_type = ? WHERE id = ?",
                    (week_start, week_start, assignment, titular_id)
                )
            if companion_id:
                cursor.execute(
                    "UPDATE Witnesses SET companion_male = ?, companion_female = ?, last_assignation = ?, last_assignment_type = ? WHERE id = ?",
                    (week_start, week_start, week_start, "companion", companion_id)
                )

    def create_new_participant(self, values):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        query = "INSERT INTO Witnesses (name, phone, gender, role, exclude, custom, companion_only, replacements) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(query, values)
        con.commit()
        cur.close()
        con.close()


    def read_all_participants_names(self):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT name FROM Witnesses ORDER BY name ASC")
        rows = cur.fetchall()
        cur.close()
        con.close()
        return rows
    

    def read_participant(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT * FROM Witnesses WHERE name = ?", (name,))
        rows = cur.fetchall()
        cur.close()
        con.close()
        return rows
    

    def modify_participant(self, id, new_data):
        new_data.append(id)
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        query = "UPDATE Witnesses SET name = ?, phone = ?, gender = ?, role = ?, exclude = ?, custom = ?, companion_only = ?, replacements = ? WHERE id = ?"
        cur.execute(query, new_data)
        con.commit()
        cur.close()
        con.close()


    def delete_participant(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("DELETE FROM Witnesses WHERE name = ?", (name,))
        con.commit()
        cur.close()
        con.close()


    def read_data_for_assignations(self, replacements = False):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        witnesses = deepcopy(WITNESS_GROUPS)
        settings = self._read_scheduler_settings(cur)

        try:
            if replacements == True:
                for query in ASSIGNATION_QUERIES:
                    query_settings = self._settings_for_assignment(cur, settings, query["assignation"])
                    cur.execute("SELECT * FROM Witnesses WHERE " + query["where"] + " AND replacements = 1")
                    witnesses[query["role"]][query["assignation"]] = sort_witnesses(cur.fetchall(), query["assignation"], replacements=True, settings=query_settings)
            else:
                for query in ASSIGNATION_QUERIES:
                    query_settings = self._settings_for_assignment(cur, settings, query["assignation"])
                    cur.execute("SELECT * FROM Witnesses WHERE " + query["where"])
                    witnesses[query["role"]][query["assignation"]] = sort_witnesses(cur.fetchall(), query["assignation"], settings=query_settings)
        except Exception as e:
            print(e)

        cur.close()
        con.close()
        return witnesses

    def read_data_for_assignments(self, replacements=False):
        return self.read_data_for_assignations(replacements)
    
    def read_data_for_simplified_assignations(self, replacements = False):
        return self.read_data_for_assignations(replacements)

    def read_data_for_simplified_assignments(self, replacements=False):
        return self.read_data_for_simplified_assignations(replacements)


    def _settings_for_assignment(self, cursor, settings, assignment):
        query_settings = dict(settings)
        query_settings["recent_assignment_counts"] = self._recent_assignment_counts(
            cursor,
            settings["avoid_multiple_assignments_weeks"]
        )
        query_settings["recent_same_assignment_names"] = self._recent_same_assignment_names(
            cursor,
            assignment,
            settings["avoid_same_assignment_weeks"]
        )
        query_settings["recent_companion_counts"] = self._recent_companion_counts(
            cursor,
            settings["frequent_companion_weeks"]
        )
        query_settings["recent_school_participation_names"] = self._recent_school_participation_names(
            cursor,
            settings["avoid_school_participation_weeks"]
        )
        return query_settings


    def _recent_assignment_counts(self, cursor, weeks):
        if weeks <= 0:
            return {}
        week_starts = self._recent_week_starts(cursor, weeks)
        if not week_starts:
            return {}
        placeholders = ",".join("?" for _ in week_starts)
        cursor.execute(
            f"""SELECT w.name, COUNT(*)
                FROM Assignments a
                JOIN Meetings m ON m.id = a.meeting_id
                JOIN Witnesses w ON w.id = a.titular_id
                WHERE m.week_start IN ({placeholders})
                GROUP BY w.name""",
            week_starts
        )
        counts = dict(cursor.fetchall())
        cursor.execute(
            f"""SELECT w.name, COUNT(*)
                FROM Assignments a
                JOIN Meetings m ON m.id = a.meeting_id
                JOIN Witnesses w ON w.id = a.companion_id
                WHERE m.week_start IN ({placeholders})
                GROUP BY w.name""",
            week_starts
        )
        for name, count in cursor.fetchall():
            counts[name] = counts.get(name, 0) + count
        return counts


    def _recent_same_assignment_names(self, cursor, assignment, weeks):
        if weeks <= 0:
            return set()
        week_starts = self._recent_week_starts(cursor, weeks)
        if not week_starts:
            return set()
        placeholders = ",".join("?" for _ in week_starts)
        cursor.execute(
            f"""SELECT DISTINCT w.name
                FROM Assignments a
                JOIN Meetings m ON m.id = a.meeting_id
                JOIN Witnesses w ON w.id = a.titular_id
                WHERE a.assignment_type = ? AND m.week_start IN ({placeholders})""",
            [assignment] + week_starts
        )
        return {row[0] for row in cursor.fetchall()}


    def _recent_companion_counts(self, cursor, weeks):
        if weeks <= 0:
            return {}
        week_starts = self._recent_week_starts(cursor, weeks)
        if not week_starts:
            return {}
        placeholders = ",".join("?" for _ in week_starts)
        cursor.execute(
            f"""SELECT w.name, COUNT(*)
                FROM Assignments a
                JOIN Meetings m ON m.id = a.meeting_id
                JOIN Witnesses w ON w.id = a.companion_id
                WHERE a.companion_id IS NOT NULL AND m.week_start IN ({placeholders})
                GROUP BY w.name""",
            week_starts
        )
        return dict(cursor.fetchall())


    def _recent_school_participation_names(self, cursor, weeks):
        if weeks <= 0:
            return set()
        week_starts = self._recent_week_starts(cursor, weeks)
        if not week_starts:
            return set()
        placeholders = ",".join("?" for _ in week_starts)
        school_assignments = ["first", "revisit", "course", "explain", "speech"]
        assignment_placeholders = ",".join("?" for _ in school_assignments)
        cursor.execute(
            f"""SELECT DISTINCT w.name
                FROM Assignments a
                JOIN Meetings m ON m.id = a.meeting_id
                JOIN Witnesses w ON w.id = a.titular_id
                WHERE a.assignment_type IN ({assignment_placeholders})
                AND m.week_start IN ({placeholders})""",
            school_assignments + week_starts
        )
        return {row[0] for row in cursor.fetchall()}


    def _recent_week_starts(self, cursor, weeks):
        cursor.execute("SELECT week_start FROM Meetings ORDER BY week_start DESC LIMIT ?", (weeks,))
        return [row[0] for row in cursor.fetchall()]
    

    def write_data(self, data_dict, week_label=None):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        meeting_id = None
        meeting_assignments = [data for data in data_dict if data[0] != "replacements_date"]
        if meeting_assignments:
            week_start = self._format_date(meeting_assignments[0][2])
            cur.execute(
                "INSERT INTO Meetings (week_start, week_label) VALUES (?, ?) ON CONFLICT(week_start) DO UPDATE SET week_label = excluded.week_label",
                (week_start, week_label)
            )
            cur.execute("SELECT id FROM Meetings WHERE week_start = ?", (week_start,))
            meeting_id = cur.fetchone()[0]
            cur.execute("DELETE FROM Assignments WHERE meeting_id = ?", (meeting_id,))

        for position, data in enumerate(data_dict):
            assignment = data[0]
            titular = data[1]
            week = self._format_date(data[2])
            if assignment not in ASSIGNATION_FIELDS and assignment != "replacements_date":
                continue
            if not titular:
                continue
            if assignment == "replacements_date":
                cur.execute("UPDATE Witnesses SET replacements_date = ? WHERE name = ?", (week, titular))
                continue
            cur.execute("SELECT id FROM Witnesses WHERE name = ?", (titular,))
            titular_row = cur.fetchone()
            if not titular_row:
                continue
            titular_id = titular_row[0]
            companion_id = None
            cur.execute(
                f"UPDATE Witnesses SET {assignment} = ?, last_assignation = ?, last_assignment_type = ? WHERE name = ?",
                (week, week, assignment, titular)
            )
            if len(data) == 4:
                companion = data[3]
                if companion:
                    cur.execute("SELECT id FROM Witnesses WHERE name = ?", (companion,))
                    companion_row = cur.fetchone()
                    if companion_row:
                        companion_id = companion_row[0]
                    cur.execute(
                        "UPDATE Witnesses SET companion_male = ?, companion_female = ?, last_assignation = ?, last_assignment_type = ? WHERE name = ?",
                        (week, week, week, "companion", companion)
                    )
            if meeting_id is not None:
                cur.execute(
                    "INSERT INTO Assignments (meeting_id, assignment_type, assignment_label, titular_id, companion_id, position) VALUES (?, ?, ?, ?, ?, ?)",
                    (meeting_id, assignment, assignment_label(assignment), titular_id, companion_id, position)
                )
        if meeting_id is not None:
            self._rebuild_assignment_cache(cur)
        con.commit()
        cur.close()
        con.close()

    def write_assignment_data(self, assignments, week_label=None):
        self.write_data(assignments, week_label)


    def update_meeting(self, week_label, data_dict):
        self.create_backup("before_edit_meeting")
        self.write_data(data_dict, week_label)


    def meeting_week_start(self, week_label):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT week_start FROM Meetings WHERE week_label = ?", (week_label,))
        row = cur.fetchone()
        cur.close()
        con.close()
        return row[0] if row else None


    def _format_date(self, value):
        if isinstance(value, datetime.datetime):
            return value.date().isoformat()
        if isinstance(value, datetime.date):
            return value.isoformat()
        return value


    def create_backup(self, reason):
        if not os.path.exists(self.table_name):
            return None
        backup_dir = os.path.join("data", "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"witnesses_{reason}_{timestamp}.db")
        shutil.copy2(self.table_name, backup_path)
        return backup_path


    def update_scheduler_setting(self, key, value):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO SchedulerSettings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, str(value))
        )
        con.commit()
        cur.close()
        con.close()


    def read_scheduler_settings(self):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        settings = self._read_scheduler_settings(cur)
        cur.close()
        con.close()
        return settings


    def read_meeting_weeks(self):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT week_label FROM Meetings ORDER BY week_start ASC")
        rows = [row[0] for row in cur.fetchall() if row[0]]
        cur.close()
        con.close()
        return rows


    def read_meeting_assignments(self, week_label):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute(
            """SELECT a.assignment_type, a.assignment_label, titular.name, companion.name
               FROM Assignments a
               JOIN Meetings m ON m.id = a.meeting_id
               JOIN Witnesses titular ON titular.id = a.titular_id
               LEFT JOIN Witnesses companion ON companion.id = a.companion_id
               WHERE m.week_label = ?
               ORDER BY a.position ASC""",
            (week_label,)
        )
        rows = cur.fetchall()
        cur.close()
        con.close()
        return rows


    def read_meeting_report(self, week_label):
        assignments = self.read_meeting_assignments(week_label)
        lines = [week_label, ""]
        for _, label, titular, companion in assignments:
            if companion:
                lines.append(f"{label}: {titular} - {companion}")
            else:
                lines.append(f"{label}: {titular}")
        return "\n".join(lines)


    def export_data(self, file_path):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        export = {}
        for table in ["Witnesses", "Meetings", "Assignments", "SchedulerSettings"]:
            cur.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cur.fetchall()]
            cur.execute(f"SELECT * FROM {table}")
            export[table] = {"columns": columns, "rows": cur.fetchall()}
        cur.close()
        con.close()
        with open(file_path, "w") as file:
            json.dump(export, file, indent=2)


    def import_data(self, file_path):
        self.create_backup("before_import")
        with open(file_path, "r") as file:
            imported = json.load(file)
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        for table in ["Assignments", "Meetings", "Witnesses", "SchedulerSettings"]:
            cur.execute(f"DELETE FROM {table}")
        for table in ["Witnesses", "Meetings", "Assignments", "SchedulerSettings"]:
            table_data = imported.get(table)
            if not table_data:
                continue
            columns = table_data["columns"]
            placeholders = ",".join("?" for _ in columns)
            column_names = ",".join(columns)
            for row in table_data["rows"]:
                cur.execute(f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})", row)
        self._ensure_default_settings(cur)
        self._rebuild_assignment_cache(cur)
        con.commit()
        cur.close()
        con.close()


    def assignment_summary(self, name, assignment):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        fields = f"last_assignation, last_assignment_type, {assignment}"
        cur.execute(f"SELECT {fields} FROM Witnesses WHERE name = ?", (name,))
        row = cur.fetchone()
        cur.close()
        con.close()
        if not row:
            return ""
        last_assignation, last_assignment_type, same_assignment = row
        last_assignation = last_assignation or "sin registro"
        same_assignment = same_assignment or "sin registro"
        if last_assignment_type == assignment:
            note = "evitar repetir esta misma parte"
        else:
            note = "buena opción para rotar"
        return f"{name}: última asignación {last_assignation}; última vez en {assignment_label(assignment)} {same_assignment}; {note}."


    def get_phone_number(self, name):
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT phone FROM Witnesses WHERE name = ?", (name,))
        rows = cur.fetchall()
        cur.close()
        con.close()

        if rows:
            phone_number = rows[0][0]
            return phone_number
        else:
            return None
        

    def clean(self):
        self.create_backup("before_clean")
        today = datetime.date.today().strftime('%Y-%m-%d')
        assignation_list = ASSIGNATION_FIELDS + ["last_assignation", "replacements_date"]

        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        for assignation in assignation_list:
            cur.execute(f"SELECT name FROM Witnesses WHERE {assignation} > ?", (today,))
            person_list = cur.fetchall()
            if person_list != []:
                for person in person_list:
                    name = person[0]
                    cur.execute(f"UPDATE Witnesses SET {assignation} = NULL WHERE name = ?", (name,))
        cur.execute("UPDATE Witnesses SET last_assignment_type = NULL WHERE last_assignation IS NULL")
        cur.execute("DELETE FROM Assignments")
        cur.execute("DELETE FROM Meetings")
        con.commit()
        cur.close()
        con.close()


    def delete_meetings_until(self, week_label):
        self.create_backup("before_delete_meetings")
        con = sqlite3.connect(self.table_name)
        cur = con.cursor()
        cur.execute("SELECT week_start FROM Meetings WHERE week_label = ?", (week_label,))
        row = cur.fetchone()
        if row:
            week_start = row[0]
            cur.execute("SELECT id FROM Meetings WHERE week_start <= ?", (week_start,))
            meeting_ids = [item[0] for item in cur.fetchall()]
            for meeting_id in meeting_ids:
                cur.execute("DELETE FROM Assignments WHERE meeting_id = ?", (meeting_id,))
                cur.execute("DELETE FROM Meetings WHERE id = ?", (meeting_id,))
            self._rebuild_assignment_cache(cur)
        con.commit()
        cur.close()
        con.close()
