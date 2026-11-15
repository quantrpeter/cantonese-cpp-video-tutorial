"""The coding stage: an editor (left) and a terminal (right) on a dark background.

The stage keeps its state from scene to scene: what one scene typed or ran is still there in the
next. Terminal output is never made up: `Run` takes a `cpp.Result` from a real run, colours
included.

    stage = Stage({"hello.cpp": CODE}, title="Hello, World!")
    stage.scene(Open("hello.cpp", mode="empty"), Type("hello.cpp", "#include <iostream>\\n", at="type"))
    stage.scene(Mark(4, at="mark"), Note("std::cout：輸出", at="mark"), Run(result, at="run"))

Events, in the order they are given (each waits for the one before, and for its `at`):
    Open(file, mode)          show a file: lines (line by line), type, instant, or empty
    Type(file, text, after=)  type text at the end, or after/before the first match of a string
                              (last=True: the last match, e.g. before="}" for the end of main)
    Replace(file, old, new)   select `old`, delete it, type `new`
    Mark(lines) / Mark(None)  highlight editor lines (one number or (first, last)); others dim
    Note(text) / Note(None)   a callout box over the terminal (where="term") or the editor
    Run(result)               type a command, wait its real run time, print its real output
                              (recall=True: an earlier command brought back with ↑, not retyped).
                              For a cpp.Input run, the output plays at its real pace and the
                              person's input is typed where the program waited for it (keys=
                              cues for each line, else a short pause); stream=True plays a plain
                              run's output line by line over its run time.
    Scroll(top=True)          scroll the terminal up to the last command (to read the start of a long report)
    Pause(seconds)
    Expect(file, text)        check that the editor shows exactly the code that was run
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass, replace
from functools import lru_cache

from PIL import Image, ImageDraw

from . import draw as D
from .style import (AMBER, BLUE, ED_BAR, ED_BG, ED_CURRENT, ED_GUTTER, ED_TEXT, H, INK, STAGE_BOTTOM,
                    STAGE_TOP, TERM_BG, TERM_DIM, TERM_PROMPT, TERM_TEXT, W, WHITE, font, mono)
from .syntax import ansi, colours
from .text import CJK
from .visuals import Timing, Visual

PX0, PY0, PH, GAP = 60, 190, 740, 30
BAR = 56
CODE_PX, CODE_LH = 28, 40
TERM_PX, TERM_LH = 26, 36
MARK_BG = (72, 64, 46)
SEL_BG = (38, 79, 120)


@dataclass(frozen=True)
class TermLine:
    kind: str   # "cmd", "out", or "part" (an unfinished line: the program waits after it)
    text: str


TYPED_ON, TYPED_OFF = "\x1b[1;36m", "\x1b[0m"   # what the person types shows in bold cyan
MAX_TERM = 300


def _typed(s: str) -> str:
    body = s.rstrip("\n")
    return (TYPED_ON + body + TYPED_OFF if body else "") + s[len(body):]


CLEAR = "\x1b[2J"   # a program that clears the screen (a game redrawing its frame) wipes what was shown


def _lines(base: tuple, acc: str, done: bool = False) -> tuple:
    k = acc.rfind(CLEAR)
    if k >= 0:
        base, acc = (), acc[k + len(CLEAR):]
    acc = acc.replace("\x1b[H", "")
    parts = acc.split("\n")
    out = [TermLine("out", l.expandtabs(8)) for l in parts[:-1]]
    if parts[-1]:
        out.append(TermLine("out" if done else "part", parts[-1].expandtabs(8)))
    return (base + tuple(out))[-MAX_TERM:]


@dataclass(frozen=True)
class State:
    tabs: tuple = ()
    active: str | None = None
    texts: tuple = ()            # ((file, text), ...)
    cursor: int = 0              # in the active file
    sel: tuple | None = None     # (start, end) in the active file
    mark: tuple | None = None    # (file, first line, last line), 1-based
    term: tuple = ()             # TermLine, ...
    typing: str = ""             # command being typed after the prompt
    busy: bool = False           # a command is running
    focus: str = "term"          # where the cursor is
    note: str | None = None
    note_where: str = "term"
    note_a: float = 0.0          # note opacity, for its fade
    scroll_top: object = False   # True: show the last command's output from its start; str: from the line containing it

    def text(self, f: str) -> str:
        return dict(self.texts).get(f, "")

    def has(self, f: str) -> bool:
        return f in dict(self.texts)

    def with_text(self, f: str, s: str, cursor: int | None = None) -> "State":
        d = dict(self.texts)
        d[f] = s
        return replace(self, texts=tuple(sorted(d.items())), cursor=len(s) if cursor is None else cursor)


@dataclass
class Open:
    file: str
    at: object = None
    mode: str = "lines"   # lines, type, instant, empty
    rate: float = 7.0     # lines or characters per second


@dataclass
class Type:
    file: str
    text: str
    at: object = None
    after: str | None = None
    before: str | None = None
    rate: float = 14.0
    last: bool = False    # match the last occurrence of after/before (e.g. before="}" = the end of main)


@dataclass
class Replace:
    file: str
    old: str
    new: str
    at: object = None
    rate: float = 14.0
    last: bool = False    # replace the last occurrence instead of the first


@dataclass
class Mark:
    lines: object = None  # 4, (3, 5) or None
    at: object = None
    file: str | None = None


@dataclass
class Note:
    text: str | None
    at: object = None
    where: str = "term"   # term or editor


@dataclass
class Run:
    result: object        # cpp.Result
    at: object = None
    rate: float = 19.0
    recall: bool = False  # the command was run before: it comes back with the ↑ key instead of being typed
    keys: tuple = ()      # Input runs: when each input line is typed (cues); missing ones follow a short pause
    type_rate: float = 8.0
    stream: bool = False  # plain runs: output appears line by line over the run time


@dataclass
class Scroll:
    """Scrolls the terminal up so the last command and the start of its output are in view (a long
    report whose first lines matter, like AddressSanitizer's); top=False scrolls back down.
    find="text" instead puts the first output line containing that text at the top (the one line
    of a long template error that names your own file)."""
    at: object = None
    top: bool = True
    find: str | None = None


@dataclass
class Pause:
    seconds: float
    at: object = None


@dataclass
class Expect:
    """Draws nothing: stops the build if the editor's text is not `text` at this point, so the
    code on screen is always the code that was really compiled."""
    file: str
    text: str
    at: object = None


def _jitter(i: int) -> float:
    return 0.6 + 0.8 * ((i * 7919) % 13) / 12


def _cols(s: str) -> int:
    return sum(2 if CJK.match(c) else 1 for c in s)


class Stage:
    """split: the editor's share of the width; 0 means a terminal only. code_px: the editor's
    font size (28 shows 16 lines of 48 characters; 24 shows 19 lines of 57)."""

    def __init__(self, files: dict[str, str] | None = None, title: str = "", split: float = 0.531,
                 code_px: int = CODE_PX):
        self.files = {k: v.rstrip("\n") for k, v in (files or {}).items()}
        self.code_px, self.code_lh = code_px, round(code_px * CODE_LH / CODE_PX)
        self.title = title
        self.state = State()
        inner = W - 2 * PX0 - GAP
        self.ew = int(inner * split) if split > 0 else 0
        self.tx = PX0 + self.ew + GAP if self.ew else PX0
        self.tw = W - PX0 - self.tx

    def scene(self, *events, title: str | None = None) -> "StageVisual":
        return StageVisual(self, list(events), self.title if title is None else title)


class StageVisual(Visual):
    dark = True

    def __init__(self, stage: Stage, events: list, title: str):
        self.stage, self.events, self.title = stage, events, title
        self._base = None
        self._kt: list[float] = []
        self._ks: list[State] = []
        self._sounds: list[tuple[float, str]] = []
        self._cache: dict = {}

    # -- timeline ------------------------------------------------------------------------------

    def prepare(self, timing: Timing) -> float:
        S = self.stage
        st, t = S.state, 0.0
        kt, ks, snd = [0.0], [st], []

        def push(s: State) -> State:
            kt.append(t)
            ks.append(s)
            return s

        def switch(f: str) -> State:
            if not st.has(f):
                raise KeyError(f"stage: {f} is not open; Open it first")
            if st.active == f and st.focus == "editor":
                return st
            return push(replace(st, active=f, focus="editor", sel=None, cursor=len(st.text(f))))

        def type_into(f: str, pos: int, txt: str, rate: float) -> State:
            nonlocal t
            s = st
            before, after = s.text(f)[:pos], s.text(f)[pos:]
            for i, ch in enumerate(txt):
                prev = txt[i - 1] if i else (before[-1:] or "\n")
                if ch == " " and prev in " \n":
                    t += 0.025                      # indentation goes in quickly
                elif ch == "\n":
                    t += 0.18
                else:
                    t += _jitter(i) / rate
                s = push(s.with_text(f, before + txt[: i + 1] + after, cursor=pos + i + 1))
                if not ch.isspace():
                    snd.append((t, "key"))
            return s

        for ev in self.events:
            a = timing.at(ev.at)
            t = max(t, a if a is not None else t)
            if isinstance(ev, Open):
                tabs = st.tabs if ev.file in st.tabs else st.tabs + (ev.file,)
                first = not st.has(ev.file)
                st = push(replace(st, tabs=tabs, active=ev.file, focus="editor", sel=None,
                                  cursor=len(st.text(ev.file))))
                if first:
                    full = "" if ev.mode == "empty" else S.files[ev.file]
                    if ev.mode in ("empty", "instant"):
                        st = push(st.with_text(ev.file, full))
                    elif ev.mode == "lines":
                        st = st.with_text(ev.file, "")
                        for e in [i for i, c in enumerate(full) if c == "\n"] + [len(full)]:
                            t += 1 / ev.rate
                            st = push(st.with_text(ev.file, full[:e]))
                    else:
                        st = st.with_text(ev.file, "")
                        st = type_into(ev.file, 0, full, ev.rate)
                t += 0.2
            elif isinstance(ev, Type):
                st = switch(ev.file)
                cur = st.text(ev.file)
                find = cur.rindex if ev.last else cur.index
                if ev.after is not None:
                    pos = find(ev.after) + len(ev.after)
                elif ev.before is not None:
                    pos = find(ev.before)
                else:
                    pos = len(cur)
                st = push(replace(st, cursor=pos))
                t += 0.25
                st = type_into(ev.file, pos, ev.text, ev.rate)
                t += 0.15
            elif isinstance(ev, Replace):
                st = switch(ev.file)
                cur = st.text(ev.file)
                p = cur.rindex(ev.old) if ev.last else cur.index(ev.old)
                old, new = ev.old, ev.new
                i = 0                                   # only the part that differs is edited
                while i < min(len(old), len(new)) and old[i] == new[i]:
                    i += 1
                j = 0
                while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]:
                    j += 1
                a_, b_ = p + i, p + len(old) - j
                if b_ > a_:
                    st = push(replace(st, sel=(a_, b_), cursor=b_))
                    t += 0.7
                    st = push(replace(st.with_text(ev.file, cur[:a_] + cur[b_:], cursor=a_), sel=None))
                    snd.append((t, "key"))
                    t += 0.2
                else:
                    st = push(replace(st, cursor=a_))
                    t += 0.3
                st = type_into(ev.file, a_, new[i:len(new) - j], ev.rate)
                t += 0.15
            elif isinstance(ev, Mark):
                if ev.lines is None:
                    st = push(replace(st, mark=None))
                else:
                    a_, b_ = (ev.lines, ev.lines) if isinstance(ev.lines, int) else ev.lines
                    st = push(replace(st, mark=(ev.file or st.active, a_, b_)))
            elif isinstance(ev, Note):
                if st.note is not None and st.note_a > 0:
                    for k in (3, 2, 1, 0):
                        t += 0.05
                        st = push(replace(st, note_a=k / 4))
                if ev.text is not None:
                    st = push(replace(st, note=ev.text, note_where=ev.where, note_a=0))
                    for k in (1, 2, 3, 4):
                        t += 0.05
                        st = push(replace(st, note_a=k / 4))
                else:
                    st = push(replace(st, note=None, note_a=0))
            elif isinstance(ev, Run):
                r = ev.result
                st = push(replace(st, focus="term", sel=None))
                t += 0.25
                if ev.recall:
                    t += 0.2
                    st = push(replace(st, typing=r.cmd))
                    snd.append((t, "key"))
                else:
                    for i in range(len(r.cmd)):
                        t += _jitter(i) / ev.rate
                        st = push(replace(st, typing=r.cmd[: i + 1]))
                        if not r.cmd[i].isspace():
                            snd.append((t, "key"))
                t += 0.35
                if r.cmd.strip() == "clear":
                    st = push(replace(st, typing="", term=()))
                    snd.append((t, "enter"))
                    t += 0.25
                    continue
                st = push(replace(st, typing="", busy=True, scroll_top=False,
                                  term=(st.term + (TermLine("cmd", r.cmd),))[-MAX_TERM:]))
                snd.append((t, "enter"))
                base = st.term
                if getattr(r, "io", None):
                    acc, t_cmd, shift, ki = "", t, 0.0, 0
                    for kind, txt, rt in r.io:
                        if kind == "o":
                            t = max(t, t_cmd + rt + shift)
                            acc += txt
                            st = push(replace(st, term=_lines(base, acc)))
                            continue
                        want = timing.at(ev.keys[ki]) if ki < len(ev.keys) else None
                        ki += 1
                        t = max(t + 0.8, want if want is not None else 0.0)
                        if txt in ("^C", ""):
                            acc += txt
                            st = push(replace(st, term=_lines(base, acc)))
                            snd.append((t, "key"))
                        else:
                            for i, ch in enumerate(txt):
                                t += 0.3 if ch == "\n" else _jitter(i) / ev.type_rate
                                snd.append((t, "enter" if ch == "\n" else "key"))
                                st = push(replace(st, term=_lines(base, acc + _typed(txt[: i + 1]))))
                            acc += _typed(txt)
                        shift = t - (t_cmd + rt)
                    t += 0.12
                    st = push(replace(st, busy=False, term=_lines(base, acc, done=True)))
                elif ev.stream and r.output.strip():
                    rows = r.output.rstrip("\n").split("\n")
                    step = max(0.12, r.seconds) / len(rows)
                    for k in range(len(rows)):
                        t += step
                        st = push(replace(st, term=_lines(base, "\n".join(rows[: k + 1]) + "\n")))
                    st = push(replace(st, busy=False))
                else:
                    t += max(0.12, r.seconds)
                    out = r.output.rstrip("\n")
                    st = push(replace(st, busy=False, term=_lines(base, out + "\n" if out.strip() else "")))
                t += 0.3
            elif isinstance(ev, Scroll):
                st = push(replace(st, scroll_top=ev.find if ev.find and ev.top else ev.top))
            elif isinstance(ev, Pause):
                t += ev.seconds
            elif isinstance(ev, Expect):
                have, want = st.text(ev.file), ev.text.rstrip("\n")
                if have != want:
                    raise AssertionError(f"stage: {ev.file} on screen differs from the code that was run\n"
                                         f"--- on screen\n{have}\n--- run\n{want}")
        S.state = st
        self._kt, self._ks, self._sounds = kt, ks, snd
        return t

    def sounds(self):
        return self._sounds

    def _at(self, t: float) -> tuple[int, State, bool]:
        i = max(0, bisect.bisect_right(self._kt, t) - 1)
        recent = t - self._kt[i] < 0.6
        cursor = recent or int(t * 1.8) % 2 == 0
        return i, self._ks[i], cursor

    def key(self, t):
        i, _, cursor = self._at(t)
        return (i, cursor)

    # -- drawing -------------------------------------------------------------------------------

    def base(self) -> Image.Image:
        if self._base is None:
            im = D.gradient(W, H, STAGE_TOP, STAGE_BOTTOM)
            d = ImageDraw.Draw(im)
            if self.tag:
                d.text((PX0, 44), self.tag, font=font(28, "medium"), fill=TERM_DIM)
            if self.title:
                d.text((PX0, 90), self.title, font=font(54, "bold"), fill=WHITE)
            self._base = im
        return self._base

    def render(self, t):
        _, st, cursor = self._at(t)
        im = self.base().copy()
        S = self.stage
        ed_on = st.focus == "editor" and cursor
        tm_on = st.focus == "term" and cursor
        parts = []
        if S.ew:
            parts.append((("ed", st.tabs, st.active, st.text(st.active) if st.active else "", st.cursor, st.sel,
                           st.mark, st.focus == "editor", ed_on), lambda: self._editor(st, ed_on), PX0))
        parts.append((("tm", st.term, st.typing, st.busy, tm_on, st.scroll_top), lambda: self._terminal(st, tm_on), S.tx))
        for k, fn, x in parts:
            if k not in self._cache:
                if len(self._cache) > 600:
                    self._cache.clear()
                self._cache[k] = fn()
            D.paste(im, self._cache[k], x, PY0)
        if st.note and st.note_a > 0:
            self._note(im, st)
        return im

    def _note(self, im: Image.Image, st: State) -> None:
        S = self.stage
        if st.note_where == "editor" and S.ew:
            x, w = PX0 + 30, S.ew - 60
        else:
            x, w = S.tx + 30, S.tw - 60
        box = _note_img(st.note, w)
        if st.note_a < 1:
            box = box.copy()
            box.putalpha(box.getchannel("A").point(lambda a: int(a * st.note_a)))
            box.info["pad"] = _note_img(st.note, w).info["pad"]
        D.paste(im, box, x, PY0 + PH - 30 - (box.height - 2 * box.info["pad"]))

    def _editor(self, st: State, cursor: bool) -> Image.Image:
        EW = self.stage.ew
        box = D.shadow_box(EW, PH, 18, ED_BG, blur=20, shadow=(0, 0, 0, 120))
        p = box.info["pad"]
        d = ImageDraw.Draw(box)
        d.rounded_rectangle((p, p, p + EW - 1, p + BAR), 18, fill=ED_BAR)
        d.rectangle((p, p + BAR - 18, p + EW - 1, p + BAR), fill=ED_BAR)
        x = p + 14
        tf = font(25, "medium")
        for name in st.tabs:
            tw = int(D.width(name, tf)) + 52
            active = name == st.active
            if active:
                d.rectangle((x, p + 8, x + tw, p + BAR), fill=ED_BG)
                d.rectangle((x, p + 8, x + tw, p + 11), fill=BLUE)
            d.text((x + 26, p + BAR / 2 + 4), name, font=tf, fill=WHITE if active else ED_GUTTER, anchor="lm")
            x += tw + 4
        if st.active:
            self._code(box, d, p, st, cursor)
        box.info["pad"] = p
        return box

    def _code(self, box, d, p, st: State, cursor: bool):
        CODE_PX, CODE_LH = self.stage.code_px, self.stage.code_lh
        f, fz = mono(CODE_PX), font(CODE_PX)
        adv = f.getlength("M")
        text = st.text(st.active)
        cols = colours(st.active, text)
        lines = text.split("\n")
        rows = (PH - BAR - 30) // CODE_LH
        cl = text.count("\n", 0, st.cursor)
        mark = st.mark if st.mark and st.mark[0] == st.active else None
        focus_line = (mark[1] - 1) if mark and st.focus != "editor" else cl
        top = max(0, min(len(lines) - rows, focus_line - rows + 3)) if len(lines) > rows else 0
        if mark and mark[1] - 1 < top:
            top = mark[1] - 1
        gx, cx, y0 = p + 16, p + 92, p + BAR + 22
        starts = [0]
        for l in lines[:-1]:
            starts.append(starts[-1] + len(l) + 1)
        for r in range(min(rows, len(lines) - top)):
            ln = top + r
            y = y0 + r * CODE_LH
            marked = mark and mark[1] <= ln + 1 <= mark[2]
            if marked:
                d.rectangle((p + 6, y - 4, p + self.stage.ew - 7, y + CODE_LH - 6), fill=MARK_BG)
                d.rectangle((p + 6, y - 4, p + 11, y + CODE_LH - 6), fill=AMBER)
            elif cursor and ln == cl and not mark and st.focus == "editor":
                d.rectangle((p, y - 4, p + self.stage.ew - 1, y + CODE_LH - 6), fill=ED_CURRENT)
            dim = bool(mark) and not marked
            d.text((gx + 56, y), str(ln + 1), font=mono(24), fill=ED_GUTTER, anchor="ra")
            line, off = lines[ln], starts[ln]
            if st.sel:
                a, b = max(st.sel[0], off), min(st.sel[1], off + len(line))
                if a < b:
                    xa = cx + _cols(line[: a - off]) * adv
                    xb = cx + _cols(line[: b - off]) * adv
                    d.rectangle((xa, y - 4, xb, y + CODE_LH - 6), fill=SEL_BG)
            col = 0
            right = p + self.stage.ew - 16           # long lines are cut at the panel edge
            for k, ch in enumerate(line):
                if cx + (col + 1) * adv > right:
                    break
                c = cols[off + k] if off + k < len(cols) else ED_TEXT
                if dim:
                    c = tuple(int(v * 0.42 + bg * 0.58) for v, bg in zip(c, ED_BG))
                if CJK.match(ch) or ord(ch) > 0x2E7F:
                    d.text((cx + col * adv, y - 2), ch, font=fz, fill=c)
                    col += 2
                else:
                    if not ch.isspace():
                        d.text((cx + col * adv, y), ch, font=f, fill=c)
                    col += 1
            if cursor and ln == cl and st.focus == "editor":
                xc = cx + _cols(line[: st.cursor - off]) * adv
                d.rectangle((xc, y - 2, xc + 3, y + CODE_LH - 8), fill=(82, 139, 255))

    def _terminal(self, st: State, cursor: bool) -> Image.Image:
        TW = self.stage.tw
        box = D.shadow_box(TW, PH, 18, TERM_BG, blur=20, shadow=(0, 0, 0, 120))
        p = box.info["pad"]
        d = ImageDraw.Draw(box)
        d.rounded_rectangle((p, p, p + TW - 1, p + BAR), 18, fill=(30, 35, 44))
        d.rectangle((p, p + BAR - 18, p + TW - 1, p + BAR), fill=(30, 35, 44))
        for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
            d.ellipse((p + 24 + i * 30, p + 20, p + 40 + i * 30, p + 36), fill=c)
        d.text((p + TW / 2, p + BAR / 2), "Terminal — bash", font=font(24, "medium"), fill=TERM_DIM, anchor="mm")
        f, fb, fz = mono(TERM_PX), mono(TERM_PX, bold=True), font(TERM_PX)
        adv = f.getlength("M")
        max_cols = int((TW - 48) // adv)
        rows: list[list[tuple[str, tuple, bool]]] = []
        cmd_row = 0
        found = None
        for ln in st.term:
            segs = ((("$ ", TERM_PROMPT, True), (ln.text, TERM_TEXT, False)) if ln.kind == "cmd" else ansi(ln.text))
            if ln.kind == "cmd":
                cmd_row, found = len(rows), None
            elif (isinstance(st.scroll_top, str) and found is None
                  and st.scroll_top in "".join(t for t, _, _ in segs)):
                found = len(rows)
            rows += _wrap_segments(segs, max_cols)
        if st.busy:
            if not (st.term and st.term[-1].kind == "part"):
                rows.append([])
        else:
            rows += _wrap_segments((("$ ", TERM_PROMPT, True), (st.typing, TERM_TEXT, False)), max_cols)
        fit = (PH - BAR - 32) // TERM_LH
        if st.scroll_top:
            start = found if isinstance(st.scroll_top, str) and found is not None else cmd_row
            rows, cursor = rows[start: start + fit], False
        else:
            rows = rows[-fit:]
        y0 = p + BAR + 20
        for r, row in enumerate(rows):
            col = 0
            y = y0 + r * TERM_LH
            for txt, c, bold in row:
                for ch in txt:
                    x = p + 24 + col * adv
                    if CJK.match(ch) or ord(ch) > 0x2E7F:
                        d.text((x, y - 2), ch, font=fz, fill=c)
                        col += 2
                    else:
                        if not ch.isspace():
                            d.text((x, y), ch, font=fb if bold else f, fill=c)
                        col += 1
            if r == len(rows) - 1 and cursor:
                x = p + 24 + col * adv
                d.rectangle((x + 1, y - 1, x + adv, y + TERM_PX + 3), fill=(200, 208, 218))
        box.info["pad"] = p
        return box


def _wrap_segments(segs, max_cols: int) -> list[list[tuple[str, tuple, bool]]]:
    rows, row, n = [], [], 0
    for txt, c, b in segs:
        buf = ""
        for ch in txt:
            w = 2 if (CJK.match(ch) or ord(ch) > 0x2E7F) else 1
            if n + w > max_cols:
                row.append((buf, c, b))
                rows.append(row)
                row, buf, n = [], "", 0
            buf += ch
            n += w
        if buf:
            row.append((buf, c, b))
    rows.append(row)
    return rows


@lru_cache(maxsize=64)
def _note_img(text: str, w: int) -> Image.Image:
    t = D.text_img(text, font(36, "medium"), INK, max_w=w - 80, line_h=1.4)
    h = t.height + 48
    box = D.shadow_box(w, h, 20, WHITE, blur=16, shadow=(0, 0, 0, 110))
    p = box.info["pad"]
    ImageDraw.Draw(box).rounded_rectangle((p, p, p + 10, p + h - 1), 5, fill=AMBER)
    box.alpha_composite(t, (p + 42, p + 22))
    box.info["pad"] = p
    return box
