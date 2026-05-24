from src.utils.switchers import assignment_label


COMPANION_ASSIGNMENTS = {"first", "revisit", "course", "explain"}


def validate_assignments(assignments, db):
    errors = []
    assigned_names = set()
    eligible = db.read_data_for_assignations()

    for assignment_data in assignments:
        assignment = assignment_data[0]
        titular = assignment_data[1]
        companion = assignment_data[3] if len(assignment_data) == 4 else ""
        label = assignment_label(assignment)

        if not titular:
            errors.append(f"{label}: falta elegir titular.")
            continue

        titular_data = db.read_participant(titular)
        if not titular_data:
            errors.append(f"{label}: {titular} no existe en participantes.")
            continue
        if titular not in eligible_names(eligible, assignment):
            errors.append(f"{label}: {titular} no está habilitado para esta asignación.")

        if titular in assigned_names:
            errors.append(f"{label}: {titular} ya tiene otra asignación esta semana.")
        assigned_names.add(titular)

        if companion:
            companion_data = db.read_participant(companion)
            if not companion_data:
                errors.append(f"{label}: {companion} no existe en participantes.")
                continue
            if companion == titular:
                errors.append(f"{label}: titular y ayudante no pueden ser la misma persona.")
            if companion in assigned_names:
                errors.append(f"{label}: {companion} ya tiene otra asignación esta semana.")
            assigned_names.add(companion)
            if assignment in COMPANION_ASSIGNMENTS and titular_data[0][3] != companion_data[0][3]:
                errors.append(f"{label}: titular y ayudante deben ser del mismo sexo.")
            if assignment in COMPANION_ASSIGNMENTS and companion not in eligible_companions(eligible, titular_data[0][3]):
                errors.append(f"{label}: {companion} no está habilitado como ayudante.")

    return errors


def eligible_names(eligible, assignment):
    if assignment in {"presidency", "needs"}:
        group = eligible["elders"]
    elif assignment in {"initial_pray", "ending_pray", "read_book"}:
        group = eligible["studients_plus"]
    elif assignment in {"treasures", "pearls", "book", "random_1", "random_2", "masters"}:
        group = eligible["ministerials"]
    else:
        group = eligible["studients"]
    return {row[1] for row in group[assignment]}


def eligible_companions(eligible, gender):
    key = "companion_female" if gender == "Mujer" else "companion_male"
    return {row[1] for row in eligible["studients"][key]}
