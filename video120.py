#!/usr/bin/env python3
"""Video 120 (syllabus 10.3): CMake 入門

3.12's calculator split into main.cpp, calc.h and calc.cpp, described by a CMakeLists.txt
(C++20, one target `calc`, -Wall -Wextra). `cmake -S . -B build` really configures (GNU 15.3.0),
`cmake --build build` really compiles both files and links; ./build/calc gives = 7 and
"Cannot divide by 0". After `touch calc.cpp` the rebuild really recompiles only calc.cpp.
Run `python3 video120.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 120
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-03"
FILES = {f: (CODE / f).read_text() for f in ["CMakeLists.txt", "main.cpp", "calc.h", "calc.cpp"]}
CHECK = (CODE / "check.cpp").read_text()
CM2 = FILES["CMakeLists.txt"] + (CODE / "challenge.txt").read_text()

(conf, bld, run, clr, touch, rebuild, wb, rc) = cpp.session(FILES, [
    "cmake -S . -B build", "cmake --build build", Input("./build/calc", ["3 + 4", "8 / 0", "q"]), "clear", "touch calc.cpp", "cmake --build build",
    Write("check.cpp", CHECK), Write("CMakeLists.txt", CM2), "cmake --build build", "./build/check",
], refresh=opts.fresh_runs, cols=48)
assert "GNU 15.3.0" in conf.output and "Build files have been written to: /work/build" in conf.output
assert "main.cpp.o" in bld.output and "calc.cpp.o" in bld.output and "Built target calc" in bld.output
assert run.output == "a op b (q to quit)\n3 + 4\n= 7\n8 / 0\nCannot divide by 0\nq\n", run.output
assert "calc.cpp.o" in rebuild.output and "main.cpp.o" not in rebuild.output
assert "Built target check" in wb.output and rc.output == "ok\n"

SAY = {"CMake": "C make", "cmake": "C make", "CMakeLists.txt": "C make lists 點 t x t", "cmake -S . -B build": "C make 大 S 點 大 B build",
       "cmake --build build": "C make build build", "add_executable": "add executable", "target_compile_options": "target compile options",
       "CMAKE_CXX_STANDARD": "C make CXX standard", "project": "project", "target": "target", "build": "build", "touch": "touch",
       "calc.h": "calc 點 h", "calc.cpp": "calc 點 c p p", "main.cpp": "main 點 c p p", "Makefile": "Make file", "Ninja": "Ninja",
       "check": "check", "cmake_minimum_required": "C make minimum required"}

s = Stage(FILES, title="CMake 入門", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！檔案一多，每次都要打長長嘅 g++ 指令，邊個檔改咗，又要自己記住重新編譯邊啲。真正嘅項目會用 build system，最流行嘅就係 CMake。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "CMakeLists.txt · build · target")),
    Scene("goal",
          "今集會講：[[b1]]將計數機拆成幾個檔；[[b2]]寫 CMakeLists.txt；[[b3]]configure 同 build 兩步；[[b4]]只重新編譯改咗嘅檔。",
          BulletCard("今集學識", [("拆開 3.12 計數機", "b1"), ("CMakeLists.txt", "b2"), ("cmake -S . -B build；cmake --build build", "b3"), ("增量編譯", "b4")])),
    Scene("split",
          "[[h]]3.12 嘅計數機拆開咗：calc.h 宣告兩個函數；[[cpp]]calc.cpp 寫佢哋嘅內容；[[main]]main.cpp 負責讀輸入同印結果。同 3.10 嘅做法一樣。",
          s.scene(Open("calc.h", at="h"), Mark((3, 4), at="h"), Open("calc.cpp", at="cpp"), Mark((3, 20), at="cpp"), Open("main.cpp", at="main"),
                  Mark((9, 17), at="main"))),
    Scene("lists",
          "[[open]]CMakeLists.txt 描述成個項目：[[proj]]最少要邊個 CMake 版本，項目叫乜；[[std]]用 C++ 二十；[[target]]add_executable：一個叫 calc 嘅程式，由兩個 cpp 砌成；"
          "[[opt]]再幫佢加警告選項。",
          s.scene(Mark(None), Open("CMakeLists.txt", at="open"), Mark((1, 2), at="proj"), Mark((4, 5), at="std"), Mark(7, at="target"), Mark(8, at="opt"))),
    Scene("configure",
          "第一步 configure：[[cmd]]cmake 大 S 點，即係源碼喺呢度；大 B build，即係所有產生出嚟嘅嘢放入 build 資料夾。[[o]]佢搵到 GNU 十五點三，寫好 build 檔案。",
          s.scene(Mark(None), Run(conf, at="cmd"))),
    Scene("build",
          "第二步 build：[[cmd]]cmake 雙減號 build build。[[o]]佢逐個編譯 main.cpp 同 calc.cpp，再連結成 calc。[[run]]運行 build 入面嘅 calc：三加四等於七；八除零，唔得；q 離開。同 3.12 一樣。",
          s.scene(Run(bld, at="cmd"), Run(run, at="run", type_rate=24))),
    Scene("incremental",
          "[[touch]]用 touch 扮改咗 calc.cpp。[[cmd]]再 build：[[o]]今次只係重新編譯 calc.cpp，main.cpp 冇改，唔使再編譯。項目大嘅時候，可以慳好多時間。",
          s.scene(Run(clr, at="touch"), Run(touch), Run(rebuild, at="cmd"))),
    Scene("terms",
          "幾個名詞：[[t]]target 係要整出嚟嘅嘢，例如一個程式；[[src]]源碼資料夾同 build 資料夾分開，想重新嚟過，刪走 build 就得；[[two]]configure 只係改咗 CMakeLists 先要再做，"
          "平時淨係 build。",
          TableCard("CMake 名詞", ["名詞", "意思"], [
              (["target", "要整嘅嘢：add_executable(calc …)"], "t"),
              (["build 資料夾", "產生嘅嘢全部喺度，唔污染源碼"], "src"),
              (["configure / build", "cmake -S . -B build / cmake --build build"], "two"),
          ], widths=[1, 2.2], code_cols=(), size=34)),
    Scene("recap",
          "總結：[[r1]]CMakeLists.txt 描述項目同 target；[[r2]]configure 一次，產生 build 檔案；[[r3]]cmake build 負責編譯同連結；[[r4]]只會重新編譯改咗嘅檔。",
          BulletCard("今集重點", [("CMakeLists.txt + add_executable", "r1"), ("cmake -S . -B build", "r2"), ("cmake --build build", "r3"), ("增量編譯", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 check.cpp 測試 calculate，喺 CMakeLists 加多一個叫 check 嘅 target，build 完運行睇吓係咪 ok。[[next]]下一集：用 gdb debug。多謝收睇，下次見！",
          EndCard("寫 check.cpp 測試 calculate；CMakeLists.txt 加一個 target：add_executable(check check.cpp calc.cpp)，再 build 同運行。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
