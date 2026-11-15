#!/usr/bin/env python3
"""Video 123 (syllabus 10.6): 用第三方庫

CMake's FetchContent downloads nlohmann/json 3.11.3 at configure time (the real configure says
"Using the multi-header code from /work/build/_deps/json-src/include/"), target_link_libraries
connects it, and the program reads scores.json: class 2A, Amy 72, Ben 91, total 163.
Run `python3 video123.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 123
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-06"
FILES = {f: (CODE / f).read_text() for f in ["CMakeLists.txt", "scores.json", "main.cpp"]}
CHALLENGE = (CODE / "challenge.cpp").read_text()

(conf, bld, run, cch, rch) = cpp.session(FILES, [
    "cmake -S . -B build -Wno-dev", "cmake --build build", "./build/scores",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -I build/_deps/json-src/include challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert "Using the multi-header code from /work/build/_deps/json-src/include/" in conf.output, conf.output
assert "Built target scores" in bld.output and run.output == "class 2A\nAmy 72\nBen 91\ntotal 163\n", run.output
assert cch.code == 0 and '"name": "Cat"' in rch.output

SAY = {"FetchContent": "Fetch Content", "FetchContent_Declare": "Fetch Content declare", "FetchContent_MakeAvailable": "Fetch Content make available",
       "target_link_libraries": "target link libraries", "nlohmann/json": "n lohmann json", "nlohmann": "n lohmann", "JSON": "jason",
       "json": "jason", "scores.json": "scores 點 jason", "json::parse": "jason parse", "CMake": "C make", "cmake": "C make",
       "dump(2)": "dump 二", "vcpkg": "v c p k g", "Conan": "Conan"}

s = Stage(FILES, title="用第三方庫", code_px=22, split=0.5)

scenes = [
    Scene("intro",
          "歡迎返嚟！好多嘢唔使自己由零寫，例如讀 JSON，網上已經有好出名嘅庫。今集用 CMake 嘅 FetchContent，自動下載 nlohmann json，再喺程式入面用。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "FetchContent · nlohmann/json")),
    Scene("goal",
          "今集會講：[[b1]]JSON 檔係乜；[[b2]]FetchContent 下載第三方庫；[[b3]]target_link_libraries 連接；[[b4]]用 json 讀資料。",
          BulletCard("今集學識", [("JSON", "b1"), ("FetchContent", "b2"), ("target_link_libraries", "b3"), ("json::parse", "b4")])),
    Scene("json",
          "[[open]]scores.json：大括號係物件，入面有 class 同 students；[[arr]]中括號係陣列，每個學生有 name 同 mark。好多網站同設定檔都用呢種格式。",
          s.scene(Open("scores.json", at="open"), Mark(2, at="open"), Mark((3, 6), at="arr"))),
    Scene("cmake",
          "[[open]]CMakeLists.txt：[[fetch]]include FetchContent，Declare 一個叫 json 嘅依賴，俾佢下載網址；[[make]]MakeAvailable 真正下載同準備；[[link]]最後 target_link_libraries，"
          "將 scores 同 json 庫連埋，header 嘅路徑亦會自動加好。",
          s.scene(Mark(None), Open("CMakeLists.txt", at="open"), Mark((5, 7), at="fetch"), Mark(8, at="make"), Mark((10, 11), at="link"))),
    Scene("code",
          "[[open]]main.cpp include nlohmann json.hpp，[[alias]]用 using 改個短名。[[parse]]json::parse 讀成個檔；[[get]]用中括號攞 class，直接放入 string；"
          "[[loop]]students 可以好似 vector 咁逐個行。",
          s.scene(Mark(None), Open("main.cpp", at="open"), Mark(4, at="open"), Mark(6, at="alias"), Mark(10, at="parse"), Mark((11, 12), at="get"),
                  Mark((14, 19), at="loop"))),
    Scene("build",
          "[[conf]]configure：今次 CMake 會上網下載 json，用嘅係佢嘅 header。[[bld]]build，[[run]]運行：class 2A，Amy 七十二，Ben 九十一，總分一百六十三。",
          s.scene(Mark(None), Run(conf, at="conf"), Run(bld, at="bld"), Run(run, at="run"))),
    Scene("ways",
          "攞第三方庫有幾種方法：[[fc]]FetchContent，CMake 自己下載；[[pm]]套件管理器，例如 vcpkg 同 Conan；[[sys]]用系統裝好嘅。細項目用 FetchContent 最簡單。",
          TableCard("點樣用第三方庫", ["方法", "特點"], [
              (["FetchContent", "寫喺 CMakeLists，自動下載"], "fc", GREEN),
              (["vcpkg / Conan", "套件管理器，庫好多"], "pm"),
              (["系統安裝（apt、brew）", "每部機要自己裝"], "sys"),
          ], widths=[1.4, 1.6], code_cols=(), size=38)),
    Scene("recap",
          "總結：[[r1]]JSON 用大括號同中括號表示資料；[[r2]]FetchContent_Declare 同 MakeAvailable 下載庫；[[r3]]target_link_libraries 連接；[[r4]]json::parse 讀，中括號攞值。",
          BulletCard("今集重點", [("JSON 格式", "r1"), ("FetchContent", "r2"), ("target_link_libraries", "r3"), ("json::parse、data[\"key\"]", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]反過嚟，用 json 砌一個學生：name、mark 同一個 tags 陣列，用 dump 二印出漂亮嘅 JSON。[[next]]下一集：效能入門。多謝收睇，下次見！",
          EndCard("建立 json out：out[\"name\"] = \"Cat\"、out[\"mark\"] = 85、out[\"tags\"] = {\"new\", \"2A\"}，再印 out.dump(2)。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
