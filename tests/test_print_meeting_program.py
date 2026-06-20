import io
import time
import unittest

from print_meeting_program import ConsoleLoader


class TerminalStream(io.StringIO):
    def isatty(self):
        return True


class ConsoleLoaderTests(unittest.TestCase):
    def test_animates_and_clears_terminal_line(self):
        stream = TerminalStream()

        with ConsoleLoader("Cargando", stream=stream, interval=0.001):
            time.sleep(0.01)

        output = stream.getvalue()
        self.assertIn("Cargando...", output)
        self.assertTrue(output.endswith("\r\033[K"))


if __name__ == "__main__":
    unittest.main()
