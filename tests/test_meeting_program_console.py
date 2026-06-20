import datetime
import unittest

from src.utils.meeting_program_console import (
    ContentBlock,
    find_base_text,
    is_week_heading,
    next_month_weeks,
    parse_console_program_html,
)


SAMPLE_HTML = """
<h1 data-pid="1">6-12 DE JULIO</h1>
<h2 data-pid="2"><a href="/es/wol/bc/r4/lp-s/202026241/0/0">JEREMÍAS 13-15</a></h2>
<h3 data-pid="3"><a href="/es/wol/pc/r4/lp-s/202026241/0/0">Canción 123</a> y oración | Palabras de introducción (1 min.)</h3>
<h2 data-pid="4">TESOROS DE LA BIBLIA</h2>
<h3 data-pid="5">1. Jehová merece que le obedezcamos</h3>
<p data-pid="6">(10 mins.)</p>
<h3 data-pid="7">2. Busquemos perlas escondidas</h3>
<p data-pid="8">(10 mins.) Pregunta que no debe mostrarse.</p>
<h3 data-pid="9">3. Lectura de la Biblia</h3>
<p data-pid="10">(4 mins.) <a href="/es/wol/bc/r4/lp-s/202026241/4/0">Jer 13:1-14</a> (th 2).</p>
<h2 data-pid="11">SEAMOS MEJORES MAESTROS</h2>
<h3 data-pid="12">4. Empiece conversaciones</h3>
<p data-pid="13">(3 mins.) DE CASA EN CASA. Use un tratado para empezar una conversación.</p>
<h2 data-pid="14">NUESTRA VIDA CRISTIANA</h2>
<h3 data-pid="15">5. “Obedecer es mejor que ofrecer un sacrificio”</h3>
<p data-pid="16">(15 mins.) Análisis con el auditorio.</p>
<p data-pid="17">Samuel le dijo al rey Saúl que obedecer es mejor.</p>
<p data-pid="18">¿Qué aprendemos de este relato?</p>
<h3 data-pid="19">6. Estudio bíblico de la congregación</h3>
<h3 data-pid="20">Palabras de conclusión (3 mins.) | <a href="/es/wol/pc/r4/lp-s/202026241/13/0">Canción 61</a> y oración</h3>
"""


class MeetingProgramConsoleTests(unittest.TestCase):
    def test_formats_requested_sections_without_urls(self):
        result = parse_console_program_html(SAMPLE_HTML, "https://wol.jw.org")

        self.assertIn("Semana del: 6-12 DE JULIO", result)
        self.assertIn("Texto base: JEREMÍAS 13-15", result)
        self.assertNotIn("Pregunta que no debe", result)
        self.assertIn("Jer 13:1-14", result)
        self.assertIn("Use un tratado para empezar una conversación.", result)
        self.assertIn("Samuel le dijo al rey Saúl", result)
        self.assertNotIn("¿Qué aprendemos", result)
        self.assertIn("Canción 61 y oración", result)
        self.assertNotIn("https://", result)
        self.assertNotIn("](", result)

    def test_next_month_starts_with_first_monday_inside_month(self):
        weeks = next_month_weeks(datetime.date(2026, 6, 20))

        self.assertEqual(weeks[0], (datetime.date(2026, 7, 6), datetime.date(2026, 7, 12)))
        self.assertEqual(weeks[-1], (datetime.date(2026, 7, 27), datetime.date(2026, 8, 2)))

    def test_recognizes_week_heading_that_crosses_into_next_month(self):
        self.assertTrue(is_week_heading("27 DE JULIO A 2 DE AGOSTO"))

    def test_finds_base_text_when_bible_chapters_use_a_comma(self):
        base = ContentBlock("[JEREMÍAS 16, 17](https://wol.jw.org/example)", "h2")

        self.assertEqual(find_base_text([base]), base.text)


if __name__ == "__main__":
    unittest.main()
