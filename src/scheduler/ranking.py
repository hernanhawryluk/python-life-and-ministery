import datetime


ASSIGNATION_FIELDS = [
    "initial_pray",
    "ending_pray",
    "read_bible",
    "first",
    "revisit",
    "course",
    "explain",
    "speech",
    "companion_male",
    "companion_female",
    "read_book",
    "treasures",
    "pearls",
    "book",
    "random_1",
    "random_2",
    "masters",
    "presidency",
    "needs",
]

FIELD_INDEX = {
    "id": 0,
    "name": 1,
    "phone": 2,
    "gender": 3,
    "role": 4,
    "exclude": 5,
    "custom": 6,
    "companion_only": 7,
    "replacements": 8,
    "replacements_date": 9,
    "initial_pray": 10,
    "ending_pray": 11,
    "read_bible": 12,
    "first": 13,
    "revisit": 14,
    "course": 15,
    "explain": 16,
    "speech": 17,
    "companion_male": 18,
    "companion_female": 19,
    "read_book": 20,
    "treasures": 21,
    "pearls": 22,
    "book": 23,
    "random_1": 24,
    "random_2": 25,
    "masters": 26,
    "presidency": 27,
    "needs": 28,
    "last_assignation": 29,
    "last_assignment_type": 30,
}

OLD_DATE = datetime.date.min

DEFAULT_RANKING_SETTINGS = {
    "avoid_same_last_assignment": True,
    "rotation_priority": "last_assignment",
    "avoid_same_assignment_weeks": 5,
    "avoid_multiple_assignments_weeks": 1,
    "avoid_frequent_companions": False,
    "frequent_companion_weeks": 0,
    "avoid_school_participation_weeks": 5,
}

SCHOOL_ASSIGNMENTS = {"first", "revisit", "course", "explain", "speech"}


def parse_date(value):
    if value in (None, ""):
        return OLD_DATE
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    return datetime.date.fromisoformat(str(value))


def sort_witnesses(witnesses, assignment, replacements=False, settings=None):
    settings = settings or DEFAULT_RANKING_SETTINGS
    recent_assignments = settings.get("recent_assignment_counts", {})
    recent_same_assignments = settings.get("recent_same_assignment_names", set())
    recent_companions = settings.get("recent_companion_counts", {})
    recent_school_participants = settings.get("recent_school_participation_names", set())

    def key(witness):
        name = witness[FIELD_INDEX["name"]]
        last_assignment = parse_date(witness[FIELD_INDEX["last_assignation"]])
        same_assignment = parse_date(witness[FIELD_INDEX[assignment]])
        last_assignment_type = witness[FIELD_INDEX["last_assignment_type"]]
        replacement_date = parse_date(witness[FIELD_INDEX["replacements_date"]])

        same_last_penalty = last_assignment_type == assignment if settings["avoid_same_last_assignment"] else False
        recent_same_penalty = name in recent_same_assignments
        recent_assignment_penalty = recent_assignments.get(name, 0) > 0
        recent_school_penalty = assignment in SCHOOL_ASSIGNMENTS and name in recent_school_participants
        frequent_companion_penalty = (
            assignment in ["companion_male", "companion_female"]
            and settings.get("avoid_frequent_companions", False)
            and recent_companions.get(name, 0) > 0
        )
        if settings["rotation_priority"] == "specific_assignment":
            ranking = (
                recent_same_penalty,
                recent_assignment_penalty,
                recent_school_penalty,
                frequent_companion_penalty,
                same_last_penalty,
                same_assignment,
                last_assignment,
                name,
            )
        else:
            ranking = (
                recent_assignment_penalty,
                recent_same_penalty,
                recent_school_penalty,
                frequent_companion_penalty,
                same_last_penalty,
                last_assignment,
                same_assignment,
                name,
            )
        if replacements:
            return (replacement_date,) + ranking
        return ranking

    return sorted(witnesses, key=key)
