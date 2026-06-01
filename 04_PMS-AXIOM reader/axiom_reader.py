"""
PMS-AXIOM Reader — local navigation and inspection tool.

 Δ ∇ □ Λ Α Ω Θ Φ Χ Σ Ψ

A single-file, dependency-free desktop reader for the PMS-AXIOM Markdown/YAML corpus.

Features:
- Loads the PMS-AXIOM repository from a folder or from a .zip file.
- Shows a project file navigator for README, source, paper blocks, Markdown case artefacts, YAML case artefacts, model/index files, and reference material.
- Shows a heading navigator for the current Markdown document.
- Renders Markdown and YAML-like text into a styled Tk text view without external packages.
- Provides corpus-wide full-text search with jump-to-result behavior.
- Highlights search matches in the current document.

Boundary:
    The Reader is a convenience tool for local navigation and inspection.
    It does not replace canonical Markdown/YAML, modify PMS-AXIOM, validate PMS Base,
    validate case findings, certify QC workflows, assign person findings, or create
    governance authority.

Run:
    python axiom_reader.py
    python axiom_reader.py /path/to/PMS-AXIOM
    python axiom_reader.py /path/to/PMS-AXIOM.zip

Note:
    Tkinter is part of Python's standard library, but some Linux distributions
    package it separately as python3-tk.
"""

from __future__ import annotations

import queue
import re
import sys
import threading
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    import tkinter.font as tkfont
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Tkinter is not available. Install the Tk bindings for your Python "
        "distribution, for example: sudo apt install python3-tk"
    ) from exc

APP_TITLE = "PMS-AXIOM Reader"
APP_VERSION = "0.4.0"

DEBUG = False  # set True to show console diagnostics


def dbg(msg: str) -> None:
    if DEBUG:
        ts = time.strftime("%H:%M:%S")
        print(f"[{ts}] {msg}", flush=True)


SUPPORTED_TEXT_SUFFIXES: Tuple[str, ...] = (".md", ".yaml", ".yml", ".py", ".txt")

PREFERRED_FILES: List[str] = [
    "README.md",

    "00_source/PMS-AXIOM_Rebuild_To_Do.md",
    "00_source/PMS-AXIOM_legacy_full.md",

    "01_blocks/01_orientation_methodology.md",
    "01_blocks/02_part_i_pms_core.md",
    "01_blocks/03_part_ii_pms_logic.md",
    "01_blocks/04_part_iii_pms_anticipation.md",
    "01_blocks/05_part_iv_pms_conflict.md",
    "01_blocks/06_part_v_pms_critique.md",
    "01_blocks/07_part_vi_pms_eden.md",
    "01_blocks/08_part_vii_pms_sex.md",
    "01_blocks/09_part_viii_pms_qc.md",
    "01_blocks/10_boundary_governance_non_mixing.md",
    "01_blocks/11_conclusion.md",

    "03_model/PMS-AXIOM_Case_Index.yaml",
    "03_model/PMS-AXIOM_Case_Schema.yaml",
]

SECTION_LABELS: Dict[str, str] = {
    "README.md": "Start",
    "00_source": "Source",
    "01_blocks": "Blocks",
    "02_cases": "Cases",
    "02_cases/markdown": "Markdown Case Artefacts",
    "02_cases/markdown case prompts": "Markdown Case Prompts",
    "02_cases/yaml": "YAML Case Artefacts",
    "02_cases/yaml case templates": "YAML Case Templates",
    "03_model": "Model / Index",
    "04_reference": "Reference",
    
}

IGNORED_REL_PATHS: set[str] = set()
IGNORED_PREFIXES: Tuple[str, ...] = ("04_PMS-AXIOM reader/", "04_PMS-AXIOM Reader/")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9_-]+)?(?:\s+.*)?\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+])\s+(.+?)\s*$")
ORDERED_LIST_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.+?)\s*$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)

# Large Markdown files are cheap to load into RAM but expensive to render
# line-by-line into a Tk Text widget. Above this threshold, use fast plain
# rendering: one insert(), no per-line marks, no per-line tags.
LARGE_DOC_LINE_THRESHOLD = 8000


PART_LABELS: Dict[str, str] = {
    "04": "Part I — PMS Core",
    "05": "Part II — PMS + LOGIC",
    "06": "Part III — PMS + ANTICIPATION",
    "07": "Part IV — PMS + CONFLICT",
    "08": "Part V — PMS + CRITIQUE",
    "09": "Part VI — PMS + EDEN",
    "10": "Part VII — PMS + SEX",
    "11": "Part VIII — PMS + QC / QC-EXT",
}

BLOCK_BY_PART: Dict[str, str] = {
    "04": "01_blocks/02_part_i_pms_core.md",
    "05": "01_blocks/03_part_ii_pms_logic.md",
    "06": "01_blocks/04_part_iii_pms_anticipation.md",
    "07": "01_blocks/05_part_iv_pms_conflict.md",
    "08": "01_blocks/06_part_v_pms_critique.md",
    "09": "01_blocks/07_part_vi_pms_eden.md",
    "10": "01_blocks/08_part_vii_pms_sex.md",
    "11": "01_blocks/09_part_viii_pms_qc.md",
}

ADDON_PREFIX_BY_PART: Dict[str, str] = {
    "05": "PMS_LOGIC",
    "06": "PMS_ANTICIPATION",
    "07": "PMS_CONFLICT",
    "08": "PMS_CRITIQUE",
    "09": "PMS_EDEN",
    "10": "PMS_SEX",
    "11": "PMS_QC",
}

QC_EXT_PREFIX = "PMS_QC_EXT"
CASE_ID_RE = re.compile(r"(\d{2})_4_(\d{1,2})")
YAML_CASE_RE = re.compile(r"^(?P<prefix>.+?)_(?P<case>\d{2}_4_\d{1,2})\.ya?ml$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Heading:
    level: int
    text: str
    line_number: int
    anchor: str


@dataclass
class Document:
    rel_path: str
    title: str
    text: str
    headings: List[Heading] = field(default_factory=list)
    frontmatter: Dict[str, str] = field(default_factory=dict)

    @property
    def line_count(self) -> int:
        return len(self.text.splitlines())

    @property
    def word_count(self) -> int:
        return len(WORD_RE.findall(self.text))


class CorpusError(RuntimeError):
    """Raised when a PMS-AXIOM corpus cannot be loaded."""


# ---------------------------------------------------------------------------
# Corpus source (folder or zip)
# ---------------------------------------------------------------------------

class CorpusSource:
    """Reads PMS-AXIOM text artefacts from either a folder or a zip file."""

    def __init__(self, source_path: Path):
        self.source_path = source_path.expanduser().resolve()
        dbg(f"CorpusSource: resolving {self.source_path}")
        self.kind: str = "folder" if self.source_path.is_dir() else "zip"
        self._zip: Optional[zipfile.ZipFile] = None
        self._zip_prefix = ""
        self.root_dir: Optional[Path] = None

        if self.source_path.is_dir():
            self.root_dir = self._detect_folder_root(self.source_path)
            dbg(f"CorpusSource: folder root = {self.root_dir}")
        elif self.source_path.is_file() and self.source_path.suffix.lower() == ".zip":
            self._zip = zipfile.ZipFile(self.source_path)
            self._zip_prefix = self._detect_zip_prefix(self._zip)
            dbg(f"CorpusSource: zip prefix = '{self._zip_prefix}'")
        else:
            raise CorpusError(f"Unsupported source: {self.source_path}")

    def close(self) -> None:
        if self._zip is not None:
            self._zip.close()

    def describe(self) -> str:
        if self.kind == "folder" and self.root_dir is not None:
            return str(self.root_dir)
        return str(self.source_path)

    def exists(self, rel_path: str) -> bool:
        rel_path = normalize_rel_path(rel_path)
        if rel_path in IGNORED_REL_PATHS:
            return False
        if self.kind == "folder":
            assert self.root_dir is not None
            return (self.root_dir / rel_path).is_file()
        assert self._zip is not None
        return self._zip_name(rel_path) in self._zip.namelist()

    def read_text(self, rel_path: str) -> str:
        rel_path = normalize_rel_path(rel_path)
        if self.kind == "folder":
            assert self.root_dir is not None
            return (self.root_dir / rel_path).read_text(encoding="utf-8")
        assert self._zip is not None
        with self._zip.open(self._zip_name(rel_path), "r") as handle:
            raw = handle.read()
        return raw.decode("utf-8")

    def available_files(self) -> List[str]:
        """Return all readable PMS-AXIOM text artefacts in stable project order."""
        found = [rel for rel in self._all_text_rel_paths() if rel not in IGNORED_REL_PATHS]
        preferred = [rel for rel in PREFERRED_FILES if rel in found]
        remaining = [rel for rel in found if rel not in set(preferred)]
        result = preferred + sorted(remaining, key=sort_rel_path)
        dbg(f"CorpusSource.available_files: {len(result)} readable file(s) found")
        return result

    def _zip_name(self, rel_path: str) -> str:
        rel_path = normalize_rel_path(rel_path)
        return f"{self._zip_prefix}{rel_path}" if self._zip_prefix else rel_path

    def _all_text_rel_paths(self) -> List[str]:
        if self.kind == "folder":
            assert self.root_dir is not None
            rels: List[str] = []
            for path in self.root_dir.rglob("*"):
                if not path.is_file():
                    continue
                if path.name.startswith("."):
                    continue
                if path.suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
                    continue
                rel = path.relative_to(self.root_dir).as_posix()
                if any(rel.startswith(prefix) for prefix in IGNORED_PREFIXES):
                    continue
                rels.append(rel)
            return rels

        assert self._zip is not None
        rels = []
        for name in self._zip.namelist():
            if name.endswith("/"):
                continue
            if self._zip_prefix and not name.startswith(self._zip_prefix):
                continue
            rel = name[len(self._zip_prefix):] if self._zip_prefix else name
            rel = normalize_rel_path(rel)
            if any(rel.startswith(prefix) for prefix in IGNORED_PREFIXES):
                continue
            if not rel or Path(rel).name.startswith("."):
                continue
            if Path(rel).suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
                continue
            rels.append(rel)
        return rels

    @staticmethod
    def _detect_folder_root(path: Path) -> Path:
        candidates = [path, path / "PMS-AXIOM"]
        for candidate in candidates:
            has_readme = (candidate / "README.md").is_file()
            has_blocks = (candidate / "01_blocks").is_dir()
            has_cases = (candidate / "02_cases").is_dir()
            has_model = (candidate / "03_model").is_dir()
            dbg(
                f"  _detect_folder_root: {candidate}  "
                f"readme={has_readme} blocks={has_blocks} cases={has_cases} model={has_model}"
            )
            if has_readme and has_blocks and has_cases:
                return candidate
        raise CorpusError(
            "Could not find a PMS-AXIOM project root. "
            "Select the folder that contains README.md, 01_blocks/, and 02_cases/."
        )

    @staticmethod
    def _detect_zip_prefix(zf: zipfile.ZipFile) -> str:
        names = set(zf.namelist())

        def has_project(prefix: str) -> bool:
            has_readme = f"{prefix}README.md" in names
            has_blocks = any(name.startswith(f"{prefix}01_blocks/") for name in names)
            has_cases = any(name.startswith(f"{prefix}02_cases/") for name in names)
            return has_readme and has_blocks and has_cases

        if has_project(""):
            return ""

        prefixes = set()
        for name in names:
            parts = name.split("/")
            if len(parts) > 1 and parts[0]:
                prefixes.add(parts[0] + "/")

        for prefix in sorted(prefixes):
            if has_project(prefix):
                return prefix

        raise CorpusError(
            "Could not find a PMS-AXIOM project root inside the zip file. "
            "Expected README.md, 01_blocks/, and 02_cases/."
        )


# ---------------------------------------------------------------------------
# Corpus (collection of loaded documents)
# ---------------------------------------------------------------------------

class Corpus:
    """Loaded PMS-AXIOM documents plus lightweight search helpers."""

    def __init__(self, source: CorpusSource):
        self.source = source
        self.documents: Dict[str, Document] = {}
        self.ordered_paths: List[str] = []
        self.load()

    def load(self) -> None:
        self.documents.clear()
        self.ordered_paths = self.source.available_files()
        dbg(f"Corpus.load: loading {len(self.ordered_paths)} documents ...")
        for rel_path in self.ordered_paths:
            dbg(f"  reading {rel_path}")
            text = self.source.read_text(rel_path)
            frontmatter, body = parse_frontmatter(text)
            headings = parse_headings(body)
            title = (
                frontmatter.get("title")
                or first_heading_title(headings)
                or prettify_file_name(rel_path)
            )
            self.documents[rel_path] = Document(
                rel_path=rel_path,
                title=title,
                text=text,
                headings=parse_headings(strip_frontmatter(text)),
                frontmatter=frontmatter,
            )
        dbg(f"Corpus.load: done — {len(self.documents)} documents loaded")

    def get(self, rel_path: str) -> Document:
        return self.documents[rel_path]

    def search(self, query: str, limit: int = 500) -> List[Tuple[str, int, str]]:
        query_norm = query.strip().lower()
        if not query_norm:
            return []
        results: List[Tuple[str, int, str]] = []
        for rel_path in self.ordered_paths:
            doc = self.documents[rel_path]
            for line_no, line in enumerate(strip_frontmatter(doc.text).splitlines(), start=1):
                if query_norm in line.lower():
                    snippet = line.strip() or "<blank line>"
                    results.append((rel_path, line_no, snippet[:300]))
                    if len(results) >= limit:
                        return results
        return results

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def total_word_count(self) -> int:
        return sum(doc.word_count for doc in self.documents.values())

    @property
    def total_line_count(self) -> int:
        return sum(doc.line_count for doc in self.documents.values())


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class PmsAxiomReaderApp(tk.Tk):
    """Tkinter desktop app for browsing the PMS-AXIOM corpus."""

    def __init__(self, initial_source: Optional[Path] = None):
        super().__init__()
        dbg("App: __init__ start")
        self.title(f"{APP_TITLE} {APP_VERSION}")
        self.geometry("1380x860")
        self.minsize(960, 600)

        # Ignore SIGINT so Ctrl+C in the console cannot interrupt Tk callbacks.
        import signal
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        self.corpus: Optional[Corpus] = None
        self.current_path: Optional[str] = None
        self.current_case_id: Optional[str] = None
        self.current_case_view: Optional[str] = None
        self._case_button_widgets: List[ttk.Button] = []
        self.heading_indices: Dict[str, str] = {}
        self.search_results: List[Tuple[str, int, str]] = []
        self._file_item_to_path: Dict[str, str] = {}
        self._case_block_tree_path_by_case: Dict[str, str] = {}
        self._virtual_block_section_paths: Dict[str, str] = {}
        self._heading_item_to_anchor: Dict[str, str] = {}
        self._search_entry: Optional[ttk.Entry] = None
        self.dark_mode = False

        self.reader_font_size = 10
        self.reader_fullscreen = False
        self._normal_geometry = ""

        # Guard against recursive Treeview callbacks:
        # programmatic selection_set() also emits <<TreeviewSelect>>.
        self._suppress_file_select_event = False

        # Queue for results coming back from the background loader thread.
        self._load_queue: queue.Queue = queue.Queue()

        self._configure_style()
        self._build_ui()
        self._bind_shortcuts()
        self.apply_theme()
        self._center_window()

        dbg("App: UI built, scheduling background load")

        # Kick off corpus loading in a background thread after the window paints.
        if initial_source is not None:
            self.after(100, lambda: self._start_load_thread(initial_source))
        else:
            self.after(100, self._start_discover_thread)

        dbg("App: __init__ done")

    # ------------------------------------------------------------------ #
    # Background loading — worker thread, NO Tk calls allowed here       #
    # ------------------------------------------------------------------ #

    def _start_discover_thread(self) -> None:
        dbg("App: starting discover thread")
        self.status_var.set("Searching for PMS-AXIOM corpus ...")
        t = threading.Thread(target=self._bg_discover, daemon=True)
        t.start()
        self.after(100, self._poll_load_queue)

    def _start_load_thread(self, source_path: Path) -> None:
        dbg(f"App: starting load thread for {source_path}")
        self.status_var.set(f"Loading corpus from {source_path} ...")
        t = threading.Thread(target=self._bg_load, args=(source_path,), daemon=True)
        t.start()
        self.after(100, self._poll_load_queue)

    def _bg_discover(self) -> None:
        """Runs in background thread: discover source path, then load."""
        try:
            dbg("bg_discover: searching ...")
            source_path = discover_default_source()
            if source_path is None:
                dbg("bg_discover: no source found")
                self._load_queue.put(("no_source", None))
                return
            dbg(f"bg_discover: found {source_path}, loading ...")
            self._bg_load(source_path)
        except Exception as exc:
            dbg(f"bg_discover: exception: {exc}")
            self._load_queue.put(("error", str(exc)))

    def _bg_load(self, source_path: Path) -> None:
        """Runs in background thread: create CorpusSource + Corpus."""
        try:
            dbg(f"bg_load: creating CorpusSource({source_path})")
            source = CorpusSource(source_path)
            dbg("bg_load: creating Corpus")
            corpus = Corpus(source)
            dbg("bg_load: done, posting result to queue")
            self._load_queue.put(("ok", corpus))
        except Exception as exc:
            dbg(f"bg_load: exception: {exc}")
            self._load_queue.put(("error", str(exc)))

    def _poll_load_queue(self) -> None:
        """Called periodically in the Tk thread to receive background results."""
        try:
            msg, payload = self._load_queue.get_nowait()
        except queue.Empty:
            # Nothing yet — reschedule.
            self.after(100, self._poll_load_queue)
            return

        dbg(f"poll_load_queue: received '{msg}'")

        if msg == "ok":
            corpus: Corpus = payload
            if self.corpus is not None:
                self.corpus.source.close()
            self.corpus = corpus
            self.current_path = None
            self.populate_file_tree()
            self.clear_search()
            self.status_var.set(
                f"Loaded {corpus.document_count} documents, "
                f"{corpus.total_line_count:,} lines, "
                f"{corpus.total_word_count:,} words — {corpus.source.describe()}"
            )
            self.open_home()

        elif msg == "no_source":
            self.status_var.set("Open a PMS-AXIOM folder or zip file to begin.")

        elif msg == "error":
            error_msg: str = payload
            self.status_var.set(f"Error: {error_msg}")
            messagebox.showerror(APP_TITLE, error_msg)

        else:
            dbg(f"poll_load_queue: unknown message '{msg}'")

    # ------------------------------------------------------------------ #
    # Style / UI construction                                            #
    # ------------------------------------------------------------------ #

    def _configure_style(self) -> None:
        self.base_font = tkfont.Font(family="Segoe UI", size=10)
        self.bold_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.italic_font = tkfont.Font(family="Segoe UI", size=10, slant="italic")
        self.bold_italic_font = tkfont.Font(family="Segoe UI", size=10, weight="bold", slant="italic")
        self.mono_font = tkfont.Font(family="Consolas", size=10)
        self.heading_font_1 = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.heading_font_2 = tkfont.Font(family="Segoe UI", size=15, weight="bold")
        self.heading_font_3 = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.heading_font_4 = tkfont.Font(family="Segoe UI", size=11, weight="bold")

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=24)
        style.configure("TButton", padding=(8, 4))
        style.configure("ActiveView.TButton", padding=(8, 4))
        style.configure("TEntry", padding=(4, 4))

    def _build_ui(self) -> None:
        self._build_toolbar()
        self._build_fullscreen_toolbar()

        self.main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        self.left_pane = ttk.PanedWindow(self.main_pane, orient=tk.VERTICAL)
        self.main_pane.add(self.left_pane, weight=1)

        # File tree
        file_frame = ttk.Frame(self.left_pane, padding=(6, 6, 6, 3))
        self.left_pane.add(file_frame, weight=3)
        ttk.Label(file_frame, text="Corpus", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)

        file_tree_wrap = ttk.Frame(file_frame)
        file_tree_wrap.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        file_tree_wrap.columnconfigure(0, weight=1)
        file_tree_wrap.columnconfigure(1, weight=0, minsize=18)
        file_tree_wrap.rowconfigure(0, weight=1)

        self.file_tree = ttk.Treeview(file_tree_wrap, show="tree")
        self.file_tree.grid(row=0, column=0, sticky="nsew")

        file_scrollbar = ttk.Scrollbar(file_tree_wrap, orient=tk.VERTICAL, command=self.file_tree.yview)
        file_scrollbar.grid(row=0, column=1, sticky="ns")
        self.file_tree.configure(yscrollcommand=file_scrollbar.set)

        self.file_tree.bind("<<TreeviewSelect>>", self._on_file_selected)
        self._bind_mousewheel_scroll(self.file_tree)

        # Search results
        search_frame = ttk.Frame(self.left_pane, padding=(6, 3, 6, 6))
        self.left_pane.add(search_frame, weight=2)
        ttk.Label(search_frame, text="Search Results", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)

        search_tree_wrap = ttk.Frame(search_frame)
        search_tree_wrap.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        self.search_tree = ttk.Treeview(
            search_tree_wrap,
            show="headings",
            columns=("file", "line", "text"),
            height=9,
        )
        self.search_tree.heading("file", text="File")
        self.search_tree.heading("line", text="Line")
        self.search_tree.heading("text", text="Text")
        self.search_tree.column("file", width=130, stretch=False)
        self.search_tree.column("line", width=48, stretch=False, anchor=tk.E)
        self.search_tree.column("text", width=260, stretch=True)
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        search_scrollbar = ttk.Scrollbar(search_tree_wrap, orient=tk.VERTICAL, command=self.search_tree.yview)
        search_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_tree.configure(yscrollcommand=search_scrollbar.set)

        self.search_tree.bind("<Double-1>", self._on_search_result_open)
        self.search_tree.bind("<Return>", self._on_search_result_open)
        self._bind_mousewheel_scroll(self.search_tree)

        # Heading tree
        self.heading_frame = ttk.Frame(self.main_pane, padding=(6, 6, 6, 6))
        self.main_pane.add(self.heading_frame, weight=1)
        ttk.Label(self.heading_frame, text="Headings", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)

        heading_tree_wrap = ttk.Frame(self.heading_frame)
        heading_tree_wrap.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        heading_tree_wrap.columnconfigure(0, weight=1)
        heading_tree_wrap.columnconfigure(1, weight=0, minsize=18)
        heading_tree_wrap.rowconfigure(0, weight=1)

        self.heading_tree = ttk.Treeview(heading_tree_wrap, show="tree")
        self.heading_tree.grid(row=0, column=0, sticky="nsew")

        heading_scrollbar = ttk.Scrollbar(heading_tree_wrap, orient=tk.VERTICAL, command=self.heading_tree.yview)
        heading_scrollbar.grid(row=0, column=1, sticky="ns")
        self.heading_tree.configure(yscrollcommand=heading_scrollbar.set)

        self.heading_tree.bind("<<TreeviewSelect>>", self._on_heading_selected)
        self._bind_mousewheel_scroll(self.heading_tree)

        # Document content
        self.content_frame = ttk.Frame(self.main_pane, padding=(6, 6, 6, 6))
        self.main_pane.add(self.content_frame, weight=4)

        self.document_label_var = tk.StringVar(value="No document loaded")
        self.document_label = ttk.Label(
            self.content_frame,
            textvariable=self.document_label_var,
            font=("Segoe UI", 11, "bold"),
        )
        self.document_label.pack(anchor=tk.W, padx=(2, 0), pady=(0, 4))

        self.case_switch_frame = ttk.Frame(self.content_frame)
        self.case_switch_frame.pack(fill=tk.X, padx=(2, 0), pady=(0, 6))
        self.case_switch_label = ttk.Label(self.case_switch_frame, text="Switch view:", font=("Segoe UI", 9, "bold"))
        self.case_switch_label.pack(side=tk.LEFT, padx=(0, 6))
        self.case_switch_empty = ttk.Label(self.case_switch_frame, text="Select a case artefact to enable case views.")
        self.case_switch_empty.pack(side=tk.LEFT)

        # Reader border: same visual discipline as the side panes.
        self.reader_border = tk.Frame(
            self.content_frame,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#cfcfcf",
            highlightcolor="#cfcfcf",
        )
        self.reader_border.pack(fill=tk.BOTH, expand=True)

        text_wrap = ttk.Frame(self.reader_border)
        text_wrap.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(
            text_wrap,
            wrap=tk.WORD,
            undo=False,
            padx=18,
            pady=14,
            font=self.base_font,
            borderwidth=0,
            highlightthickness=0,
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        yscroll = ttk.Scrollbar(text_wrap, orient=tk.VERTICAL, command=self.text.yview)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=yscroll.set)

        self._configure_text_tags()

        self.status_var = tk.StringVar(value="Starting ...")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor=tk.W, padding=(6, 3))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def _build_toolbar(self) -> None:
        self.toolbar = ttk.Frame(self, padding=(6, 6, 6, 3))
        self.toolbar.pack(fill=tk.X)

        ttk.Button(self.toolbar, text="Open Folder", command=self._open_folder).pack(side=tk.LEFT)
        ttk.Button(self.toolbar, text="Open ZIP", command=self._open_zip).pack(side=tk.LEFT, padx=(6, 10))

        ttk.Label(self.toolbar, text="Search").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self._search_entry = ttk.Entry(self.toolbar, textvariable=self.search_var, width=42)
        self._search_entry.pack(side=tk.LEFT, padx=(6, 4))
        self._search_entry.bind("<Return>", lambda event: self.run_search())
        ttk.Button(self.toolbar, text="Run", command=self.run_search).pack(side=tk.LEFT)
        ttk.Button(self.toolbar, text="Clear", command=self.clear_search).pack(side=tk.LEFT, padx=(4, 12))

        ttk.Button(self.toolbar, text="Reload", command=self.reload_source).pack(side=tk.LEFT)
        ttk.Button(self.toolbar, text="Home", command=self.open_home).pack(side=tk.LEFT, padx=(6, 12))

        ttk.Button(self.toolbar, text="A−", command=self.decrease_reader_font).pack(side=tk.LEFT)
        ttk.Button(self.toolbar, text="A+", command=self.increase_reader_font).pack(side=tk.LEFT, padx=(4, 12))

        self.fullscreen_button = ttk.Button(
            self.toolbar,
            text="Reader Fullscreen",
            command=self.toggle_reader_fullscreen,
        )
        self.fullscreen_button.pack(side=tk.LEFT, padx=(0, 12))

        self.theme_button = ttk.Button(self.toolbar, text="Dark Mode", command=self.toggle_dark_mode)
        self.theme_button.pack(side=tk.LEFT)

        ttk.Button(self.toolbar, text="Exit", command=self.destroy).pack(side=tk.RIGHT)
        ttk.Button(self.toolbar, text="Help", command=self.show_help).pack(side=tk.RIGHT, padx=(0, 6))

    def _build_fullscreen_toolbar(self) -> None:
        self.fullscreen_toolbar = ttk.Frame(self, padding=(8, 6, 8, 4))

        ttk.Button(
            self.fullscreen_toolbar,
            text="A−",
            command=self.decrease_reader_font,
        ).pack(side=tk.LEFT)

        ttk.Button(
            self.fullscreen_toolbar,
            text="A+",
            command=self.increase_reader_font,
        ).pack(side=tk.LEFT, padx=(4, 12))

        ttk.Label(
            self.fullscreen_toolbar,
            text="Reader Fullscreen",
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.LEFT)

        ttk.Button(
            self.fullscreen_toolbar,
            text="Exit Fullscreen",
            command=self.exit_reader_fullscreen,
        ).pack(side=tk.RIGHT)

        ttk.Button(
            self.fullscreen_toolbar,
            text="Help",
            command=self.show_help,
        ).pack(side=tk.RIGHT, padx=(0, 6))

    def _configure_text_tags(self) -> None:
        self.text.tag_configure("h1", font=self.heading_font_1, spacing1=22, spacing3=12, lmargin1=14, lmargin2=14)
        self.text.tag_configure("h2", font=self.heading_font_2, spacing1=20, spacing3=10, lmargin1=14, lmargin2=14)
        self.text.tag_configure("h3", font=self.heading_font_3, spacing1=16, spacing3=8, lmargin1=14, lmargin2=14)
        self.text.tag_configure("h4", font=self.heading_font_4, spacing1=14, spacing3=7, lmargin1=14, lmargin2=14)
        self.text.tag_configure("h5", font=self.heading_font_4, spacing1=12, spacing3=6, lmargin1=14, lmargin2=14)
        self.text.tag_configure("h6", font=self.heading_font_4, spacing1=12, spacing3=6, lmargin1=14, lmargin2=14)

        self.text.tag_configure("body", font=self.base_font, lmargin1=8, lmargin2=8)
        self.text.tag_configure("bold", font=self.bold_font)
        self.text.tag_configure("italic", font=self.italic_font)
        self.text.tag_configure("bold_italic", font=self.bold_italic_font)
        self.text.tag_configure("list", font=self.base_font, lmargin1=28, lmargin2=46, spacing1=1, spacing3=1)
        self.text.tag_configure("code", font=self.mono_font, background="#f4f4f4", lmargin1=28, lmargin2=28, spacing1=8, spacing3=8)
        self.text.tag_configure("inline_code", font=self.mono_font, background="#f4f4f4")
        self.text.tag_configure("yaml_key", font=self.mono_font, background="#f4f4f4", foreground="#7a3e9d", lmargin1=28, lmargin2=28)
        self.text.tag_configure("yaml_value", font=self.mono_font, background="#f4f4f4", foreground="#555555", lmargin1=28, lmargin2=28)
        self.text.tag_configure("quote", lmargin1=24, lmargin2=24, foreground="#555555")
        self.text.tag_configure("table", font=self.mono_font, lmargin1=24, lmargin2=24, spacing1=4, spacing3=4)
        self.text.tag_configure("rule", foreground="#777777")
        self.text.tag_configure("search", background="#fff2a8")
        self.text.tag_configure("current_line", background="#eef5ff")

    def toggle_dark_mode(self) -> None:
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self) -> None:
        if self.dark_mode:
            bg = "#1e1e1e"
            panel_bg = "#252526"
            fg = "#d4d4d4"
            muted_fg = "#a0a0a0"
            text_bg = "#1e1e1e"
            text_fg = "#d4d4d4"
            code_bg = "#2d2d2d"
            button_bg = "#333333"
            button_hover_bg = "#404040"
            selection_bg = "#3a3d41"
            current_line_bg = "#2a2d2e"
            search_bg = "#665c00"
            rule_fg = "#777777"
            yaml_key_fg = "#ce9178"
            yaml_value_fg = "#b5cea8"
            reader_border_fg = "#3a3d41"
            self.theme_button.configure(text="Light Mode")
        else:
            bg = "#f0f0f0"
            panel_bg = "#ffffff"
            fg = "#000000"
            muted_fg = "#555555"
            text_bg = "#ffffff"
            text_fg = "#000000"
            code_bg = "#f4f4f4"
            button_bg = "#f0f0f0"
            button_hover_bg = "#e5e5e5"
            selection_bg = "#cde8ff"
            current_line_bg = "#eef5ff"
            search_bg = "#fff2a8"
            rule_fg = "#777777"
            yaml_key_fg = "#7a3e9d"
            yaml_value_fg = "#555555"
            reader_border_fg = "#cfcfcf"
            self.theme_button.configure(text="Dark Mode")

        self.configure(background=bg)

        style = ttk.Style(self)
        style.configure(".", background=bg, foreground=fg)
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TButton", background=button_bg, foreground=fg)
        style.map(
            "TButton",
            background=[
                ("active", button_hover_bg),
                ("pressed", selection_bg),
                ("!active", button_bg),
            ],
            foreground=[
                ("active", fg),
                ("pressed", fg),
                ("!active", fg),
            ],
        )
        style.configure("ActiveView.TButton", background=button_hover_bg, foreground=fg)
        style.map(
            "ActiveView.TButton",
            background=[
                ("active", button_hover_bg),
                ("pressed", button_hover_bg),
                ("!active", button_hover_bg),
            ],
            foreground=[
                ("active", fg),
                ("pressed", fg),
                ("!active", fg),
            ],
        )

        style.configure("TEntry", fieldbackground=text_bg, foreground=fg)
        style.configure(
            "Treeview",
            background=panel_bg,
            fieldbackground=panel_bg,
            foreground=fg,
        )
        style.map(
            "Treeview",
            background=[("selected", selection_bg)],
            foreground=[("selected", fg)],
        )

        if hasattr(self, "reader_border"):
            self.reader_border.configure(
                background=reader_border_fg,
                highlightbackground=reader_border_fg,
                highlightcolor=reader_border_fg,
            )

        self.text.configure(
            background=text_bg,
            foreground=text_fg,
            insertbackground=text_fg,
        )

        for tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.text.tag_configure(tag, background=text_bg, foreground=text_fg)

        self.text.tag_configure("body", background=text_bg, foreground=text_fg)
        self.text.tag_configure("bold", background=text_bg, foreground=text_fg)
        self.text.tag_configure("italic", background=text_bg, foreground=text_fg)
        self.text.tag_configure("bold_italic", background=text_bg, foreground=text_fg)
        self.text.tag_configure("list", background=text_bg, foreground=text_fg)
        self.text.tag_configure("code", background=code_bg, foreground=text_fg)
        self.text.tag_configure("inline_code", background=code_bg, foreground=text_fg)
        self.text.tag_configure("yaml_key", background=code_bg, foreground=yaml_key_fg)
        self.text.tag_configure("yaml_value", background=code_bg, foreground=yaml_value_fg)
        self.text.tag_configure("quote", background=text_bg, foreground=muted_fg)
        self.text.tag_configure("table", background=text_bg, foreground=text_fg)
        self.text.tag_configure("rule", background=text_bg, foreground=rule_fg)
        self.text.tag_configure("search", background=search_bg, foreground=text_fg)
        self.text.tag_configure("current_line", background=current_line_bg)

    def _bind_mousewheel_scroll(self, widget: tk.Widget) -> None:
        """Make mouse-wheel scrolling work reliably for Treeview-like widgets.

        Tk/ttk scrolling behavior differs between Windows, macOS, and Linux.
        Binding directly to each navigation tree keeps Corpus, Search Results,
        and Headings scrollable even before they have keyboard focus.
        """
        widget.bind("<MouseWheel>", lambda event, w=widget: self._on_mousewheel_scroll(event, w))
        widget.bind("<Button-4>", lambda event, w=widget: self._on_linux_mousewheel_scroll(event, w, -1))
        widget.bind("<Button-5>", lambda event, w=widget: self._on_linux_mousewheel_scroll(event, w, 1))

    def _on_mousewheel_scroll(self, event: tk.Event, widget: tk.Widget) -> str:
        delta = getattr(event, "delta", 0)

        if delta == 0:
            return "break"

        # Windows usually sends +/-120. macOS can send smaller values.
        if abs(delta) >= 120:
            units = -int(delta / 120)
        else:
            units = -1 if delta > 0 else 1

        try:
            widget.yview_scroll(units, "units")
        except tk.TclError:
            pass

        return "break"

    def _on_linux_mousewheel_scroll(self, event: tk.Event, widget: tk.Widget, units: int) -> str:
        try:
            widget.yview_scroll(units, "units")
        except tk.TclError:
            pass

        return "break"

    def _center_window(self) -> None:
        """Center the main window on the current screen after widgets exist."""
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            geometry = self.geometry().split("+", 1)[0]
            width_text, height_text = geometry.split("x", 1)
            width = int(width_text)
            height = int(height_text)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_help(self) -> None:
        messagebox.showinfo(
            f"{APP_TITLE} Help",
            "PMS-AXIOM Reader controls\n\n"
            "Navigation:\n"
            "  Open Folder / Open ZIP  Load a PMS-AXIOM corpus\n"
            "  Home                    Open README / orientation\n"
            "  Reload                  Reload the current corpus\n\n"
            "Search:\n"
            "  Ctrl+F                  Focus search field\n"
            "  Enter                   Run search from search field\n"
            "  Double-click result     Open search result\n\n"
            "Reader:\n"
            "  A+ / Ctrl++             Increase reader font size\n"
            "  A− / Ctrl+-             Decrease reader font size\n"
            "  Ctrl+0                  Reset reader font size\n"
            "  F11                     Toggle reader fullscreen\n"
            "  Esc                     Exit reader fullscreen\n\n"
            "Theme:\n"
            "  Dark Mode               Toggle light / dark mode\n\n"
            "Boundary:\n"
            "  The Reader navigates and inspects local PMS-AXIOM Markdown/YAML.\n"
            "  It does not validate PMS Base, create case findings, certify QC workflows,\n"
            "  evaluate persons, or modify canonical files.\n\n"
            "Fullscreen mode keeps only the reading area and a compact control bar visible.",
        )

    def increase_reader_font(self) -> None:
        self.set_reader_font_size(self.reader_font_size + 1)

    def decrease_reader_font(self) -> None:
        self.set_reader_font_size(self.reader_font_size - 1)

    def reset_reader_font(self) -> None:
        self.set_reader_font_size(10)

    def set_reader_font_size(self, size: int) -> None:
        self.reader_font_size = max(8, min(24, size))
        self._apply_reader_font_sizes()
        self.status_var.set(f"Reader font size: {self.reader_font_size}")

    def _apply_reader_font_sizes(self) -> None:
        size = self.reader_font_size

        self.base_font.configure(size=size)
        self.bold_font.configure(size=size)
        self.italic_font.configure(size=size)
        self.bold_italic_font.configure(size=size)
        self.mono_font.configure(size=size)

        self.heading_font_1.configure(size=size + 8)
        self.heading_font_2.configure(size=size + 5)
        self.heading_font_3.configure(size=size + 3)
        self.heading_font_4.configure(size=size + 1)

        self.text.configure(font=self.base_font)

    def toggle_reader_fullscreen(self) -> None:
        if self.reader_fullscreen:
            self.exit_reader_fullscreen()
        else:
            self.enter_reader_fullscreen()

    def enter_reader_fullscreen(self) -> None:
        if self.reader_fullscreen:
            return

        self.reader_fullscreen = True
        self._normal_geometry = self.geometry()

        self.toolbar.pack_forget()
        self.status_label.pack_forget()
        self.fullscreen_toolbar.pack(fill=tk.X, before=self.main_pane)

        try:
            self.main_pane.forget(self.left_pane)
        except tk.TclError:
            pass

        try:
            self.main_pane.forget(self.heading_frame)
        except tk.TclError:
            pass

        self.attributes("-fullscreen", True)
        self.fullscreen_button.configure(text="Exit Fullscreen")
        self.text.focus_set()

    def exit_reader_fullscreen(self) -> None:
        if not self.reader_fullscreen:
            return

        self.reader_fullscreen = False
        self.attributes("-fullscreen", False)

        self.fullscreen_toolbar.pack_forget()

        try:
            self.main_pane.forget(self.content_frame)
        except tk.TclError:
            pass

        self.main_pane.add(self.left_pane, weight=1)
        self.main_pane.add(self.heading_frame, weight=1)
        self.main_pane.add(self.content_frame, weight=4)

        self.toolbar.pack(fill=tk.X, before=self.main_pane)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

        if self._normal_geometry:
            self.geometry(self._normal_geometry)

        self.fullscreen_button.configure(text="Reader Fullscreen")
        self.text.focus_set()

    def _bind_shortcuts(self) -> None:
        self.bind("<Control-o>", lambda event: self._open_folder())
        self.bind("<Control-f>", self._focus_search)
        self.bind("<F5>", lambda event: self.reload_source())
        self.bind("<F1>", lambda event: self.show_help())

        self.bind("<Control-plus>", lambda event: self.increase_reader_font())
        self.bind("<Control-equal>", lambda event: self.increase_reader_font())
        self.bind("<Control-KP_Add>", lambda event: self.increase_reader_font())

        self.bind("<Control-minus>", lambda event: self.decrease_reader_font())
        self.bind("<Control-KP_Subtract>", lambda event: self.decrease_reader_font())

        self.bind("<Control-0>", lambda event: self.reset_reader_font())
        self.bind("<F11>", lambda event: self.toggle_reader_fullscreen())
        self.bind("<Escape>", lambda event: self.exit_reader_fullscreen())

    def _focus_search(self, event: tk.Event) -> str:
        if self._search_entry is not None:
            self._search_entry.focus_set()
            self._search_entry.selection_range(0, tk.END)
        return "break"

    # ------------------------------------------------------------------ #
    # Source loading (UI-thread side)                                    #
    # ------------------------------------------------------------------ #

    def load_source(self, source_path: Path) -> None:
        """Called from the UI thread; kicks off a background load."""
        self._start_load_thread(source_path)

    def reload_source(self) -> None:
        if self.corpus is None:
            return
        source_path = self.corpus.source.source_path
        self.load_source(source_path)

    def open_home(self) -> None:
        if self.corpus is None:
            return
        for candidate in [
            "README.md",
            "01_blocks/01_orientation_methodology.md",
            "01_blocks/10_boundary_governance_non_mixing.md",
            "03_model/PMS-AXIOM_Case_Index.yaml",
        ]:
            if candidate in self.corpus.documents:
                self.open_document(candidate)
                return

    # ------------------------------------------------------------------ #
    # Tree population                                                    #
    # ------------------------------------------------------------------ #

    def populate_file_tree(self) -> None:
        dbg("populate_file_tree: start")
        self.file_tree.delete(*self.file_tree.get_children())
        self._file_item_to_path.clear()
        self._case_block_tree_path_by_case.clear()
        self._virtual_block_section_paths.clear()
        if self.corpus is None:
            dbg("populate_file_tree: corpus is None, nothing to show")
            return

        def add_section(label: str, parent: str = "", open_: bool = False) -> str:
            # Keep the top corpus level open by default, but keep nested
            # groups collapsed unless explicitly opened.
            return self.file_tree.insert(parent, tk.END, text=label, open=(True if parent == "" else open_))

        def add_file(parent: str, rel_path: str, label: Optional[str] = None) -> None:
            if rel_path not in self.corpus.documents:
                return
            doc = self.corpus.documents[rel_path]
            item = self.file_tree.insert(parent, tk.END, text=label or doc.title, open=False)
            self._file_item_to_path[item] = rel_path

        def add_virtual_case(parent: str, case_id: str, label: str) -> None:
            rel_path = f"case://{case_id}/block"
            item = self.file_tree.insert(parent, tk.END, text=label, open=False)
            self._file_item_to_path[item] = rel_path
            self._case_block_tree_path_by_case[case_id] = rel_path

        def add_virtual_block_section(parent: str, part: str, kind: str, label: str) -> None:
            rel_path = f"block-section://{part}/{kind}"
            item = self.file_tree.insert(parent, tk.END, text=label, open=False)
            self._file_item_to_path[item] = rel_path
            self._virtual_block_section_paths[rel_path] = rel_path

        # Start / source.
        add_file("", "README.md", "README")

        source_root = add_section("Source")
        for rel in self._paths_under("00_source/"):
            label = None
            if rel == "00_source/PMS-AXIOM_legacy_full.md":
                label = "PMS AXIOM - LEGACY"
            add_file(source_root, rel, label)

        # Blocks are case-split for Parts I–VIII so the reader never scrolls
        # from one case into the next in block view. Non-case blocks remain full files.
        block_root = add_section("Blocks")
        add_file(block_root, "01_blocks/01_orientation_methodology.md", "01 Orientation / Methodology")

        for part, part_label in PART_LABELS.items():
            part_paths = sorted(
                [
                    rel for rel in self._paths_under("02_cases/markdown/")
                    if case_id_from_rel_path(rel) and case_id_from_rel_path(rel).startswith(part + "_")
                ],
                key=case_sort_key,
            )
            if not part_paths:
                continue
            part_item = add_section(part_label, block_root)
            add_virtual_block_section(part_item, part, "intro", "Chapter opening / cases orientation")
            for rel in part_paths:
                case_id = case_id_from_rel_path(rel) or ""
                case_no = int(case_id.split("_")[-1]) if case_id else 0
                title = remove_case_number(self.corpus.documents[rel].title)
                add_virtual_case(part_item, case_id, f"{case_no}. {title}")
            add_virtual_block_section(part_item, part, "summary", "Summary / conclusion")

        add_file(block_root, "01_blocks/10_boundary_governance_non_mixing.md", "10 Boundary / Governance / Non-Mixing")
        add_file(block_root, "01_blocks/11_conclusion.md", "11 Conclusion")

        # Cases with explicit order: Markdown artefacts, YAML artefacts,
        # prompts/templates. The reader tooling folder is intentionally not shown.
        cases_root = add_section("Cases")

        md_root = add_section("Markdown Case Artefacts", cases_root)
        for part, part_label in PART_LABELS.items():
            part_paths = sorted(
                [
                    rel for rel in self._paths_under("02_cases/markdown/")
                    if case_id_from_rel_path(rel) and case_id_from_rel_path(rel).startswith(part + "_")
                ],
                key=case_sort_key,
            )
            if not part_paths:
                continue
            part_item = add_section(part_label, md_root)
            for rel in part_paths:
                case_id = case_id_from_rel_path(rel) or ""
                case_no = int(case_id.split("_")[-1]) if case_id else 0
                title = remove_case_number(self.corpus.documents[rel].title)
                add_file(part_item, rel, f"{case_no}. {title}")

        yaml_root = add_section("YAML Case Artefacts", cases_root)
        yaml_groups = [
            ("PMS Core", "PMS_CORE_"),
            ("PMS + LOGIC", "PMS_LOGIC_"),
            ("PMS + ANTICIPATION", "PMS_ANTICIPATION_"),
            ("PMS + CONFLICT", "PMS_CONFLICT_"),
            ("PMS + CRITIQUE", "PMS_CRITIQUE_"),
            ("PMS + EDEN", "PMS_EDEN_"),
            ("PMS + SEX", "PMS_SEX_"),
            ("PMS + QC", "PMS_QC_"),
            ("PMS + QC-EXT", "PMS_QC_EXT_"),
            ("MIP", "MIP_"),
            ("AHP", "MIP_AHP_"),
        ]
        used_yaml: set[str] = set()
        for label, prefix in yaml_groups:
            paths = sorted(
                [rel for rel in self._paths_under("02_cases/yaml/") if Path(rel).name.startswith(prefix)],
                key=case_sort_key,
            )
            if not paths:
                continue
            group_item = add_section(label, yaml_root)
            for rel in paths:
                used_yaml.add(rel)
                add_file(group_item, rel, Path(rel).name)

        other_yaml = [rel for rel in self._paths_under("02_cases/yaml/") if rel not in used_yaml]
        if other_yaml:
            other_item = add_section("Other YAML", yaml_root)
            for rel in sorted(other_yaml, key=case_sort_key):
                add_file(other_item, rel, Path(rel).name)

        scaffolding_root = add_section("Prompts and Templates", cases_root)
        prompts_root = add_section("Markdown Case Prompts", scaffolding_root)
        for rel in self._paths_under("02_cases/markdown case prompts/"):
            add_file(prompts_root, rel, Path(rel).name)
        templates_root = add_section("YAML Case Templates", scaffolding_root)
        for rel in self._paths_under("02_cases/yaml case templates/"):
            add_file(templates_root, rel, Path(rel).name)

        model_root = add_section("Model / Index")
        for rel in self._paths_under("03_model/"):
            add_file(model_root, rel)

        reference_paths = self._paths_under("04_reference/")
        if reference_paths:
            reference_root = add_section("Reference")
            for rel in reference_paths:
                add_file(reference_root, rel)

        dbg(f"populate_file_tree: inserted {len(self._file_item_to_path)} file items")

    def _paths_under(self, prefix: str) -> List[str]:
        if self.corpus is None:
            return []
        return sorted(
            [rel for rel in self.corpus.ordered_paths if rel.startswith(prefix)],
            key=case_sort_key,
        )

    def populate_heading_tree(self, doc: Document) -> None:
        self.heading_tree.delete(*self.heading_tree.get_children())
        self._heading_item_to_anchor.clear()

        parent_by_level: Dict[int, str] = {0: ""}
        for heading in doc.headings:
            parent_level = heading.level - 1
            while parent_level > 0 and parent_level not in parent_by_level:
                parent_level -= 1
            parent = parent_by_level.get(parent_level, "")
            label = f"{'  ' * max(0, heading.level - 1)}{heading.text}"
            item = self.heading_tree.insert(parent, tk.END, text=label, open=(parent == ""))
            self._heading_item_to_anchor[item] = heading.anchor
            parent_by_level[heading.level] = item
            for deeper in list(parent_by_level):
                if deeper > heading.level:
                    del parent_by_level[deeper]

    # ------------------------------------------------------------------ #
    # Document rendering                                                 #
    # ------------------------------------------------------------------ #

    def open_document(self, rel_path: str, line_number: Optional[int] = None) -> None:
        if self.corpus is None:
            dbg(f"open_document: corpus is None, cannot open {rel_path}")
            return

        rel_path = normalize_rel_path(rel_path)

        # Virtual case-block entries must be handled before corpus lookup.
        if rel_path.startswith("case://"):
            parts = rel_path.split("/")
            if len(parts) >= 3:
                self.open_case_view(parts[2], preferred_view="block", source_rel_path=rel_path, line_number=line_number)
            return

        # Virtual block section entries render chapter openings and summaries as
        # bounded block excerpts, so the reader does not scroll into unrelated cases.
        if rel_path.startswith("block-section://"):
            self.open_block_section(rel_path)
            return

        if rel_path not in self.corpus.documents:
            dbg(f"open_document: {rel_path} not in corpus")
            return

        # Prevent accidental reopen loops caused by Treeview selection events.
        # Still allow reopening the same document when a search result requests a line jump.
        if self.current_path == rel_path and line_number is None:
            dbg(f"open_document: already open, skipping {rel_path}")
            return

        dbg(f"open_document: {rel_path}")
        case_id = case_id_from_rel_path(rel_path)
        if case_id:
            preferred = preferred_case_view_for_path(rel_path)
            self.open_case_view(case_id, preferred_view=preferred, source_rel_path=rel_path, line_number=line_number)
            return

        doc = self.corpus.documents[rel_path]
        self.current_case_id = None
        self.current_case_view = None
        self._refresh_case_switch_buttons()
        self.current_path = rel_path
        self.document_label_var.set(f"{doc.title} — {rel_path}")
        self.populate_heading_tree(doc)
        self.render_markdown(doc)
        self.highlight_query()
        self._select_file_tree_item(rel_path)
        if line_number is not None:
            self.scroll_to_source_line(line_number)
        else:
            self.text.yview_moveto(0)

        self.status_var.set(
            f"{rel_path} — {doc.line_count:,} lines, "
            f"{doc.word_count:,} words, {len(doc.headings):,} headings"
        )

    def open_block_section(self, rel_path: str) -> None:
        """Open a bounded block-only chapter opening or summary excerpt."""
        if self.corpus is None:
            return
        match = re.fullmatch(r"block-section://(\d{2})/(intro|summary)", normalize_rel_path(rel_path))
        if not match:
            return
        part, kind = match.groups()
        excerpt = self.block_section_excerpt(part, kind)
        if excerpt is None:
            return
        title, text = excerpt
        doc = Document(
            rel_path=rel_path,
            title=title,
            text=text,
            headings=parse_headings(strip_frontmatter(text)),
            frontmatter={},
        )

        self.current_case_id = None
        self.current_case_view = None
        self._refresh_case_switch_buttons()
        self.current_path = rel_path
        self.document_label_var.set(f"{doc.title} — {doc.rel_path}")
        self.populate_heading_tree(doc)
        self.render_markdown(doc)
        self.highlight_query()
        self._select_file_tree_item(rel_path)
        self.text.yview_moveto(0)
        self.status_var.set(
            f"{doc.rel_path} — {doc.line_count:,} lines, "
            f"{doc.word_count:,} words, {len(doc.headings):,} headings"
        )

    def open_case_view(
        self,
        case_id: str,
        preferred_view: Optional[str] = None,
        source_rel_path: Optional[str] = None,
        line_number: Optional[int] = None,
    ) -> None:
        """Open one case in one of its switchable views.

        Views:
        - block: paper-facing block subsection only
        - markdown: full Markdown case artefact
        - yaml:<rel_path>: one YAML artefact for the same case
        """
        if self.corpus is None:
            return

        available = self.available_case_views(case_id)
        if not available:
            return

        view = preferred_view if preferred_view in available else None
        if view is None:
            for candidate in ("block", "markdown"):
                if candidate in available:
                    view = candidate
                    break
        if view is None:
            view = next(iter(available))

        doc = self.case_view_document(case_id, view)
        if doc is None:
            return

        self.current_case_id = case_id
        self.current_case_view = view
        self.current_path = doc.rel_path
        self.document_label_var.set(f"{doc.title} — {doc.rel_path}")
        self._refresh_case_switch_buttons()
        self.populate_heading_tree(doc)
        self.render_markdown(doc)
        self.highlight_query()

        # Keep the file tree selection on the selected view when possible.
        select_path = source_rel_path
        if view == "block":
            select_path = f"case://{case_id}/block"
        elif view == "markdown":
            select_path = f"02_cases/markdown/{case_id}.md"
        elif view.startswith("yaml:"):
            select_path = view.split(":", 1)[1]
        if select_path:
            self._select_file_tree_item(select_path)

        if line_number is not None and select_path == source_rel_path:
            self.scroll_to_source_line(line_number)
        else:
            self.text.yview_moveto(0)

        self.status_var.set(
            f"{doc.rel_path} — {doc.line_count:,} lines, "
            f"{doc.word_count:,} words, {len(doc.headings):,} headings"
        )

    def available_case_views(self, case_id: str) -> Dict[str, str]:
        if self.corpus is None:
            return {}
        views: Dict[str, str] = {}
        if self.block_case_excerpt(case_id) is not None:
            views["block"] = "Block Markdown"
        md_path = f"02_cases/markdown/{case_id}.md"
        if md_path in self.corpus.documents:
            views["markdown"] = "Markdown Case Artefact"
        for label, rel in self.yaml_variant_paths(case_id):
            views[f"yaml:{rel}"] = label
        return views

    def case_view_document(self, case_id: str, view: str) -> Optional[Document]:
        if self.corpus is None:
            return None
        if view == "block":
            excerpt = self.block_case_excerpt(case_id)
            if excerpt is None:
                return None
            title, text = excerpt
            return Document(
                rel_path=f"case://{case_id}/block",
                title=f"Block Markdown — {title}",
                text=text,
                headings=parse_headings(strip_frontmatter(text)),
                frontmatter={},
            )
        if view == "markdown":
            rel = f"02_cases/markdown/{case_id}.md"
            return self.corpus.documents.get(rel)
        if view.startswith("yaml:"):
            rel = view.split(":", 1)[1]
            return self.corpus.documents.get(rel)
        return None

    def block_section_excerpt(self, part: str, kind: str) -> Optional[Tuple[str, str]]:
        """Return intro-through-cases-heading or summary excerpt for one block part."""
        if self.corpus is None:
            return None
        block_path = BLOCK_BY_PART.get(part)
        if not block_path or block_path not in self.corpus.documents:
            return None
        doc = self.corpus.documents[block_path]
        body = strip_frontmatter(doc.text)
        lines = body.splitlines()

        if kind == "intro":
            # Include the chapter opening through the Cases heading (e.g. 4 ... 4.4 Cases),
            # but stop before the first case subsection (e.g. 4.4.1).
            start_idx = 0
            cases_idx: Optional[int] = None
            first_case_idx: Optional[int] = None
            part_num = str(int(part))
            for idx, line in enumerate(lines):
                m = HEADING_RE.match(line)
                if not m:
                    continue
                heading_text = clean_heading_text(m.group(2))
                if cases_idx is None and re.match(rf"^{re.escape(part_num)}\.4(\s|$|[—:-])", heading_text):
                    cases_idx = idx
                    continue
                if cases_idx is not None and re.match(rf"^{re.escape(part_num)}\.4\.\d+(\s|$|[—:-])", heading_text):
                    first_case_idx = idx
                    break
            if cases_idx is None:
                return None
            end_idx = first_case_idx if first_case_idx is not None else len(lines)
            text = "\n".join(lines[start_idx:end_idx]).strip() + "\n"
            return f"Block Opening — {PART_LABELS.get(part, part)}", text

        if kind == "summary":
            # Prefer an explicit x.5 Summary heading; fall back to the last Summary heading.
            part_num = str(int(part))
            start_idx: Optional[int] = None
            start_level = 0
            last_summary_idx: Optional[Tuple[int, int]] = None
            for idx, line in enumerate(lines):
                m = HEADING_RE.match(line)
                if not m:
                    continue
                heading_text = clean_heading_text(m.group(2))
                level = len(m.group(1))
                if re.match(rf"^{re.escape(part_num)}\.5(\s|$|[—:-])", heading_text):
                    start_idx = idx
                    start_level = level
                    break
                if "summary" in heading_text.lower() or "conclusion" in heading_text.lower():
                    last_summary_idx = (idx, level)
            if start_idx is None and last_summary_idx is not None:
                start_idx, start_level = last_summary_idx
            if start_idx is None:
                return None
            end_idx = len(lines)
            for idx in range(start_idx + 1, len(lines)):
                m = HEADING_RE.match(lines[idx])
                if not m:
                    continue
                if len(m.group(1)) <= start_level:
                    end_idx = idx
                    break
            text = "\n".join(lines[start_idx:end_idx]).strip() + "\n"
            return f"Block Summary — {PART_LABELS.get(part, part)}", text

        return None

    def block_case_excerpt(self, case_id: str) -> Optional[Tuple[str, str]]:
        if self.corpus is None:
            return None
        match = CASE_ID_RE.fullmatch(case_id)
        if not match:
            return None
        part, case_no = match.groups()
        block_path = BLOCK_BY_PART.get(part)
        if not block_path or block_path not in self.corpus.documents:
            return None
        doc = self.corpus.documents[block_path]
        body = strip_frontmatter(doc.text)
        lines = body.splitlines()
        section = f"{int(part)}.4.{int(case_no)}"
        start_idx: Optional[int] = None
        start_level = 0
        for idx, line in enumerate(lines):
            m = HEADING_RE.match(line)
            if not m:
                continue
            heading_text = clean_heading_text(m.group(2))
            if re.match(rf"^{re.escape(section)}(\s|$|[—:-])", heading_text):
                start_idx = idx
                start_level = len(m.group(1))
                break
        if start_idx is None:
            return None
        end_idx = len(lines)
        for idx in range(start_idx + 1, len(lines)):
            m = HEADING_RE.match(lines[idx])
            if not m:
                continue
            level = len(m.group(1))
            if level <= start_level:
                end_idx = idx
                break
        excerpt_lines = lines[start_idx:end_idx]
        text = "\n".join(excerpt_lines).strip() + "\n"
        title = clean_heading_text(HEADING_RE.match(lines[start_idx]).group(2)) if HEADING_RE.match(lines[start_idx]) else case_id
        return title, text

    def yaml_variant_paths(self, case_id: str) -> List[Tuple[str, str]]:
        if self.corpus is None:
            return []
        match = CASE_ID_RE.fullmatch(case_id)
        if not match:
            return []
        part, _case_no = match.groups()
        candidates: List[Tuple[str, str]] = []
        base = f"02_cases/yaml/PMS_CORE_{case_id}.yaml"
        candidates.append(("PMS Core YAML", base))

        addon_prefix = ADDON_PREFIX_BY_PART.get(part)
        if addon_prefix:
            addon_path = f"02_cases/yaml/{addon_prefix}_{case_id}.yaml"
            label = "Add-on YAML"
            if addon_prefix == "PMS_QC":
                label = "QC YAML"
            candidates.append((label, addon_path))

        if part == "11":
            candidates.append(("QC-EXT YAML", f"02_cases/yaml/{QC_EXT_PREFIX}_{case_id}.yaml"))

        candidates.append(("MIP YAML", f"02_cases/yaml/MIP_{case_id}.yaml"))
        candidates.append(("AHP YAML", f"02_cases/yaml/MIP_AHP_{case_id}.yaml"))

        return [(label, rel) for label, rel in candidates if rel in self.corpus.documents]

    def _refresh_case_switch_buttons(self) -> None:
        for button in self._case_button_widgets:
            button.destroy()
        self._case_button_widgets.clear()

        if self.current_case_id is None:
            self.case_switch_empty.configure(text="Select a case artefact to enable case views.")
            if not self.case_switch_empty.winfo_manager():
                self.case_switch_empty.pack(side=tk.LEFT)
            return

        if self.case_switch_empty.winfo_manager():
            self.case_switch_empty.pack_forget()

        views = self.available_case_views(self.current_case_id)
        if not views:
            self.case_switch_empty.configure(text="No alternate case views found.")
            self.case_switch_empty.pack(side=tk.LEFT)
            return

        for view_key, label in views.items():
            button_style = "ActiveView.TButton" if view_key == self.current_case_view else "TButton"
            button = ttk.Button(
                self.case_switch_frame,
                text=label,
                style=button_style,
                command=lambda key=view_key: self.open_case_view(self.current_case_id or "", preferred_view=key),
            )
            button.pack(side=tk.LEFT, padx=(0, 4))
            self._case_button_widgets.append(button)

    def render_markdown(self, doc: Document) -> None:
        """Render *doc* into the text widget.

        This renderer keeps large files fast by avoiding per-line source marks
        in large documents, but still performs Markdown-light normalization:
        headings, fenced code blocks, YAML blocks, lists, and tables.
        """
        dbg(f"render_markdown: {doc.rel_path} ({doc.line_count} lines)")
        is_yaml_doc = Path(doc.rel_path).suffix.lower() in {".yaml", ".yml"}
        body = doc.text if is_yaml_doc else strip_frontmatter(doc.text)
        self.heading_indices.clear()

        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)

        try:
            use_source_marks = doc.line_count <= LARGE_DOC_LINE_THRESHOLD
            if is_yaml_doc:
                self._render_yaml_document(doc, body, use_source_marks=use_source_marks)
            else:
                self._render_markdown_blocks(doc, body, use_source_marks=use_source_marks)
        except Exception as exc:
            dbg(f"render_markdown: exception: {exc}")
            self.status_var.set(f"Render error: {exc}")
        finally:
            self.text.configure(state=tk.DISABLED)

    def _render_yaml_document(self, doc: Document, body: str, use_source_marks: bool) -> None:
        """Render a YAML artefact as syntax-colored YAML, not as Markdown.

        The EM reader already rendered YAML fences with lightweight key/value
        coloring. AXIOM uses many standalone .yaml files, so they need the same
        treatment at document level.
        """
        lines = body.splitlines()
        for source_line, raw_line in enumerate(lines, start=1):
            line_start = self.text.index(tk.INSERT)
            if use_source_marks:
                self.text.mark_set(f"source_line_{source_line}", line_start)
            self._insert_yaml_line(raw_line)

        if not lines:
            self.text.insert(tk.END, "\n", ("code",))

    def _render_markdown_blocks(self, doc: Document, body: str, use_source_marks: bool) -> None:
        """Markdown-light block renderer.

        It is intentionally not a full Markdown engine. It renders the PMS-AXIOM
        corpus well enough without external dependencies and without destroying
        performance on the large monolith.
        """
        lines = body.splitlines()
        i = 0
        heading_counter = 0

        while i < len(lines):
            raw_line = lines[i]
            source_line = i + 1
            line_start = self.text.index(tk.INSERT)

            if use_source_marks:
                self.text.mark_set(f"source_line_{source_line}", line_start)

            fence_match = FENCE_RE.match(raw_line)
            if fence_match:
                opener = fence_match.group(1)
                fence_char = opener[0]
                fence_len = len(opener)
                language = (fence_match.group(2) or "").lower()
                block_lines: List[str] = []
                i += 1

                while i < len(lines):
                    close_match = FENCE_RE.match(lines[i])
                    if close_match:
                        closer = close_match.group(1)
                        if closer[0] == fence_char and len(closer) >= fence_len:
                            break
                    block_lines.append(lines[i])
                    i += 1

                # Skip closing fence when present. Accept closers with at least
                # the opener length, so accidental four-backtick closers close
                # ordinary triple-backtick blocks.
                if i < len(lines):
                    close_match = FENCE_RE.match(lines[i])
                    if close_match and close_match.group(1)[0] == fence_char and len(close_match.group(1)) >= fence_len:
                        i += 1

                self._insert_code_block(block_lines, language)
                continue

            heading_match = HEADING_RE.match(raw_line)
            if heading_match:
                level = min(len(heading_match.group(1)), 6)
                heading_text = clean_heading_text(heading_match.group(2))
                anchor = f"h-{heading_counter}-{slugify(heading_text)}"
                heading_counter += 1
                self.heading_indices[anchor] = line_start
                self._insert_inline_markdown(heading_text, (f"h{level}",))
                self.text.insert(tk.END, "\n", (f"h{level}",))
                i += 1
                continue

            if looks_like_table_line(raw_line):
                table_lines: List[str] = []
                while i < len(lines) and looks_like_table_line(lines[i]):
                    table_lines.append(lines[i])
                    i += 1
                self._insert_table_block(table_lines)
                continue

            list_match = LIST_RE.match(raw_line)
            if list_match:
                indent, _bullet, content = list_match.groups()
                level = max(0, len(indent.replace("\t", "    ")) // 2)
                prefix = "  " * level + "• "
                self.text.insert(tk.END, prefix, ("list",))
                self._insert_inline_markdown(content, ("list",))
                self.text.insert(tk.END, "\n", ("list",))
                i += 1
                continue

            ordered_match = ORDERED_LIST_RE.match(raw_line)
            if ordered_match:
                indent, number, content = ordered_match.groups()
                level = max(0, len(indent.replace("\t", "    ")) // 2)
                prefix = "  " * level + f"{number}. "
                self.text.insert(tk.END, prefix, ("list",))
                self._insert_inline_markdown(content, ("list",))
                self.text.insert(tk.END, "\n", ("list",))
                i += 1
                continue

            if raw_line.strip().startswith(">"):
                quote_text = re.sub(r"^\s*>\s?", "", raw_line)
                self._insert_inline_markdown(quote_text, ("quote",))
                self.text.insert(tk.END, "\n", ("quote",))
                i += 1
                continue

            if raw_line.strip() in {"---", "***", "___"}:
                self.text.insert(tk.END, "\u2500" * 80 + "\n", ("rule",))
                i += 1
                continue

            self._insert_inline_markdown(raw_line, ("body",))
            self.text.insert(tk.END, "\n", ("body",))
            i += 1

        dbg(f"_render_markdown_blocks: done ({heading_counter} headings rendered)")

    def _insert_code_block(self, block_lines: List[str], language: str) -> None:
        """Insert a fenced code block without showing the fence markers."""
        if not block_lines:
            self.text.insert(tk.END, "\n", ("code",))
            return

        # Top margin.
        self.text.insert(tk.END, "\n", ("body",))

        if language in {"yaml", "yml"}:
            for raw_line in block_lines:
                self._insert_yaml_line(raw_line)
        else:
            block = "\n".join(block_lines)
            self.text.insert(tk.END, block + "\n", ("code",))

        # Bottom margin.
        self.text.insert(tk.END, "\n", ("body",))

    def _insert_yaml_line(self, raw_line: str) -> None:
        """Insert one YAML line with lightweight syntax coloring."""
        stripped = raw_line.strip()

        if not stripped:
            self.text.insert(tk.END, "\n", ("code",))
            return

        if stripped.startswith("#"):
            self.text.insert(tk.END, raw_line + "\n", ("quote",))
            return

        # YAML list item with inline key: "- key: value"
        list_key_match = re.match(r"^(\s*-\s*)([A-Za-z0-9_.-]+)(\s*:\s*)(.*)$", raw_line)
        if list_key_match:
            bullet, key, separator, value = list_key_match.groups()
            self.text.insert(tk.END, bullet, ("code",))
            self.text.insert(tk.END, key, ("yaml_key",))
            self.text.insert(tk.END, separator, ("code",))
            self.text.insert(tk.END, value + "\n", ("yaml_value",))
            return

        # Standard YAML key: value
        match = re.match(r"^(\s*)([A-Za-z0-9_.-]+)(\s*:\s*)(.*)$", raw_line)
        if match:
            indent, key, separator, value = match.groups()
            self.text.insert(tk.END, indent, ("code",))
            self.text.insert(tk.END, key, ("yaml_key",))
            self.text.insert(tk.END, separator, ("code",))
            self.text.insert(tk.END, value + "\n", ("yaml_value",))
            return

        self.text.insert(tk.END, raw_line + "\n", ("code",))

    def _insert_inline_markdown(self, text: str, base_tags: Tuple[str, ...]) -> None:
        """Insert one text fragment with lightweight inline Markdown styling.

        Supported:
        - `inline code`
        - ***bold italic***
        - **bold**
        - *italic*

        This intentionally avoids full Markdown parsing but handles the corpus'
        most common inline patterns.
        """
        token_re = re.compile(
            r"(`[^`]+`|\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*\n]+\*)"
        )

        pos = 0

        for match in token_re.finditer(text):
            if match.start() > pos:
                self.text.insert(tk.END, text[pos:match.start()], base_tags)

            token = match.group(0)

            if token.startswith("`") and token.endswith("`"):
                self.text.insert(tk.END, token[1:-1], base_tags + ("inline_code",))
            elif token.startswith("***") and token.endswith("***"):
                self.text.insert(tk.END, token[3:-3], base_tags + ("bold_italic",))
            elif token.startswith("**") and token.endswith("**"):
                self.text.insert(tk.END, token[2:-2], base_tags + ("bold",))
            elif token.startswith("*") and token.endswith("*"):
                self.text.insert(tk.END, token[1:-1], base_tags + ("italic",))
            else:
                self.text.insert(tk.END, token, base_tags)

            pos = match.end()

        if pos < len(text):
            self.text.insert(tk.END, text[pos:], base_tags)

    def _insert_table_block(self, table_lines: List[str]) -> None:
        """Render a Markdown table as an aligned monospace text table."""
        rows: List[List[str]] = []

        for line in table_lines:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]

            # Skip Markdown separator rows like | --- | :---: |
            if cells and all(re.fullmatch(r":?-{3,}:?", cell or "---") for cell in cells):
                continue

            rows.append(cells)

        if not rows:
            return

        column_count = max(len(row) for row in rows)
        normalized_rows: List[List[str]] = [
            row + [""] * (column_count - len(row))
            for row in rows
        ]

        widths = [
            max(len(row[column]) for row in normalized_rows)
            for column in range(column_count)
        ]

        rendered_lines: List[str] = []
        for row_index, row in enumerate(normalized_rows):
            rendered = "  │  ".join(
                row[column].ljust(widths[column])
                for column in range(column_count)
            )
            rendered_lines.append(rendered)

            if row_index == 0 and len(normalized_rows) > 1:
                rendered_lines.append("──┼──".join("─" * width for width in widths))

        self.text.insert(tk.END, "\n", ("body",))
        self.text.insert(tk.END, "\n".join(rendered_lines) + "\n", ("table",))
        self.text.insert(tk.END, "\n", ("body",))

    # ------------------------------------------------------------------ #
    # Search                                                             #
    # ------------------------------------------------------------------ #

    def run_search(self) -> None:
        if self.corpus is None:
            return
        query = self.search_var.get().strip()
        self.search_tree.delete(*self.search_tree.get_children())
        self.search_results = self.corpus.search(query)

        for index, (rel_path, line_no, snippet) in enumerate(self.search_results):
            title = self.corpus.documents[rel_path].title
            self.search_tree.insert("", tk.END, iid=str(index), values=(title, line_no, snippet))

        self.highlight_query()
        if query:
            self.status_var.set(f"Search '{query}': {len(self.search_results):,} result(s).")
        else:
            self.status_var.set("Search cleared.")

    def clear_search(self) -> None:
        self.search_var.set("")
        self.search_tree.delete(*self.search_tree.get_children())
        self.search_results = []
        self.text.configure(state=tk.NORMAL)
        self.text.tag_remove("search", "1.0", tk.END)
        self.text.configure(state=tk.DISABLED)

    def highlight_query(self) -> None:
        query = self.search_var.get().strip()
        self.text.configure(state=tk.NORMAL)
        self.text.tag_remove("search", "1.0", tk.END)
        if query:
            start = "1.0"
            while True:
                pos = self.text.search(query, start, stopindex=tk.END, nocase=True)
                if not pos:
                    break
                end = f"{pos}+{len(query)}c"
                self.text.tag_add("search", pos, end)
                start = end
        self.text.configure(state=tk.DISABLED)

    def scroll_to_source_line(self, line_number: int) -> None:
        mark = f"source_line_{line_number}"

        try:
            index = self.text.index(mark)
        except tk.TclError:
            # Large documents do not create per-line marks.
            # Tk Text line indices are good enough for direct jumps.
            index = f"{max(1, line_number)}.0"

        self.text.configure(state=tk.NORMAL)
        self.text.tag_remove("current_line", "1.0", tk.END)
        self.text.tag_add("current_line", index, f"{index} lineend+1c")
        self.text.configure(state=tk.DISABLED)
        self.text.see(index)

    # ------------------------------------------------------------------ #
    # Toolbar / dialog actions                                           #
    # ------------------------------------------------------------------ #

    def _open_folder(self) -> None:
        path = filedialog.askdirectory(title="Open PMS-AXIOM folder")
        if path:
            self.load_source(Path(path))

    def _open_zip(self) -> None:
        path = filedialog.askopenfilename(
            title="Open PMS-AXIOM zip file",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")],
        )
        if path:
            self.load_source(Path(path))

    # ------------------------------------------------------------------ #
    # Event handlers                                                     #
    # ------------------------------------------------------------------ #

    def _on_file_selected(self, event: tk.Event) -> None:
        if self._suppress_file_select_event:
            dbg("_on_file_selected: suppressed programmatic selection")
            return

        selection = self.file_tree.selection()
        if not selection:
            return

        item = selection[0]
        rel_path = self._file_item_to_path.get(item)
        if rel_path:
            self.open_document(rel_path)

    def _on_heading_selected(self, event: tk.Event) -> None:
        selection = self.heading_tree.selection()
        if not selection:
            return
        item = selection[0]
        anchor = self._heading_item_to_anchor.get(item)
        if anchor and anchor in self.heading_indices:
            index = self.heading_indices[anchor]
            self.text.see(index)
            self.text.configure(state=tk.NORMAL)
            self.text.tag_remove("current_line", "1.0", tk.END)
            self.text.tag_add("current_line", index, f"{index} lineend+1c")
            self.text.configure(state=tk.DISABLED)

    def _on_search_result_open(self, event: tk.Event) -> None:
        selection = self.search_tree.selection()
        if not selection:
            return
        try:
            result_index = int(selection[0])
        except ValueError:
            return
        if result_index >= len(self.search_results):
            return
        rel_path, line_no, _snippet = self.search_results[result_index]
        self.open_document(rel_path, line_number=line_no)

    def _select_file_tree_item(self, rel_path: str) -> None:
        for item, item_path in self._file_item_to_path.items():
            if item_path == rel_path:
                self._suppress_file_select_event = True
                try:
                    self.file_tree.selection_set(item)
                    self.file_tree.see(item)
                finally:
                    self.after_idle(self._enable_file_select_events)
                break

    def _enable_file_select_events(self) -> None:
        self._suppress_file_select_event = False

    # ------------------------------------------------------------------ #
    # Cleanup                                                            #
    # ------------------------------------------------------------------ #

    def destroy(self) -> None:
        if self.corpus is not None:
            self.corpus.source.close()
        super().destroy()


# ---------------------------------------------------------------------------
# Pure helper functions
# ---------------------------------------------------------------------------

def normalize_rel_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("/")


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    raw = match.group(1)
    meta: Dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        if key:
            meta[key] = value
    return meta, text[match.end():]


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def parse_headings(text: str) -> List[Heading]:
    headings: List[Heading] = []
    in_code = False
    heading_counter = 0

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        try:
            is_fence = bool(FENCE_RE.match(raw_line))
        except Exception:
            is_fence = False

        if is_fence:
            in_code = not in_code
            continue
        if in_code:
            continue

        try:
            match = HEADING_RE.match(raw_line)
        except Exception:
            continue

        if not match:
            continue

        text_value = clean_heading_text(match.group(2))
        anchor = f"h-{heading_counter}-{slugify(text_value)}"
        headings.append(
            Heading(
                level=len(match.group(1)),
                text=text_value,
                line_number=line_number,
                anchor=anchor,
            )
        )
        heading_counter += 1
    return headings


def first_heading_title(headings: List[Heading]) -> Optional[str]:
    return headings[0].text if headings else None


def clean_heading_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+#*$", "", text)
    text = text.replace("`", "")
    return text


def slugify(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "heading"


def looks_like_table_line(line: str) -> bool:
    stripped = line.strip()
    return (
        stripped.startswith("|")
        and stripped.endswith("|")
        and stripped.count("|") >= 2
    )


def case_id_from_rel_path(rel_path: str) -> Optional[str]:
    rel = normalize_rel_path(rel_path)
    if rel.startswith("case://"):
        match = CASE_ID_RE.search(rel)
        return match.group(0) if match else None
    if rel.startswith("02_cases/markdown/") and rel.lower().endswith(".md"):
        match = CASE_ID_RE.search(Path(rel).stem)
        return match.group(0) if match else None
    if rel.startswith("02_cases/yaml/") and Path(rel).suffix.lower() in {".yaml", ".yml"}:
        match = YAML_CASE_RE.match(Path(rel).name)
        if match:
            return match.group("case")
        fallback = CASE_ID_RE.search(Path(rel).stem)
        return fallback.group(0) if fallback else None
    return None


def preferred_case_view_for_path(rel_path: str) -> str:
    rel = normalize_rel_path(rel_path)
    if rel.startswith("case://"):
        return "block"
    if rel.startswith("02_cases/markdown/"):
        return "markdown"
    if rel.startswith("02_cases/yaml/"):
        return f"yaml:{rel}"
    return "block"


def case_sort_key(rel_path: str) -> Tuple[int, int, int, str]:
    case_id = case_id_from_rel_path(rel_path)
    if case_id:
        part, _mid, case_no = case_id.split("_")
        return (int(part), int(case_no), 0, natural_sort_key(rel_path))
    # Keep templates/prompts predictable but after real case ids.
    return (999, 999, 0, natural_sort_key(rel_path))


def remove_case_number(title: str) -> str:
    value = clean_heading_text(title)
    value = re.sub(r"^\d+(?:\.\d+)+\s*[-–—:]?\s*", "", value)
    return value.strip() or title


def sort_rel_path(rel_path: str) -> Tuple[int, str]:
    rel = normalize_rel_path(rel_path)
    order = [
        "README.md",
        "00_source/",
        "01_blocks/",
        "02_cases/markdown/",
        "02_cases/yaml/",
        "02_cases/markdown case prompts/",
        "02_cases/yaml case templates/",
        "03_model/",
        "04_reference/",
    ]
    for index, prefix in enumerate(order):
        if rel == prefix.rstrip("/") or rel.startswith(prefix):
            return (index, natural_sort_key(rel))
    return (len(order), natural_sort_key(rel))


def natural_sort_key(value: str) -> str:
    return re.sub(r"(\d+)", lambda m: f"{int(m.group(1)):06d}", value.lower())


def prettify_file_name(rel_path: str) -> str:
    name = Path(rel_path).name
    if name.lower().endswith(".md"):
        name = name[:-3]
    name = name.replace("_", " ").replace("-", " - ")
    name = re.sub(r"\s+", " ", name).strip()
    return name


def walk_widgets(widget: tk.Widget) -> Iterable[tk.Widget]:
    yield widget
    for child in widget.winfo_children():
        yield from walk_widgets(child)


def discover_default_source() -> Optional[Path]:
    """Return the first valid PMS-AXIOM source path found, or None."""
    candidates: List[Path] = []

    if len(sys.argv) > 1:
        candidates.append(Path(sys.argv[1]))

    cwd = Path.cwd()
    script_dir = Path(__file__).resolve().parent
    repo_root_from_tool_dir = script_dir.parent

    candidates.extend(
        [
            cwd,
            cwd / "PMS-AXIOM",
            cwd / "PMS-AXIOM.zip",
            script_dir,
            script_dir / "PMS-AXIOM",
            script_dir / "PMS-AXIOM.zip",
            repo_root_from_tool_dir,
            repo_root_from_tool_dir / "PMS-AXIOM",
            repo_root_from_tool_dir / "PMS-AXIOM.zip",
        ]
    )

    for candidate in candidates:
        dbg(f"discover: checking {candidate}")
        try:
            if candidate.is_dir():
                CorpusSource._detect_folder_root(candidate)
                dbg(f"discover: valid folder at {candidate}")
                return candidate
            if candidate.is_file() and candidate.suffix.lower() == ".zip":
                with zipfile.ZipFile(candidate) as zf:
                    CorpusSource._detect_zip_prefix(zf)
                dbg(f"discover: valid zip at {candidate}")
                return candidate
        except Exception as e:
            dbg(f"discover: {candidate} rejected ({e})")
            continue

    dbg("discover: no valid source found")
    return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    dbg(f"main: argv={sys.argv}")
    initial_source = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    app = PmsAxiomReaderApp(initial_source=initial_source)
    app.mainloop()
    dbg("main: mainloop exited")


if __name__ == "__main__":
    main()
