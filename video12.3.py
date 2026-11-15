#!/usr/bin/env python3
"""Video 135 (syllabus 12.3): 前綴和

pre[i] = pre[i-1] + a[i] turns every range sum into one subtraction: pre[r] - pre[l-1]. With
in.txt (array 3 1 4 1 5 and queries 1-3, 2-5, 4-4) the real run prints 8, 11, 1. Building pre is
O(n), each query O(1). 2D prefix sums use inclusion–exclusion (the challenge prints 28).
Run `python3 video135.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 135
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-03"
FINAL = (CODE / "prefix.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()

(cat, c1, r1, cch, rch) = cpp.session({"prefix.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 prefix.cpp -o pre", "./pre < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert cat.output == IN and r1.output == "8\n11\n1\n" and c1.code == cch.code == 0 and rch.output == "28\n"

SAY = {"pre[r] - pre[l-1]": "pre r 減 pre l 減一", "pre[i]": "pre i", "pre": "pre", "O(n)": "O n", "O(1)": "O 一", "O(nq)": "O n q",
       "in.txt": "in 點 t x t", "cat": "cat", "l": "l", "r": "r", "2D": "二維"}

s = Stage({"prefix.cpp": FINAL}, title="前綴和", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！題目俾你一個陣列，再問你好多次：第 l 個到第 r 個加埋係幾多？每次都由頭加，問十萬次就太慢。今集學前綴和：預先準備一次，之後每個問題一步答。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "pre[r] - pre[l-1] · O(1) 查詢")),
    Scene("goal",
          "今集會講：[[b1]]前綴和係乜；[[b2]]點樣一步答區間和；[[b3]]寫成程式；[[b4]]二維前綴和。",
          BulletCard("今集學識", [("pre[i]：頭 i 個嘅和", "b1"), ("pre[r] − pre[l−1]", "b2"), ("程式", "b3"), ("二維", "b4")])),
    Scene("idea",
          "[[a]]陣列係三、一、四、一、五。[[pre]]pre i 係頭 i 個加埋：零、三、四、八、九、十四。[[q]]問第二到第五個：pre 五減 pre 一，十四減三，等於十一。",
          BoxesCard("前綴和", [
              BoxRow([Box("a", "3", "1", at="a", w=120), Box("", "1", "2", at="a", w=120), Box("", "4", "3", at="a", w=120),
                      Box("", "1", "4", at="a", w=120), Box("", "5", "5", at="a", w=120)], gap=10, label="a"),
              BoxRow([Box("", "0", "0", at="pre", color=BLUE, w=110), Box("", "3", "1", at="q", color=AMBER, w=110), Box("", "4", "2", at="pre", color=BLUE, w=110),
                      Box("", "8", "3", at="pre", color=BLUE, w=110), Box("", "9", "4", at="pre", color=BLUE, w=110),
                      Box("", "14", "5", at="q", color=AMBER, w=110)], gap=10, label="pre"),
          ], notes=[("第 2 到 5 個：pre[5] − pre[1] = 14 − 3 = 11", "q")], top=CONTENT_TOP + 10, row_h=230, box_h=100, size=40)),
    Scene("code",
          "[[read]]讀入 n 同問題數 q。[[build]]pre 開 n 加一格，pre 零係零；每讀一個數，pre i 等於 pre i 減一加 x。[[query]]每個問題 l、r，答案就係 pre r 減 pre l 減一。",
          s.scene(Open("prefix.cpp", at="read"), Mark((7, 8), at="read"), Mark((9, 14), at="build"), Mark((15, 19), at="query"))),
    Scene("run",
          "[[cat]]輸入檔：五個數，三個問題。[[cc]]編譯運行：[[o]]一到三係八，二到五係十一，四到四係一。",
          s.scene(Mark(None), Run(cat, at="cat"), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("cost",
          "[[naive]]直接加：每個問題最多 n 步，q 個問題就係 O n q；[[prefix]]前綴和：準備 O n，之後每個問題 O 一。n 同 q 都係十萬，差一萬倍。",
          TableCard("n、q = 10⁵", ["方法", "時間", "步數"], [
              (["每次由頭加", "O(nq)", "10¹⁰：太慢"], "naive", RED),
              (["前綴和", "O(n + q)", "2 × 10⁵：即刻"], "prefix", GREEN),
          ], widths=[1.2, 1, 1.4], code_cols=(1,), size=40)),
    Scene("twod",
          "[[two]]二維都一樣：p r c 係左上角到 r c 嘅長方形總和。[[q]]問一個長方形，就用大嘅減上面、減左面，再加返重複減咗嘅左上角。",
          TableCard("二維前綴和", ["步驟", "公式"], [
              (["建立", "p[r][c] = g[r][c] + p[r-1][c] + p[r][c-1] - p[r-1][c-1]"], "two"),
              (["查詢", "p[r2][c2] - p[r1-1][c2] - p[r2][c1-1] + p[r1-1][c1-1]"], "q", GREEN),
          ], widths=[0.6, 2.6], code_cols=(1,), size=30)),
    Scene("recap",
          "總結：[[r1]]pre i 係頭 i 個嘅和，pre 零係零；[[r2]]區間和等於 pre r 減 pre l 減一；[[r3]]準備 O n，每次查詢 O 一；[[r4]]二維就用加減重疊部分。",
          BulletCard("今集重點", [("pre[0] = 0、pre[i] = pre[i-1] + a[i]", "r1"), ("sum(l..r) = pre[r] − pre[l−1]", "r2"), ("O(n) 準備、O(1) 查詢", "r3"),
                                ("二維：容斥", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]一個三乘三嘅格，填一到九，用二維前綴和計第二至三行、第二至三列嘅長方形總和。[[next]]下一集：雙指針同滑動視窗。多謝收睇，下次見！",
          EndCard("3 × 3 格填 1 到 9，用二維前綴和計 (2,2) 到 (3,3) 嘅總和：答案 28。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
