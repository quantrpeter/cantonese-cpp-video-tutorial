#!/usr/bin/env python3
"""Video 125 (syllabus 10.8): C++20 modules 簡介

A module `mathx` exports square() but not helper(). With GCC 15 (-std=c++20 -fmodules):
compiling main.cpp first really fails ("failed to read compiled module ... imports must be built
before being imported"); compiling mathx.cpp first creates gcm.cache/mathx.gcm, then main builds,
links and prints 49. Calling the unexported helper is a real "'helper' was not declared" error.
Run `python3 video10.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 125
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-08"
FILES = {f: (CODE / f).read_text() for f in ["mathx.cpp", "main.cpp"]}
CHALLENGE = (CODE / "challenge.cpp").read_text()

(first, cm, ls, cmain, link, run, clr, cch) = cpp.session(FILES, [
    "g++ -std=c++20 -fmodules -c main.cpp", "g++ -std=c++20 -fmodules -c mathx.cpp", "ls gcm.cache",
    "g++ -std=c++20 -fmodules -c main.cpp", "g++ main.o mathx.o -o app", "./app", "clear",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -fmodules -c challenge.cpp",
], refresh=opts.fresh_runs, cols=58)
assert "failed to read compiled module" in cpp.visible(first.output) and first.code != 0
assert ls.output.strip() == "mathx.gcm" and cm.code == cmain.code == link.code == 0 and run.output == "49\n"
assert "'helper' was not declared in this scope" in cpp.visible(cch.output)

SAY = {"module": "module", "modules": "modules", "export module": "export module", "export": "export", "import": "import",
       "mathx": "math x", "-fmodules": "f modules", "gcm.cache": "g c m 點 cache", "mathx.gcm": "math x 點 g c m", "#include": "include",
       "square": "square", "helper": "helper", "import std": "import std", "header": "header", "CMake": "C make"}

s = Stage(FILES, title="C++20 modules 簡介", code_px=26, split=0.5)

scenes = [
    Scene("intro",
          "歡迎返嚟！第十部分最後一集。include 其實係將成個 header 貼入嚟，好慢，又會互相影響。C++20 有一個新做法：modules。今集簡單介紹，同埋講吓而家嘅支援程度。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "export module · import · GCC 15")),
    Scene("goal",
          "今集會講：[[b1]]寫一個 module；[[b2]]export 決定俾人睇嘅嘢；[[b3]]import 同編譯次序；[[b4]]而家用唔用得。",
          BulletCard("今集學識", [("export module mathx;", "b1"), ("export：公開", "b2"), ("import + 編譯次序", "b3"), ("支援程度", "b4")])),
    Scene("module",
          "[[decl]]mathx.cpp 第一行：export module mathx，宣告呢個檔係一個叫 mathx 嘅 module。[[help]]helper 冇 export，只係 module 自己用；[[sq]]square 有 export，外面先用得。",
          s.scene(Open("mathx.cpp", at="decl"), Mark(1, at="decl"), Mark((3, 5), at="help"), Mark((7, 9), at="sq"))),
    Scene("import",
          "[[open]]main.cpp 用 import mathx，代替 include。[[cc]]用 D f modules 編譯 main：[[err]]錯誤：搵唔到已編譯嘅 module，imports 一定要先編譯。",
          s.scene(Mark(None), Open("main.cpp", at="open"), Mark(2, at="open"), Mark(None, at="cc"), Run(first, at="cc"))),
    Scene("order",
          "[[m]]所以要先編譯 mathx.cpp，[[ls]]佢會喺 gcm.cache 入面產生 mathx.gcm，即係 module 嘅編譯結果。[[main]]再編譯 main，佢會讀 mathx.gcm，唔使再處理一次 module 嘅源碼；之後連結兩個 o 檔，[[run]]運行：四十九，七嘅平方。",
          s.scene(Run(clr, at="m"), Run(cm), Run(ls, at="ls"), Run(cmain, at="main"), Run(link), Run(run, at="run"))),
    Scene("vs",
          "同 include 比較：[[paste]]include 每次都貼入成個 header，[[once]]module 只編譯一次；[[leak]]include 嘅 macro 同所有名都會漏出嚟，module 只會公開 export 嘅嘢。",
          TableCard("#include vs module", ["", "#include", "import"], [
              (["編譯", "每個 .cpp 重新處理", "編譯一次，重用"], "paste"),
              (["俾人見到", "全部（連 macro）", "只有 export 嘅"], "leak", GREEN),
              (["次序", "唔理", "module 要先編譯"], "once", AMBER),
          ], widths=[0.8, 1.4, 1.4], code_cols=(), size=38)),
    Scene("state",
          "而家用唔用得？[[gcc]]GCC 十五、Clang、MSVC 都已經支援，但係要加選項；[[build]]build system 要識排編譯次序，CMake 新版本先支援；[[std]]import std 仲未係所有地方都方便。"
          "[[advice]]學習同新項目可以試；大型舊項目，大部分仲係用 include。",
          BulletCard("支援程度", [("編譯器：支援，要加選項", "gcc"), ("build system：要新版本 CMake", "build"), ("import std：未普及", "std"),
                              ("新項目可以試，舊項目多數仲用 #include", "advice")])),
    Scene("recap",
          "總結：[[r1]]export module 宣告一個 module；[[r2]]只有 export 嘅嘢外面先見到；[[r3]]import 之前，module 要先編譯；[[r4]]支援越嚟越好，但係仲未完全普及。",
          BulletCard("今集重點", [("export module 名;", "r1"), ("export：公開", "r2"), ("先編譯 module", "r3"), ("支援：發展中", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]喺 main 試吓叫冇 export 嘅 helper，睇吓編譯器點講。[[next]]下一集開始第十一部分：並行，第一集係 thread 同 jthread。多謝收睇，下次見！",
          EndCard("喺 main 叫 helper(7)：佢冇 export，編譯器會話 'helper' was not declared。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
