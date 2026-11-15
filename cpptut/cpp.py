"""Runs the programs shown in a video, for real, in the pinned GCC container (docker/Dockerfile).

Results are cached in build/runs/ by the files, commands and image, so a rerun of a video does
not need Docker unless its code changed. `refresh=True` (or --fresh-runs) runs them again.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .style import ROOT
from .syntax import visible

DOCKER_DIR = ROOT / "docker"
RUNS = ROOT / "build" / "runs"


@dataclass
class Result:
    cmd: str
    output: str     # stdout and stderr together, as the terminal shows them (typed input included)
    seconds: float  # wall time inside the container
    code: int
    io: list | None = None  # Input runs: [kind, text, seconds after start], kind "o" (output) or "i" (typed)

    @property
    def real(self) -> float | None:
        """The `real` line printed by bash's `time`, in seconds."""
        m = re.search(r"real\s+(\d+)m([\d.]+)s", self.output)
        return int(m.group(1)) * 60 + float(m.group(2)) if m else None


def image() -> str:
    """The image tag, derived from the Dockerfile so that edits rebuild it."""
    h = hashlib.sha256((DOCKER_DIR / "Dockerfile").read_bytes()).hexdigest()[:10]
    return f"hkps-cpp:{h}"


def ensure_image() -> str:
    tag = image()
    if not shutil.which("docker"):
        raise SystemExit("cpptut: Docker is needed to run the C++ programs (install Docker Desktop)")
    ok = subprocess.run(["docker", "info"], capture_output=True)
    if ok.returncode:
        raise SystemExit("cpptut: Docker is not running. Start Docker Desktop and try again.")
    have = subprocess.run(["docker", "image", "inspect", tag], capture_output=True)
    if have.returncode:
        print(f"[cpp] building {tag} from docker/Dockerfile (first time only)…", flush=True)
        subprocess.run(["docker", "build", "-t", tag, str(DOCKER_DIR)], check=True)
    return tag


@dataclass
class Write:
    """A step that (re)writes a file between commands, e.g. the program after an edit on camera."""
    name: str
    text: str


@dataclass
class Input:
    """A command run in a pseudo-terminal while a person types `lines` into it.

    Each line is typed when the program goes quiet (it is waiting for input), so the transcript
    shows it in the right place, the way a terminal echoes it. "^C" presses Ctrl+C and "^D" sends
    end of input; give (text, seconds) to type at a fixed time instead, e.g. ("^C", 1.5) to stop a
    program that never goes quiet. A dict {"bisect": [1, 100], "big": "Too big", "small": "Too small"}
    plays a guessing game to the end: it guesses the middle and halves the range after each reply. The output is recorded with its timing, so `Run` can replay it
    at the real pace (a countdown, an endless loop scrolling by).
    """
    cmd: str
    lines: tuple = ()


# Runs inside the container: python3 .drive.py <command file> <input json> <cols> > <io json>
DRIVER = r'''
import codecs, fcntl, json, os, pty, select, signal, struct, sys, termios, time
cmd = open(sys.argv[1]).read()
feed = json.load(open(sys.argv[2]))
cols = int(sys.argv[3])
pid, fd = pty.fork()
if pid == 0:
    a = termios.tcgetattr(0)
    a[3] &= ~(termios.ECHO | termios.ECHOCTL)
    termios.tcsetattr(0, termios.TCSANOW, a)
    fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack("HHHH", 40, cols, 0, 0))
    os.execvp("bash", ["bash", "-c", cmd])
segs, dec, t0 = [], codecs.getincrementaldecoder("utf-8")("replace"), time.time()
last, k = t0, 0
def add(kind, text):
    now = round(time.time() - t0, 3)
    if segs and segs[-1][0] == kind and now - segs[-1][2] < 0.03:
        segs[-1][1] += text
        return
    if segs and segs[-1][0] == "o" and segs[-1][1].count("\n") > 200:   # a flood: only its newest lines can
        head, _, rest = segs[-1][1].partition("\n")                     # be on screen (keep the end of the
        segs[-1][1] = head + "\n" + "\n".join(rest.split("\n")[-60:])   # line the chunk before started)
    segs.append([kind, text, now])
while True:
    r, _, _ = select.select([fd], [], [], 0.02)
    if r:
        try:
            data = os.read(fd, 65536)
        except OSError:
            data = b""
        if not data:
            break
        add("o", dec.decode(data))
        last = time.time()
    now = time.time()
    if k < len(feed):
        text, at = feed[k]
        if isinstance(text, dict):            # a player who halves the range after each reply
            if now - last >= 0.35:
                b = text
                if "g" not in b:
                    b["lo_"], b["hi_"] = b["bisect"]
                else:
                    seen = "".join(x for kk, x, _ in segs if kk == "o")[b["mark"]:]
                    if b["big"] in seen:
                        b["hi_"] = b["g"] - 1
                    elif b["small"] in seen:
                        b["lo_"] = b["g"] + 1
                b["g"] = (b["lo_"] + b["hi_"]) // 2
                b["mark"] = len("".join(x for kk, x, _ in segs if kk == "o"))
                os.write(fd, f"{b['g']}\n".encode())
                add("i", f"{b['g']}\n")
                last = time.time()
        elif (now - last >= 0.35) if at is None else (now - t0 >= at):
            if text == "^C":
                os.write(fd, b"\x03")
                add("i", "^C")
            elif text == "^D":
                os.write(fd, b"\x04")
                add("i", "")
            else:
                os.write(fd, (text + "\n").encode())
                add("i", text + "\n")
            last, k = time.time(), k + 1
    if now - t0 > 40:
        os.kill(pid, 9)
segs = [sg for sg in segs if sg[1] or sg[0] == "i"]
stops = [i for i, sg in enumerate(segs) if sg[:2] == ["i", "^C"]]
if stops and all(sg[0] == "o" for sg in segs[stops[-1] + 1:]):   # show ^C after what was already on its way
    c = segs.pop(stops[-1])
    c[2] = segs[-1][2] if segs else c[2]
    segs.append(c)
_, status = os.waitpid(pid, 0)
code = os.waitstatus_to_exitcode(status)
if code < 0 and -code != signal.SIGINT:      # bash names the signal that killed the program
    segs.append(["o", ("" if not segs or segs[-1][1].endswith("\n") else "\n") + signal.strsignal(-code) + "\n",
                 round(time.time() - t0, 3)])
json.dump({"io": segs, "code": 128 - code if code < 0 else code, "seconds": round(time.time() - t0, 3)},
          sys.stdout, ensure_ascii=False)
'''


def _text(s: str) -> str:
    return s if s.endswith("\n") else s + "\n"


# A crash reported by the non-interactive bash that runs each command (".c1.sh: line 1:  21 Aborted  ./a")
# is shown the way an interactive bash reports it to a student: just "Aborted".
_CRASH = re.compile(r"^\.c\d+\.sh: line \d+: +\d+ (.+?) {2,}\S.*$", re.M)


def _clean(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "").replace("\x00", "")   # a terminal shows NUL as nothing
    return _CRASH.sub(r"\1", s)


def session(files: dict[str, str], steps: list, refresh: bool = False, tty: bool = True,
            cols: int = 60) -> list[Result]:
    """Writes `files` into an empty folder, then runs the steps there in order.

    Steps are shell commands (str), Input(cmd, lines) for a program a person types into, or
    Write(name, text). Returns one Result per command.
    With tty=True each command runs in a pseudo-terminal (`script`), so g++ prints its colours
    and `ls` lays out columns `cols` wide, exactly as a student's terminal shows them.
    """
    tag = image()
    plain = all(isinstance(s, str) for s in steps)
    def enc(s):
        if isinstance(s, str):
            return s
        if isinstance(s, Input):
            return {"input": s.cmd, "lines": [list(x) if isinstance(x, tuple) else x for x in s.lines]}
        return {"write": s.name, "text": s.text}
    spec = [tag, files, steps] if plain and not tty else [tag, files, [enc(s) for s in steps], tty, cols]
    if any(isinstance(s, Input) for s in steps):
        spec.append(hashlib.sha256(DRIVER.encode()).hexdigest()[:8])   # a changed driver reruns them
    key = hashlib.sha256(json.dumps(spec, ensure_ascii=False).encode()).hexdigest()[:16]
    cache = RUNS / f"{key}.json"
    if cache.exists() and not refresh:
        return [Result(**r) for r in json.loads(cache.read_text())]
    ensure_image()
    work = RUNS / key
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for name, text in files.items():
        (work / name).parent.mkdir(parents=True, exist_ok=True)   # files may sit in folders
        (work / name).write_text(_text(text))
    script = ["set +e", f"export TERM=xterm-256color GCC_URLS=no COLUMNS={cols} LINES=40"]
    commands, driven = [], set()
    for i, s in enumerate(steps):
        if isinstance(s, Write):
            (work / f".w{i}").write_text(_text(s.text))
            script.append(f"cp .w{i} {s.name}")
            continue
        n = len(commands)
        if isinstance(s, Input):
            commands.append(s.cmd)
            driven.add(n)
            (work / ".drive.py").write_text(DRIVER)
            (work / f".c{n}.sh").write_text(s.cmd + "\n")
            feed = [list(x) if isinstance(x, tuple) else [x, None] for x in s.lines]
            (work / f".f{n}.json").write_text(json.dumps(feed, ensure_ascii=False))
            script.append(f"python3 .drive.py .c{n}.sh .f{n}.json {cols} > .io{n}.json")
            continue
        commands.append(s)
        if tty:
            (work / f".c{n}.sh").write_text(s + "\n")
            run = f'script -qec "bash .c{n}.sh" /dev/null > .out{n} 2>&1'
        else:
            run = f"{{ {s} ; }} > .out{n} 2>&1"
        script.append(f's=$(date +%s.%N); {run}; echo $? > .rc{n}; e=$(date +%s.%N); echo "$s $e" > .t{n}')
    (work / ".run.sh").write_text("\n".join(script) + "\n")
    print(f"[cpp] running {len(commands)} command(s) in {tag}", flush=True)
    subprocess.run(["docker", "run", "--rm", "--cap-add=SYS_PTRACE", "-v", f"{work}:/work", "-w", "/work",
                    tag, "bash", ".run.sh"], check=True)
    out = []
    for n, c in enumerate(commands):
        if n in driven:
            d = json.loads((work / f".io{n}.json").read_text())
            io = [[k, _clean(x), t] for k, x, t in d["io"]]
            out.append(Result(c, "".join(x for _, x, _ in io), d["seconds"], d["code"], io))
            continue
        s, e = (float(x) for x in (work / f".t{n}").read_text().split())
        text = _clean((work / f".out{n}").read_text(errors="replace"))
        out.append(Result(c, text, round(e - s, 3), int((work / f".rc{n}").read_text())))
    cache.write_text(json.dumps([asdict(r) for r in out], ensure_ascii=False, indent=1))
    for r in out:
        shown = r.output.splitlines()
        more = f"      … {len(shown) - 30} more lines\n" if len(shown) > 30 else ""
        print(f"[cpp] $ {r.cmd}  ({r.seconds:.2f}s, exit {r.code})\n" + more
              + "".join(f"      {visible(l)}\n" for l in shown[-30:]), end="")
    return out
