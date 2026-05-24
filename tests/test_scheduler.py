import datetime
import os
import tempfile
import unittest

from src.database import DataBase
from src.scheduler.ranking import sort_witnesses
from src.scheduler.validation import validate_assignments
from src.utils.meeting_program import parse_program_html
from src.utils.weeks import calculate_weeks


class SchedulerTests(unittest.TestCase):
    def make_db(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        db = DataBase()
        db.table_name = tmp.name
        db.create_database()
        return db

    def test_ranking_avoids_repeating_same_last_assignment(self):
        empty = [None] * 31
        mariano = empty.copy()
        mariano[1] = "Mariano"
        mariano[27] = "2025-01-01"
        mariano[29] = "2024-01-01"
        mariano[30] = "presidency"

        esteban = empty.copy()
        esteban[1] = "Esteban"
        esteban[27] = "2026-01-01"
        esteban[29] = "2024-02-01"
        esteban[30] = "treasures"

        self.assertEqual(sort_witnesses([mariano, esteban], "presidency")[0][1], "Esteban")

    def test_validation_rejects_ineligible_bible_reader(self):
        db = self.make_db()
        db.create_new_participant(["Ana", "", "Mujer", "Estudiante", 0, 0, 0, 0])

        errors = validate_assignments([["read_bible", "Ana", datetime.date(2026, 6, 1)]], db)

        self.assertTrue(any("no está habilitado" in error for error in errors))

    def test_validation_rejects_mixed_gender_companions(self):
        db = self.make_db()
        db.create_new_participant(["Ana", "", "Mujer", "Estudiante", 0, 0, 0, 0])
        db.create_new_participant(["Luis", "", "Hombre", "Estudiante", 0, 0, 0, 0])

        errors = validate_assignments([["first", "Ana", datetime.date(2026, 6, 1), "Luis"]], db)

        self.assertTrue(any("mismo sexo" in error for error in errors))

    def test_write_data_records_meeting_history(self):
        db = self.make_db()
        db.create_new_participant(["Esteban", "", "Hombre", "Anciano", 0, 0, 0, 0])

        db.write_data([["presidency", "Esteban", datetime.date(2026, 6, 1)]], "Semana del 1 - 7 de Junio")

        self.assertEqual(db.read_meeting_weeks(), ["Semana del 1 - 7 de Junio"])
        self.assertEqual(db.read_meeting_assignments("Semana del 1 - 7 de Junio")[0][2], "Esteban")

    def test_calculate_weeks_handles_year_rollover(self):
        weeks = calculate_weeks(14)

        self.assertTrue(all(week[0] <= week[1] for week in weeks))

    def test_export_import_roundtrip(self):
        source = self.make_db()
        source.create_new_participant(["Esteban", "", "Hombre", "Anciano", 0, 0, 0, 0])
        source.write_data([["presidency", "Esteban", datetime.date(2026, 6, 1)]], "Semana del 1 - 7 de Junio")

        export_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        export_file.close()
        source.export_data(export_file.name)

        target = self.make_db()
        target.import_data(export_file.name)

        self.assertEqual(target.read_meeting_assignments("Semana del 1 - 7 de Junio")[0][2], "Esteban")
        os.unlink(export_file.name)

    def test_read_meeting_assignments_includes_school_assignments(self):
        db = self.make_db()
        db.create_new_participant(["Ana", "", "Mujer", "Estudiante", 0, 0, 0, 0])
        db.create_new_participant(["Laura", "", "Mujer", "Estudiante", 0, 0, 0, 0])

        db.write_data([["first", "Ana", datetime.date(2026, 6, 1), "Laura"]], "Semana del 1 - 7 de Junio")
        assignments = db.read_meeting_assignments("Semana del 1 - 7 de Junio")

        self.assertEqual(assignments[0], ("first", "Empiece conversaciones", "Ana", "Laura"))

    def test_scheduler_avoids_next_week_participation(self):
        db = self.make_db()
        db.create_new_participant(["Esteban", "", "Hombre", "Anciano", 0, 0, 0, 0])
        db.create_new_participant(["Bernardo", "", "Hombre", "Anciano", 0, 0, 0, 0])
        db.write_data([["presidency", "Esteban", datetime.date(2026, 6, 1)]], "Semana del 1 - 7 de Junio")

        candidates = db.read_data_for_assignations()["elders"]["needs"]

        self.assertEqual(candidates[0][1], "Bernardo")

    def test_scheduler_avoids_monthly_school_repetition(self):
        db = self.make_db()
        db.create_new_participant(["Ana", "", "Mujer", "Estudiante", 0, 0, 0, 0])
        db.create_new_participant(["Laura", "", "Mujer", "Estudiante", 0, 0, 0, 0])
        db.write_data([["first", "Ana", datetime.date(2026, 6, 1), "Laura"]], "Semana del 1 - 7 de Junio")

        candidates = db.read_data_for_assignations()["studients"]["revisit"]

        self.assertEqual(candidates[0][1], "Laura")

    def test_parse_program_html_detects_school_assignments(self):
        html = """
        <p data-pid="1">SEAMOS MEJORES MAESTROS</p>
        <p data-pid="3">1. Empiece conversaciones</p>
        <p data-pid="4">2. Haga revisitas</p>
        <p data-pid="5">3. Haga discípulos</p>
        <p data-pid="6">4. Discurso estudiantil</p>
        <p data-pid="7">NUESTRA VIDA CRISTIANA</p>
        <p data-pid="8">15 mins.: Jehová cuida de sus siervos</p>
        <p data-pid="9">15 mins.: Necesidades de la congregación</p>
        <p data-pid="10">30 mins.: Estudio bíblico de la congregación</p>
        """

        program = parse_program_html(html)

        self.assertTrue(program["ok"])
        self.assertEqual(
            program["school_assignments"],
            ["Empiece conversaciones", "Haga revisitas", "Haga discípulos", "Discurso estudiantil"],
        )
        self.assertEqual(program["life_assignments"], {"random_1": True, "random_2": False, "needs": True})

    def test_parse_program_html_classifies_audience_discussion_and_life_parts(self):
        html = """
        <p data-pid="1">SEAMOS MEJORES MAESTROS</p>
        <p data-pid="2">4. Valor: Lo que hizo Jesús (7 mins.) Análisis con el auditorio.</p>
        <p data-pid="3">5. Discurso estudiantil (5 mins.) th lección 12.</p>
        <p data-pid="4">NUESTRA VIDA CRISTIANA</p>
        <p data-pid="5">6. Cómo prepararnos para una emergencia (15 mins.) Análisis con el auditorio.</p>
        <p data-pid="6">7. Logros de la organización (15 mins.) Análisis con el auditorio.</p>
        <p data-pid="7">8. Estudio bíblico de la congregación (30 mins.)</p>
        """

        program = parse_program_html(html)

        self.assertEqual(program["school_assignments"], ["Análisis con el auditorio", "Discurso estudiantil"])
        self.assertEqual(program["life_assignments"], {"random_1": True, "random_2": True, "needs": False})

    def test_parse_program_html_detects_assignment_markers_from_2026_example(self):
        html = """
        <p data-pid="1">SEAMOS MEJORES MAESTROS</p>
        <p data-pid="2">4. Empiece conversaciones</p>
        <p data-pid="3">(3 mins.) DE CASA EN CASA.</p>
        <p data-pid="4">5. Haga revisitas</p>
        <p data-pid="5">(4 mins.) DE CASA EN CASA.</p>
        <p data-pid="6">6. Haga discípulos</p>
        <p data-pid="7">(5 mins.) Converse con alguien que estudia la Biblia.</p>
        <p data-pid="8">NUESTRA VIDA CRISTIANA</p>
        <p data-pid="9">Canción 76</p>
        <p data-pid="10">7. ¡Sé valiente como Jeremías! ASIGNACIÓN 1</p>
        <p data-pid="11">(6 mins.) Análisis con el auditorio.</p>
        <p data-pid="12">8. “Listos para presentar una defensa [...] con apacibilidad y profundo respeto” ASIGNACIÓN 2</p>
        <p data-pid="13">(9 mins.) Análisis con el auditorio.</p>
        """

        program = parse_program_html(html)

        self.assertEqual(program["school_assignments"], ["Empiece conversaciones", "Haga revisitas", "Haga discípulos"])
        self.assertEqual(program["life_assignments"], {"random_1": True, "random_2": True, "needs": False})


if __name__ == "__main__":
    unittest.main()
