WITNESS_GROUPS = {
    "studients": {
        "read_bible": [],
        "first": [],
        "revisit": [],
        "course": [],
        "explain": [],
        "speech": [],
        "companion_male": [],
        "companion_female": [],
    },
    "studients_plus": {
        "initial_pray": [],
        "ending_pray": [],
        "read_book": [],
    },
    "ministerials": {
        "treasures": [],
        "pearls": [],
        "book": [],
        "random_1": [],
        "random_2": [],
        "masters": [],
    },
    "elders": {
        "presidency": [],
        "needs": [],
    },
}

WITNESS_GROUP_ALIASES = {
    "students": "studients",
    "students_plus": "studients_plus",
}

ASSIGNATION_QUERIES = [
    {"role": "studients", "assignation": "read_bible", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0"},
    {"role": "studients", "assignation": "first", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0"},
    {"role": "studients", "assignation": "revisit", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0"},
    {"role": "studients", "assignation": "course", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0 AND custom = 0"},
    {"role": "studients", "assignation": "explain", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND companion_only = 0 AND exclude = 0 AND custom = 0"},
    {"role": "studients", "assignation": "companion_male", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0"},
    {"role": "studients", "assignation": "companion_female", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Mujer' AND exclude = 0"},
    {"role": "studients", "assignation": "speech", "where": "(role = 'Estudiante' OR role = 'Estudiante +') AND gender = 'Hombre' AND exclude = 0"},
    {"role": "ministerials", "assignation": "masters", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0"},
    {"role": "studients_plus", "assignation": "read_book", "where": "(role = 'Estudiante +' OR role = 'Ministerial') AND exclude = 0"},
    {"role": "studients_plus", "assignation": "initial_pray", "where": "(role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0"},
    {"role": "studients_plus", "assignation": "ending_pray", "where": "(role = 'Estudiante +' OR role = 'Ministerial' OR role = 'Anciano') AND exclude = 0"},
    {"role": "ministerials", "assignation": "treasures", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0"},
    {"role": "ministerials", "assignation": "pearls", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0"},
    {"role": "ministerials", "assignation": "book", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0"},
    {"role": "ministerials", "assignation": "random_1", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0"},
    {"role": "ministerials", "assignation": "random_2", "where": "(role = 'Ministerial' or role = 'Anciano') AND exclude = 0"},
    {"role": "elders", "assignation": "presidency", "where": "role = 'Anciano' AND exclude = 0 AND custom = 0"},
    {"role": "elders", "assignation": "needs", "where": "role = 'Anciano' AND exclude = 0"},
]
