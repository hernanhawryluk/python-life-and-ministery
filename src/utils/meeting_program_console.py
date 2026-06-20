import datetime
import re
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin

from src.utils.meeting_program import fetch_url, find_detail_url
from src.utils.weeks import calculate_weeks


SECTION_TITLES = {
    "TESOROS DE LA BIBLIA",
    "SEAMOS MEJORES MAESTROS",
    "NUESTRA VIDA CRISTIANA",
}
MONTH_PATTERN = (
    r"(?:ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|"
    r"SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)"
)
WEEK_PATTERN = re.compile(
    rf"^(?:\d{{1,2}}\s*-\s*\d{{1,2}}\s+DE\s+{MONTH_PATTERN}|"
    rf"\d{{1,2}}\s+DE\s+{MONTH_PATTERN}\s+A\s+\d{{1,2}}\s+DE\s+{MONTH_PATTERN})$",
    re.IGNORECASE,
)
NUMBERED_PART_PATTERN = re.compile(r"^\d+\.\s+")


@dataclass
class ContentBlock:
    text: str
    tag: str = ""
    links: list[tuple[str, str]] = field(default_factory=list)


class WolContentParser(HTMLParser):
    """Extract WOL content blocks while preserving their inline links."""

    def __init__(self, base_url=""):
        super().__init__()
        self.base_url = base_url
        self.blocks = []
        self.block_depth = 0
        self.block_tag = ""
        self.fragments = []
        self.links = []
        self.anchor_depth = 0
        self.anchor_href = ""
        self.anchor_fragments = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.block_depth and "data-pid" in attrs:
            self.block_depth = 1
            self.block_tag = tag
            self.fragments = []
            self.links = []
            return

        if not self.block_depth:
            return

        self.block_depth += 1
        if tag == "a" and not self.anchor_depth:
            self.anchor_depth = self.block_depth
            self.anchor_href = urljoin(self.base_url, attrs.get("href", ""))
            self.anchor_fragments = []

    def handle_endtag(self, tag):
        if not self.block_depth:
            return

        if tag == "a" and self.anchor_depth:
            label = normalize_text("".join(self.anchor_fragments))
            if label:
                self.links.append((label, self.anchor_href))
                self.fragments.append(markdown_link(label, self.anchor_href))
            self.anchor_depth = 0
            self.anchor_href = ""
            self.anchor_fragments = []

        self.block_depth -= 1
        if self.block_depth == 0:
            text = normalize_markdown(" ".join(self.fragments))
            if text:
                self.blocks.append(ContentBlock(text, self.block_tag, self.links))

    def handle_data(self, data):
        if not self.block_depth:
            return
        if self.anchor_depth:
            self.anchor_fragments.append(data)
        else:
            self.fragments.append(data)


def fetch_week_console_program(week_start, timeout=20):
    """Fetch one week using the same WOL URL strategy as the desktop app."""
    year, week_number, _ = week_start.isocalendar()
    urls = [
        f"https://wol.jw.org/es/wol/dt/r4/lp-s/{week_start.year}/{week_start.month}/{week_start.day}",
        f"https://wol.jw.org/es/wol/meetings/r4/lp-s/{year}/{week_number}",
    ]
    errors = []

    for url in urls:
        content = fetch_url(url, timeout)
        if isinstance(content, dict):
            errors.append(content.get("error", "Error desconocido"))
            continue

        program = parse_console_program_html(content, url)
        if program:
            return program

        detail_url = find_detail_url(content, url)
        if not detail_url:
            continue
        detail_content = fetch_url(detail_url, timeout)
        if isinstance(detail_content, dict):
            errors.append(detail_content.get("error", "Error desconocido"))
            continue
        program = parse_console_program_html(detail_content, detail_url)
        if program:
            return program

    message = "; ".join(error for error in errors if error)
    raise RuntimeError(message or "No se detectó el programa semanal en WOL.")


def parse_console_program_html(content, url=""):
    parser = WolContentParser(url)
    parser.feed(content)
    blocks = parser.blocks
    start = next((index for index, block in enumerate(blocks) if is_week_heading(block.text)), None)
    if start is None:
        return None

    relevant = []
    for block in blocks[start:]:
        if relevant and is_week_heading(block.text):
            break
        relevant.append(block)

    if not any(normalized_plain(block.text) == "seamos mejores maestros" for block in relevant):
        return None

    return format_program_blocks(relevant)


def format_program_blocks(blocks):
    lines = [f"Semana del: {plain_text(blocks[0].text).upper()}"]
    base = find_base_text(blocks[1:])
    if base:
        lines.extend([f"Texto base: {base}", ""])

    current_section = ""
    index = 1
    while index < len(blocks):
        block = blocks[index]
        plain = plain_text(block.text)
        normalized = normalized_plain(block.text)

        if base and block.text == base:
            index += 1
            continue
        if normalized in {title.lower() for title in SECTION_TITLES}:
            current_section = plain.upper()
            suffix = ":" if current_section != "NUESTRA VIDA CRISTIANA" else ""
            append_paragraph(lines, f"{current_section}{suffix}")
            index += 1
            continue
        if is_song_and_prayer(normalized):
            append_paragraph(lines, trim_song_line(block.text))
            index += 1
            continue
        if NUMBERED_PART_PATTERN.match(plain):
            append_paragraph(lines, block.text)
            details, index = collect_part_details(blocks, index + 1)
            selected = select_details(current_section, plain, details)
            for detail in selected:
                append_paragraph(lines, detail)
            continue
        index += 1

    return plain_text("\n".join(lines).strip())


def collect_part_details(blocks, index):
    details = []
    while index < len(blocks):
        plain = plain_text(blocks[index].text)
        normalized = normalized_plain(blocks[index].text)
        if NUMBERED_PART_PATTERN.match(plain) or normalized in {
            title.lower() for title in SECTION_TITLES
        } or is_song_and_prayer(normalized) or is_week_heading(plain):
            break
        if not is_noise(blocks[index].text):
            details.append(blocks[index])
        index += 1
    return details, index


def select_details(section, title, details):
    if not details:
        return []

    if section == "TESOROS DE LA BIBLIA":
        if "lectura de la biblia" not in normalized_plain(title):
            return []
        scripture = first_scripture_link(details)
        return [scripture] if scripture else [strip_timing(details[0].text)]

    if section == "SEAMOS MEJORES MAESTROS":
        return [details[0].text]

    if section == "NUESTRA VIDA CRISTIANA":
        if "estudio biblico de la congregacion" in normalized_plain(title):
            return []
        selected = [details[0].text]
        for detail in details[1:]:
            text = plain_text(detail.text)
            if "?" in text or text.lower() == "respuesta":
                break
            selected.append(detail.text)
            break
        return selected

    return []


def first_scripture_link(details):
    scripture_pattern = re.compile(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{1,5}\s+\d+[:\d,\-– ]+")
    for detail in details:
        for label, href in detail.links:
            if scripture_pattern.search(label):
                return markdown_link(label, href)
    return ""


def find_base_text(blocks):
    for block in blocks:
        normalized = normalized_plain(block.text)
        if normalized in {title.lower() for title in SECTION_TITLES} or is_song_and_prayer(normalized):
            break
        if block.tag == "h2":
            return block.text
    return ""


def next_month_weeks(reference_date=None):
    if reference_date is None:
        return calculate_weeks()
    year = reference_date.year + (reference_date.month // 12)
    month = (reference_date.month % 12) + 1
    first = datetime.date(year, month, 1)
    monday = first + datetime.timedelta(days=(7 - first.weekday()) % 7)
    weeks = []
    while monday.month == month:
        weeks.append((monday, monday + datetime.timedelta(days=6)))
        monday += datetime.timedelta(days=7)
    return weeks


def fetch_next_month_program(reference_date=None, timeout=20):
    programs = []
    for week_start, _ in next_month_weeks(reference_date):
        try:
            programs.append(fetch_week_console_program(week_start, timeout))
        except RuntimeError as error:
            raise RuntimeError(
                f"semana del {week_start.strftime('%d/%m/%Y')}: {error}"
            ) from error
    return "\n\n---\n\n".join(programs)


def append_paragraph(lines, text):
    if not text:
        return
    if lines and lines[-1] != "":
        lines.append("")
    lines.append(text)


def is_week_heading(text):
    return bool(WEEK_PATTERN.match(plain_text(text).upper()))


def is_song_and_prayer(normalized):
    return "cancion" in normalized and "oracion" in normalized


def trim_song_line(text):
    parts = re.split(r"\s*\|\s*", text, maxsplit=1)
    if len(parts) == 2 and "palabras de conclusion" in normalized_plain(parts[0]):
        return parts[1].strip()
    return parts[0].strip()


def strip_timing(text):
    return re.sub(r"^\(\d+\s+mins?\.\)\s*", "", text).strip()


def is_noise(text):
    normalized = normalized_plain(text)
    return normalized in {"respuesta", "reproducir", "atras", "siguiente"} or normalized.startswith("image:")


def markdown_link(label, href):
    return f"[{label}]({href})" if href else label


def normalize_text(text):
    return re.sub(r"\s+", " ", unescape(text)).strip()


def normalize_markdown(text):
    text = normalize_text(text).replace(" ]", "]").replace("[ ", "[")
    text = re.sub(r"\(\s+(?=\[)", "(", text)
    text = re.sub(r"(?<=\))\s+([.,;:])", r"\1", text)
    text = re.sub(r"(?<=[\])])\s+\)", ")", text)
    return text


def plain_text(text):
    return re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", text)


def normalized_plain(text):
    value = plain_text(text).lower()
    for source, target in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ü", "u")):
        value = value.replace(source, target)
    return normalize_text(value)
