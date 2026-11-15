#!/usr/bin/env python3
"""Video 116 (syllabus 9.8): std::filesystem

A photos/ folder with cat.jpg, dog.png and 2025/beach.jpg (`ls -R photos` really lists it).
fs::path joins with / (photos/2025/beach.jpg), gives filename beach.jpg and extension .jpg;
fs::exists answers 1 and 0. A recursive_directory_iterator walk really prints each file with its
size and the total, 5003 bytes. Run `python3 video116.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 116
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-08"
FINAL = (CODE / "folder.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
PHOTOS = {f"photos/{n}": (CODE / "photos" / n).read_text() for n in ["cat.jpg", "dog.png", "2025/beach.jpg"]}
WALK = "    std::uintmax_t total" + FINAL.split("    std::uintmax_t total")[1].rsplit("}\n", 1)[0]
V1 = FINAL.replace(WALK, "").replace("#include <cstdint>\n", "")
CC = "g++ -std=c++20 -Wall -Wextra folder.cpp -o fd"

(ls, c1, r1, clr, c2, r2, cch, rch) = cpp.session({"folder.cpp": V1, **PHOTOS}, [
    "ls -R photos", CC, "./fd", "clear", Write("folder.cpp", FINAL), CC, "./fd",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
HEAD = "photos/2025/beach.jpg\nbeach.jpg .jpg\n1 0\n"
assert "beach.jpg" in ls.output and r1.output == HEAD, r1.output
lines = r2.output.split("\n")
assert r2.output.startswith(HEAD) and sorted(lines[3:6]) == ["photos/2025/beach.jpg 3001", "photos/cat.jpg 1201", "photos/dog.png 801"], r2.output
assert lines[6] == "total 5003 bytes" and c1.code == c2.code == cch.code == 0 and rch.output == "2\n"

SAY = {"std::filesystem": "S T D filesystem", "filesystem": "filesystem", "fs::path": "f s path", "fs": "f s", "namespace fs": "namespace f s",
       "filename()": "filename", "extension()": "extension", "fs::exists": "f s exists", "exists": "exists",
       "recursive_directory_iterator": "recursive directory iterator", "file_size()": "file size", "is_regular_file()": "is regular file",
       "std::uintmax_t": "u int max t", "photos": "photos", "beach.jpg": "beach 點 j p g", ".jpg": "點 j p g", "ls -R": "l s 大 R"}

s = Stage({"folder.cpp": V1}, title="std::filesystem", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！想知一個資料夾有幾大、入面有乜檔案、某個檔存唔存在？以前要靠作業系統自己嘅函數，C++17 開始有 std::filesystem，邊度都用得。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "path · exists · 計資料夾大小")),
    Scene("goal",
          "今集會講：[[b1]]path 同斜線組合；[[b2]]檔名同副檔名；[[b3]]exists；[[b4]]逐個行資料夾，計總大小。",
          BulletCard("今集學識", [("fs::path、/", "b1"), ("filename()、extension()", "b2"), ("fs::exists", "b3"), ("recursive_directory_iterator", "b4")])),
    Scene("ls",
          "[[ls]]先睇吓資料夾：photos 入面有 cat.jpg、dog.png，仲有一個 2025 資料夾，入面有 beach.jpg。",
          s.scene(Open("folder.cpp", mode="instant"), Run(ls, at="ls"))),
    Scene("path",
          "[[alias]]filesystem 個名好長，用 namespace fs 做簡稱。[[join]]path 用斜線砌：photos 斜線 2025 斜線 beach.jpg。[[parts]]filename 係檔名，extension 係副檔名；"
          "[[ex]]exists 問存唔存在。[[cc]]編譯運行：[[o]]路徑、beach.jpg、點 j p g；存在係一，nope 係零。斜線自動幫你加分隔符號。",
          s.scene(Mark(4, at="alias"), Mark((7, 8), at="join"), Mark((10, 11), at="parts"), Mark((12, 13), at="ex"),
                  Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("walk",
          "[[type]]計資料夾大小：recursive_directory_iterator 會行晒入面所有嘢，包括子資料夾。[[file]]係普通檔案，就印路徑同大小，加落 total。[[cc]]運行：[[o]]三個檔，"
          "連 2025 入面嗰個都搵到；總共五千零三 byte。次序係檔案系統決定嘅，唔保證。",
          s.scene(Run(clr, at="type"), Replace("folder.cpp", "#include <filesystem>\n", "#include <cstdint>\n#include <filesystem>\n", at="type", rate=40),
                  Type("folder.cpp", WALK, before="}", last=True, rate=70), Expect("folder.cpp", FINAL), Mark(16, at="type"), Mark((17, 21), at="file"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("api",
          "常用嘅仲有：[[mk]]create_directories 開資料夾；[[cp]]copy 同 rename；[[rm]]remove 刪檔。[[err]]呢啲出錯會 throw filesystem_error。",
          TableCard("std::filesystem 常用", ["函數", "做乜"], [
              (["fs::create_directories(p)", "開資料夾（連中間嗰啲）"], "mk"),
              (["fs::copy / fs::rename", "複製 / 改名"], "cp"),
              (["fs::remove(p)", "刪走"], "rm"),
              (["出錯", "throw fs::filesystem_error"], "err", AMBER),
          ], widths=[1.6, 1.6], code_cols=(0,), size=36)),
    Scene("recap",
          "總結：[[r1]]fs::path 用斜線組合，有 filename 同 extension；[[r2]]exists 問存唔存在；[[r3]]recursive_directory_iterator 行晒成個資料夾；[[r4]]file_size 攞大小。",
          BulletCard("今集重點", [("path / \"x\"、filename、extension", "r1"), ("fs::exists", "r2"), ("recursive_directory_iterator", "r3"), ("file_size()", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]數 photos 入面，連子資料夾，有幾多個 jpg 檔。[[next]]下一集：第九部分嘅小項目，記帳簿。多謝收睇，下次見！",
          EndCard("行晒 photos（連子資料夾），數 extension() == \".jpg\" 嘅檔案：答案 2。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
