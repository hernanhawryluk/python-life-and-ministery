import re
import urllib.error
import urllib.request
from urllib.parse import urljoin
from html import unescape
from html.parser import HTMLParser


SCHOOL_ASSIGNMENT_LABELS = [
    "Empiece conversaciones",
    "Haga revisitas",
    "Haga discípulos",
    "Explique sus creencias",
    "Discurso estudiantil",
    "Análisis con el auditorio",
]


class WolDataPidParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_data_pid = False
        self.depth = 0
        self.current = []
        self.items = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-pid" in attrs and not self.in_data_pid:
            self.in_data_pid = True
            self.depth = 1
            self.current = []
        elif self.in_data_pid:
            self.depth += 1

    def handle_endtag(self, tag):
        if not self.in_data_pid:
            return
        self.depth -= 1
        if self.depth == 0:
            text = normalize_spaces("".join(self.current))
            if text:
                self.items.append(text)
            self.in_data_pid = False

    def handle_data(self, data):
        if self.in_data_pid:
            self.current.append(data)


class WolPublicationLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attrs = dict(attrs)
        href = attrs.get("href", "")
        if "/wol/d/" in href:
            self.links.append(href)


def fetch_week_program(week_start, timeout=15):
    year, week_number, _ = week_start.isocalendar()
    urls = [
        f"https://wol.jw.org/es/wol/dt/r4/lp-s/{week_start.year}/{week_start.month}/{week_start.day}",
        f"https://wol.jw.org/es/wol/meetings/r4/lp-s/{year}/{week_number}",
    ]

    last_error = default_program(urls[-1], "No se pudo obtener el programa.")
    for url in urls:
        content = fetch_url(url, timeout)
        if isinstance(content, dict):
            last_error = content
            continue

        program = parse_program_html(content, url)
        if program["ok"]:
            return program

        detail_url = find_detail_url(content, url)
        if detail_url:
            detail_content = fetch_url(detail_url, timeout)
            if not isinstance(detail_content, dict):
                detail_program = parse_program_html(detail_content, detail_url)
                if detail_program["ok"]:
                    return detail_program

    return last_error


def fetch_url(url, timeout):
    last_error = ""
    for _ in range(2):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept-Language": "es",
                },
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if response.status != 200:
                    return default_program(url, f"HTTP {response.status}")
                return response.read().decode("utf-8", errors="ignore")
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = str(error)
    return default_program(url, last_error)


def find_detail_url(content, base_url):
    parser = WolPublicationLinkParser()
    parser.feed(content)
    candidates = list(parser.links)
    candidates += re.findall(r"https?://wol\.jw\.org/es/wol/d/r4/lp-s/\d+", content)
    candidates += re.findall(r"/es/wol/d/r4/lp-s/\d+", content)
    candidates += re.findall(r"/wol/d/r4/lp-s/\d+", content)
    if not candidates:
        return None
    return urljoin(base_url, candidates[0])


def parse_program_html(content, url=""):
    parser = WolDataPidParser()
    parser.feed(content)
    text_items = [unescape(item) for item in parser.items]
    if not text_items:
        text_items = [normalize_spaces(strip_tags(content))]
    school_assignments = extract_school_assignments(text_items)
    life_assignments = extract_life_assignments(text_items)
    return {
        "ok": bool(school_assignments or any(life_assignments.values())),
        "url": url,
        "error": "" if school_assignments or any(life_assignments.values()) else "No se detectaron asignaciones del programa.",
        "school_assignments": school_assignments,
        "life_assignments": life_assignments,
    }


def extract_school_assignments(text_items):
    section_items = section_between(text_items, "SEAMOS MEJORES MAESTROS", "NUESTRA VIDA CRISTIANA")
    if not section_items:
        section_items = text_items
    assignments = []
    seen_labels = set()
    for item in split_numbered_parts(section_items):
        label = classify_school_part(item)
        if not label or label in seen_labels:
            continue
        assignments.append(label)
        seen_labels.add(label)
    if assignments:
        return assignments[:4]

    normalized = normalize_for_matching("\n".join(section_items))
    matches = []
    for label in SCHOOL_ASSIGNMENT_LABELS:
        pattern = normalize_for_matching(label)
        for match in re.finditer(re.escape(pattern), normalized):
            matches.append((match.start(), label))
    for _, label in sorted(matches, key=lambda item: item[0]):
        if label in seen_labels:
            continue
        assignments.append(label)
        seen_labels.add(label)
    return assignments[:4]


def classify_school_part(text):
    normalized = normalize_for_matching(text)
    for label in SCHOOL_ASSIGNMENT_LABELS:
        if normalize_for_matching(label) in normalized:
            return label
    if "analisis con el auditorio" in normalized:
        return "Análisis con el auditorio"
    if "discurso" in normalized:
        return "Discurso estudiantil"
    return None


def extract_life_assignments(text_items):
    section_items = section_after(text_items, "NUESTRA VIDA CRISTIANA")
    life = {"random_1": False, "random_2": False, "needs": False}
    random_count = 0
    for item in split_numbered_parts(section_items):
        normalized = normalize_for_matching(item)
        if is_section_title(normalized) and "nuestra vida cristiana" not in normalized:
            break
        if "necesidades" in normalized:
            life["needs"] = True
            continue
        if "asignacion 1" in normalized:
            life["random_1"] = True
            continue
        if "asignacion 2" in normalized:
            life["random_2"] = True
            continue
        if should_count_life_assignment(normalized):
            random_count += 1
            if random_count == 1:
                life["random_1"] = True
            elif random_count == 2:
                life["random_2"] = True
    return life


def split_numbered_parts(text_items):
    text = "\n".join(text_items)
    parts = re.split(r"(?=\b\d+\.\s)", text)
    parts = [normalize_spaces(part) for part in parts if normalize_spaces(part)]
    if len(parts) <= 1 and len(text_items) > 1:
        return text_items
    return parts or text_items


def section_between(text_items, start_title, end_title):
    in_section = False
    items = []
    start = normalize_for_matching(start_title)
    end = normalize_for_matching(end_title)
    for item in text_items:
        normalized = normalize_for_matching(item)
        if start in normalized:
            in_section = True
            continue
        if in_section and end in normalized:
            break
        if in_section:
            items.append(item)
    return items


def section_after(text_items, start_title):
    in_section = False
    items = []
    start = normalize_for_matching(start_title)
    for item in text_items:
        normalized = normalize_for_matching(item)
        if start in normalized:
            in_section = True
            continue
        if in_section:
            items.append(item)
    return items


def should_count_life_assignment(normalized):
    ignored = [
        "cancion",
        "estudio biblico de la congregacion",
        "palabras de conclusion",
        "comentarios de conclusion",
        "oracion",
    ]
    if any(text in normalized for text in ignored):
        return False
    return bool(re.search(r"\b\d+\s*mins?\.?:", normalized)) or bool(re.search(r"\b\d+\.", normalized))


def is_section_title(normalized):
    return normalized in [
        "tesoros de la biblia",
        "seamos mejores maestros",
        "nuestra vida cristiana",
    ]


def normalize_spaces(text):
    return re.sub(r"\s+", " ", text).strip()


def strip_tags(content):
    return re.sub(r"<[^>]+>", " ", content)


def normalize_for_matching(text):
    text = text.lower()
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return normalize_spaces(text)


def default_program(url, error):
    return {
        "ok": False,
        "url": url,
        "error": error,
        "school_assignments": [],
        "life_assignments": {"random_1": True, "random_2": False, "needs": False},
    }
