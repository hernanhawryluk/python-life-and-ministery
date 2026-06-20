import unittest

from src.utils.participants_console import format_participants


class ParticipantsConsoleTests(unittest.TestCase):
    def test_groups_and_orders_by_role_then_name(self):
        participants = [
            ("Ángel Pérez", "Hombre", "Anciano", 0, 0, 0, 0),
            ("Carlos Díaz", "Hombre", "Estudiante +", 0, 0, 0, 1),
            ("Bruno López", "Hombre", "Estudiante", 1, 0, 0, 0),
            ("Abel Sosa", "Hombre", "Anciano", 0, 0, 0, 0),
            ("Ana Torres", "Mujer", "Estudiante", 0, 1, 1, 0),
        ]

        result = format_participants(participants)

        self.assertLess(result.index("Bruno López"), result.index("Carlos Díaz"))
        self.assertLess(result.index("Carlos Díaz"), result.index("Abel Sosa"))
        self.assertLess(result.index("Abel Sosa"), result.index("Ángel Pérez"))
        self.assertLess(result.index("HOMBRES:"), result.index("MUJERES:"))

    def test_formats_role_and_active_conditions(self):
        participants = [
            ("Luis Gómez", "Hombre", "Ministerial", 1, 1, 0, 1),
            ("Laura Paz", "Mujer", "Estudiante", 0, 0, 0, 0),
        ]

        result = format_participants(participants)

        self.assertIn(
            "Luis Gómez - Hombre - Siervo Ministerial - "
            "Omitir temporalmente, Limitado por edad, Acepta remplazos",
            result,
        )
        self.assertIn("Laura Paz - Mujer - Estudiante", result)
        self.assertNotIn("Sin restricciones", result)


if __name__ == "__main__":
    unittest.main()
