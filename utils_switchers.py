def school_switcher(name):
    switcher = {
        "Empiece conversaciones": "first",
        "Haga revisitas": "revisit",
        "Haga discípulos": "course",
        "Explique sus creencias": "explain",
        "Discurso estudiantil": "speech",
        "Análisis con el auditorio": "masters",
    }
    return switcher[name]

def meeting_switcher(assignation):
        switcher = {
            "Presidencia": "presidency",
            "Oración inicial": "initial_pray",
            "Tesoros de la Biblia": "treasures",
            "Busquemos Perlas Escondidas": "pearls",
            "Lectura de la Biblia": "read_bible",
            "Asignación 1": "random_1",
            "Asignación 2": "random_2",
            "Estudio Biblico de Congregación": "book",
            "Lectura en Estudio Biblico": "read_book",
            "Oración final": "ending_pray",
        }
        return switcher[assignation]