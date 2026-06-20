import unicodedata

from src.database import DataBase


ROLE_ORDER = {
    "Estudiante": 0,
    "Estudiante +": 1,
    "Ministerial": 2,
    "Siervo Ministerial": 2,
    "Anciano": 3,
}
ROLE_LABELS = {
    "Ministerial": "Siervo Ministerial",
}
STATUS_LABELS = (
    (3, "Omitir temporalmente"),
    (4, "Limitado por edad"),
    (5, "Solo acompañante"),
    (6, "Acepta remplazos"),
)


def fetch_registered_participants(database=None):
    database = database or DataBase()
    return format_participants(database.read_all_participants())


def format_participants(participants):
    groups = {
        "Hombre": [],
        "Mujer": [],
    }
    for participant in participants:
        gender = participant[1]
        if gender in groups:
            groups[gender].append(participant)

    sections = []
    for gender, heading in (("Hombre", "HOMBRES"), ("Mujer", "MUJERES")):
        lines = [f"{heading}:"]
        ordered = sorted(groups[gender], key=participant_sort_key)
        if ordered:
            lines.extend(format_participant(participant) for participant in ordered)
        else:
            lines.append("Sin personas registradas")
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def participant_sort_key(participant):
    name, _, role = participant[:3]
    return ROLE_ORDER.get(role, 99), normalize_for_sorting(name)


def format_participant(participant):
    name, gender, role = participant[:3]
    role_label = ROLE_LABELS.get(role, role)
    statuses = [label for index, label in STATUS_LABELS if bool(participant[index])]
    participant_text = f"{name} - {gender} - {role_label}"
    if statuses:
        participant_text += f" - {', '.join(statuses)}"
    return participant_text


def normalize_for_sorting(value):
    decomposed = unicodedata.normalize("NFD", value.casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))
