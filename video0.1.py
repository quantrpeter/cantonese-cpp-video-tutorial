#!/usr/bin/env python3
"""Video 1 (syllabus 0.1): C++ 係乜嘢？

What a program is, where C++ came from and where it is used, compiled vs interpreted (with a
real C++ vs Python race in the GCC container), and a map of the course.

    python3 video0.1.py              # -> out/video0.1.mp4 (narration is cached; reruns are quick)
    python3 video0.1.py --draft      # silent, estimated timing, fast: for checking layout
    python3 video0.1.py --stills     # two PNGs per scene in build/video0.1/stills/
    python3 video0.1.py --redo why   # regenerate one scene's narration
    python3 video0.1.py --help
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut import draw as D
from cpptut.style import INK, LINE, ROOT, WHITE, font

N = 1
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)
CODE = ROOT / "code" / "00-01"
CPP = (CODE / "primes.cpp").read_text()
PY = (CODE / "primes.py").read_text()
LIMIT = int(re.search(r"n < (\d+)", CPP).group(1))  # said aloud, so it always matches the code

# The race, run for real (cached in build/runs/ until the code changes).
compile_, run_cpp, run_py = cpp.session(
    {"primes.cpp": CPP, "primes.py": PY},
    ["g++ primes.cpp -o primes", "time ./primes", "time python3 primes.py"],
    refresh=opts.fresh_runs, tty=False,
)
assert compile_.code == 0, compile_.output
count = int(re.search(r"primes: (\d+)", run_cpp.output).group(1))
assert f"primes: {count}" in run_py.output, "C++ and Python disagree"
t_cpp, t_py = run_cpp.real, run_py.real
ratio = t_py / t_cpp


def program_card() -> Card:
    c = Card("程式 = 一連串指令")
    c.add(D.panel(760, 470, "即食麵食譜", ("煲滾水", "落麵", "煮三分鐘", "落調味粉"), numbered=True, size=46),
          120, 262, at="recipe", sound="pop")
    c.add(D.panel(820, 330, "電腦只識 0 同 1", ("10110000 01100001", "11001101 00100001", "01110100 11100011"),
                  mono_lines=True, dark=True, accent=GREEN, size=40), 980, 262, at="binary", sound="pop")
    box = D.shadow_box(820, 230, 26, WHITE, outline=LINE)
    p = box.info["pad"]
    left = D.pill("程式語言", font(44, "bold"), WHITE, BLUE, px=34, py=12)
    right = D.pill("0 同 1", font(44, "bold"), WHITE, GREEN, px=34, py=12)
    box.alpha_composite(left, (p + 60, p + 40))
    box.alpha_composite(right, (p + 820 - 60 - right.width, p + 40))
    a, ax, ay = D.arrow(p + 60 + left.width + 20, p + 40 + left.height / 2,
                        p + 820 - 60 - right.width - 20, p + 40 + left.height / 2, color=INK)
    box.alpha_composite(a, (ax, ay))
    cap = D.text_img("人睇得明　→　電腦做得到", font(34, "medium"), INK)
    box.alpha_composite(cap, (p + (820 - cap.width) // 2, p + 150))
    box.info["pad"] = p
    c.add(box, 980, 640, at="lang", anim="pop", sound="pop")
    return c


def compile_card(with_python: bool) -> FlowCard:
    live = (lambda cue: None) if with_python else (lambda cue: cue)  # C++ row already shown in part two
    rows = [Row("C++", "編譯語言", BLUE, [
        Node("原始碼", "primes.cpp", live("src")),
        Node("編譯器", "g++ 一次過翻譯晒", live("compiler")),
        Node("機器碼程式", "primes", live("exe")),
        Node("運行", "好快！", live("run")),
    ], note="好似成本書預先翻譯好先出版", note_at=live("note"))]
    if with_python:
        rows.append(Row("Python", "直譯語言", TEAL, [
            Node("原始碼", "primes.py", "src"),
            Node("直譯器", "一邊讀一邊做", "interp"),
            Node("運行", "慢啲", "run", col=3),
        ], note="好似即場傳譯", note_at="note"))
    return FlowCard("編譯 vs 直譯", rows)


stage = Stage({"primes.cpp": CPP, "primes.py": PY}, title="實際比較：C++ vs Python")
part_tiles = [(p.num, p.zh, p.en) for p in course.parts()]

scenes = [
    Scene("intro",
          "大家好！歡迎嚟到香港編程學會嘅 C++ 全攻略。呢個係起步篇第一集，我哋先嚟傾吓：C++ 究竟係乜嘢？",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "廣東話教學 · 由零開始")),
    Scene("goal",
          "今集會講四樣嘢：[[b1]]程式同程式語言係乜；[[b2]]C++ 由邊度嚟、用嚟做乜；[[b3]]編譯同直譯有乜分別；[[b4]]仲有成個課程會學啲乜。",
          BulletCard("今集學識", [("程式同程式語言係乜", "b1"), ("C++ 嘅由來同用途", "b2"),
                                ("編譯 vs 直譯", "b3"), ("成個課程會學啲乜", "b4")])),
    Scene("program",
          "程式其實就係一連串指令，好似食譜咁。[[recipe]]例如煮即食麵：煲水、落麵、煮三分鐘、落調味粉，一步跟一步做。"
          "[[binary]]不過電腦本身只識零同一，[[lang]]所以我哋用程式語言，用人睇得明嘅文字寫指令，再轉做電腦明白嘅零同一。",
          program_card()),
    Scene("history",
          "C++ 喺一九七九年開始出現。[[bjarne]]一位丹麥電腦科學家喺貝爾實驗室，將 C 語言加上 class，叫做 C with Classes。"
          "[[rename]]一九八三年正式改名做 C++。[[plus]]兩個加號喺 C 語言入面係「加一」嘅意思，即係 C 語言嘅升級版。"
          "[[std]]後來 C++ 有咗國際標準，而家大約每三年更新一次。",
          TimelineCard("C++ 嘅由來", [
              Event("1979", "C with Classes", "Bjarne Stroustrup\n喺貝爾實驗室開始設計", "bjarne"),
              Event("1983", "改名做 C++", "", "rename"),
              Event("1985", "第一個商業版本", "", ("rename", 1.0)),
              Event("1998", "C++98", "第一個國際標準", "std"),
              Event("2011", "C++11", "現代 C++ 開始", ("std", 0.5)),
              Event("2020", "C++20", "呢個課程用", ("std", 1.0), AMBER),
              Event("2023", "C++23", "每三年一個新版本", ("std", 1.5)),
          ], callout=("C++ ＝ C 加一（升級版）", "plus"))),
    Scene("uses",
          "C++ 喺好多地方都用到：[[t1]]大型遊戲同遊戲引擎，[[t2]]你每日用嘅瀏覽器，[[t3]]作業系統同好多專業軟件，"
          "[[t4]]機械人、汽車同各種電子產品，[[t5]]銀行同金融交易系統，[[t6]]仲有編程比賽，好似 HKOI 同 IOI，好多參加者都係用 C++。",
          TileCard("C++ 喺邊度用？", [
              Tile("🎮", "遊戲", "Unreal Engine 等遊戲引擎", "t1", BLUE),
              Tile("🌐", "瀏覽器", "Chrome、Firefox", "t2", TEAL),
              Tile("💻", "作業系統同軟件", "Windows、Photoshop", "t3", PURPLE),
              Tile("🤖", "機械人同電子產品", "Arduino、汽車系統", "t4", GREEN),
              Tile("📈", "金融交易", "銀行同高速交易系統", "t5", AMBER),
              Tile("🏆", "編程比賽", "HKOI、IOI", "t6", RED),
          ])),
    Scene("why",
          "點解要學 C++ 呢？[[fast]]第一，佢好快。[[control]]第二，你可以控制得好細緻，連記憶體都可以自己管。"
          "[[base]]第三，學識 C++，再學 Java、C#、JavaScript 都會容易好多，因為好多寫法都好似。"
          "[[hard]]C++ 係出名難學嘅，不過唔使驚，我哋會一步一步嚟。",
          TileCard("點解學 C++？", [
              Tile("⚡", "快", "直接變成機器碼運行", "fast", AMBER),
              Tile("🔧", "控制力強", "連記憶體都可以自己管", "control", BLUE),
              Tile("🧱", "打好根基", "再學 Java、C#、JavaScript 都容易好多", "base", GREEN),
          ], height=380, footer=("出名難學？唔使驚，我哋一步一步嚟", "hard"))),
    Scene("compile_cpp",
          "C++ 同 Python 運行嘅方法唔同。[[src]]C++ 係編譯語言：寫好嘅原始碼，[[compiler]]先交俾編譯器，例如 g++，一次過翻譯晒，"
          "[[exe]]變成一個機器碼程式，[[run]]之後直接運行，所以好快。[[note]]就好似成本書預先翻譯好先出版。",
          compile_card(with_python=False)),
    Scene("compile_py",
          "[[src]]Python 就係直譯語言，[[interp]]由直譯器一邊讀、一邊翻譯、一邊做，[[run]]好方便，但係慢啲。[[note]]就好似即場傳譯咁。",
          compile_card(with_python=True)),
    Scene("demo_code",
          f"講咁多，不如實際比較吓。[[code]]呢個 C++ 程式會數吓{zh_int(LIMIT)}以下有幾多個質數。"
          "而家唔使睇得明，由 Hello World 嗰集開始，我哋會逐行講。",
          stage.scene(Open("primes.cpp", at="code", rate=7))),
    Scene("demo_cpp",
          f"首先用 g++ 將程式編譯好。[[run]]然後運行佢，前面加個 time，等電腦幫我哋計時。"
          f"[[result]]你睇，一眨眼就計完：{zh_int(count)}個質數，只係用咗{zh_seconds(t_cpp)}。",
          stage.scene(Run(compile_), Run(run_cpp, at="run"))),
    Scene("demo_py",
          "[[tab]]同一個計法，用 Python 寫。[[run]]一樣咁運行、一樣計時。Python 要一邊讀一邊做，所以要等一陣。",
          stage.scene(Open("primes.py", at="tab", rate=9), Run(run_py, at="run"))),
    Scene("compare",
          f"[[bars]]兩邊答案一樣，不過 C++ 用咗{zh_seconds(t_cpp)}，Python 就用咗{zh_seconds(t_py)}。"
          f"[[badge]]C++ 快咗大約{zh_int(about(ratio))}倍！[[why]]原因就係編譯：C++ 一早翻譯晒做機器碼，Python 就要一邊讀一邊做。",
          BarCard("同一個計法，邊個快啲？", [
              Bar("C++", t_cpp, f"{t_cpp:.3f} 秒", BLUE),
              Bar("Python", t_py, f"{t_py:.3f} 秒", TEAL),
          ], at="bars", badge=(f"C++ 快 {ratio:.0f} 倍", "badge"),
              note=("編譯：一早翻譯好　·　直譯：一邊讀一邊做", "why"))),
    Scene("course",
          "呢個課程由零開始：[[g1]]先學變數、迴圈同函數，[[g2]]再學指標同物件導向，[[g3]]然後係模板、STL、檔案、工具同並行，"
          "[[g4]]仲有比賽用嘅演算法。[[g5]]最後，我哋會用 C++ 寫一個喺終端機玩嘅貪食蛇遊戲。",
          RoadmapCard("成個課程學啲乜？", part_tiles, [
              ([0, 1, 2, 3, 4], BLUE, "g1"), ([5, 6], PURPLE, "g2"), ([7, 8, 9, 10, 11], TEAL, "g3"),
              ([12], AMBER, "g4"), ([13], GREEN, "g5"),
          ])),
    Scene("need",
          "想跟住一齊學，你只需要[[pc]]一部電腦、[[compiler]]一個編譯器，[[editor]]同埋一個寫程式嘅編輯器。"
          "[[free]]全部都係免費嘅，下一集我哋會一步一步裝好佢哋。",
          TileCard("要準備啲乜？", [
              Tile("💻", "一部電腦", "Windows、Mac、Linux 都得", "pc", BLUE),
              Tile("🧰", "編譯器", "g++：將 C++ 變成程式", "compiler", PURPLE),
              Tile("📝", "編輯器", "VS Code：寫程式用", "editor", TEAL),
          ], height=380, footer=("全部免費！下一集一齊安裝", "free"))),
    Scene("recap",
          "總結一下：[[r1]]程式就係一連串指令，用程式語言寫；[[r2]]C++ 又快、用途又廣；[[r3]]C++ 要先編譯，變成機器碼，先至運行。",
          BulletCard("今集重點", [("程式就係一連串指令，用程式語言寫", "r1"),
                                ("C++ 又快、用途又廣：遊戲、瀏覽器、比賽都用佢", "r2"),
                                ("C++ 要先編譯成機器碼，先至運行", "r3")])),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]揀一個你成日用嘅遊戲或者 app，上網查吓佢有冇用 C++ 寫。[[next]]下一集，我哋會安裝開發環境。多謝收睇，下次見！",
          EndCard("揀一個你成日用嘅遊戲或者 app，上網查吓佢有冇用 C++ 寫。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts)
