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
            "Necesidades Locales": "needs",
            "Estudio Biblico de Congregación": "book",
            "Lectura en Estudio Biblico": "read_book",
            "Oración final": "ending_pray",
        }
        return switcher[assignation]

def assignment_label(assignment):
      switcher = {
            "presidency": "Presidencia",
            "initial_pray": "Oración inicial",
            "treasures": "Tesoros de la Biblia",
            "pearls": "Busquemos Perlas Escondidas",
            "read_bible": "Lectura de la Biblia",
            "first": "Empiece conversaciones",
            "revisit": "Haga revisitas",
            "course": "Haga discípulos",
            "explain": "Explique sus creencias",
            "speech": "Discurso estudiantil",
            "masters": "Análisis con el auditorio",
            "random_1": "Asignación 1",
            "random_2": "Asignación 2",
            "needs": "Necesidades Locales",
            "book": "Estudio Biblico de Congregación",
            "read_book": "Lectura en Estudio Biblico",
            "ending_pray": "Oración final",
      }
      return switcher[assignment]

def determiner_switcher(assignment):
      switcher= {
            "Presidencia": "la Presidencia",
            "Oración inicial": "la oración inicial",
            "Tesoros de la Biblia": "los Tesoros de la Biblia",
            "Busquemos Perlas Escondidas": "la sección Busquemos Perlas Escondidas",
            "Lectura de la Biblia": "la Lectura de la Biblia",
            "Empiece conversaciones": "la sección Empiece conversaciones",
            "Haga revisitas": "la sección Haga revisitas",
            "Haga discípulos": "la sección Haga discípulos",
            "Explique sus creencias": "la sección Explique sus creencias",
            "Discurso estudiantil": "el Discurso estudiantil",
            "Análisis con el auditorio": "una asignación de Análisis con el auditorio",
            "Asignación 1": "una asignación en la sección Nuestra Vida Cristiana",
            "Asignación 2": "una asignación en la sección Nuestra Vida Cristiana",
            "Necesidades Locales": "las Necesidades Locales",
            "Estudio Biblico de Congregación": "el Estudio Biblico de Congregación",
            "Lectura en Estudio Biblico": "la Lectura en el Estudio Biblico",
            "Oración final": "la oración final",
      }
      return switcher[assignment]
