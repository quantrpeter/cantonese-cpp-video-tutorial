#!/usr/bin/env python3
"""Video 133 (syllabus 12.1): 競賽寫法

A contest template: #include <bits/stdc++.h> (GCC only), using namespace std (fine in a one-file
contest program), and fast I/O. Summing 2,000,000 numbers from big.txt (made with a python3
one-liner) built with -O2: `time ./slow < big.txt` really takes about six times longer than
`time ./fast < big.txt` with ios::sync_with_stdio(false) and cin.tie(nullptr). Both print
1999999000000. The challenge reads a test-case count first. Run `python3 video12.1.py --help`.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 133
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-01"
FAST = (CODE / "fast.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CH_IN = (CODE / "challenge.txt").read_text()
SYNC = "    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n"
SLOW = FAST.replace(SYNC, "")
GEN = "python3 -c 'print(2000000); print(*range(2000000))' > big.txt"

(gen, cs, cf, ts, tf, cch, rch) = cpp.session({"slow.cpp": SLOW, "fast.cpp": FAST, "challenge.txt": CH_IN}, [
    GEN, "g++ -O2 slow.cpp -o slow", "g++ -O2 fast.cpp -o fast", "time ./slow < big.txt", "time ./fast < big.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch < challenge.txt",
], refresh=opts.fresh_runs, cols=58)


def secs(r):
    return float(re.search(r"real\s+0m([\d.]+)s", r.output).group(1))


slow, fast = secs(ts), secs(tf)
assert ts.output.startswith("1999999000000\n") and tf.output.startswith("1999999000000\n") and slow > 3 * fast, (slow, fast)
assert rch.output == "3\n30\n0\n"
ratio = round(slow / fast)
D = "零一二三四五六七八九"
say_ratio = D[ratio] if ratio < 10 else ("十" + (D[ratio % 10] if ratio % 10 else "") if ratio < 20 else str(ratio))

say_slow = "零點" + "".join(D[int(c)] for c in f"{slow:.2f}".split(".")[1])

SAY = {"bits/stdc++.h": "bits std c 加加 點 h", "#include <bits/stdc++.h>": "include bits std c 加加", "using namespace std": "using namespace std",
       "ios::sync_with_stdio(false)": "sync with stdio false", "sync_with_stdio": "sync with stdio", "cin.tie(nullptr)": "cin tie null pointer",
       "HKOI": "H K O I", "big.txt": "big 點 t x t", "python3": "python 三", "time": "time", "-O2": "O 二", "endl": "end l", "'\\n'": "反斜線 n"}

s = Stage({"slow.cpp": SLOW, "fast.cpp": SLOW}, title="競賽寫法", code_px=26)

scenes = [
    Scene("intro",
          "歡迎返嚟！第十二部分講演算法同競賽，例如香港嘅 HKOI。比賽寫程式有啲唔同：只得一個檔案，要快，仲要讀好多輸入。今集整一個比賽用嘅樣板。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "bits/stdc++.h · 快速輸入輸出")),
    Scene("goal",
          "今集會講：[[b1]]bits stdc 加加；[[b2]]比賽入面嘅 using namespace std；[[b3]]兩句快速輸入輸出；[[b4]]常見輸入格式。",
          BulletCard("今集學識", [("#include <bits/stdc++.h>", "b1"), ("using namespace std;", "b2"), ("sync_with_stdio(false)、cin.tie(nullptr)", "b3"),
                                ("輸入格式：先讀 n", "b4")])),
    Scene("template",
          "[[bits]]bits stdc 加加一次過 include 晒標準庫，只有 GCC 有，比賽用嚟慳時間，正式項目唔好用。[[ns]]using namespace std 喺比賽嘅單一檔案都 OK，但係 header 入面千祈唔好，3.11 講過。"
          "[[read]]程式先讀 n，再讀 n 個數加埋。",
          s.scene(Open("slow.cpp", at="bits"), Mark(1, at="bits"), Mark(2, at="ns"), Mark((5, 13), at="read"))),
    Scene("gen",
          f"[[gen]]用 python 一句過整一個測試檔：二百萬個數。[[cc]]用 O 二編譯 slow。[[t]]time slow，細過號表示輸入由 big.txt 嚟：[[o]]用咗 {say_slow} 秒。",
          s.scene(Mark(None), Run(gen, at="gen"), Run(cs, at="cc"), Run(ts, at="t"))),
    Scene("fast",
          f"[[type]]fast.cpp 一樣，但係加兩句：sync with stdio false，cin tie null pointer。[[cc]]編譯 fast，再 time：[[o]]答案一樣，但係快咗大約 {say_ratio} 倍。",
          s.scene(Open("fast.cpp", at="type"), Type("fast.cpp", SYNC, after="int main() {\n", at="type", rate=40), Expect("fast.cpp", FAST), Mark((4, 5), at="type"),
                  Mark(None, at="cc"), Run(cf, at="cc"), Run(tf, at="o"))),
    Scene("why",
          "[[sync]]第一句：cin 同 C 嘅 scanf 唔再保持同步，可以自己用大 buffer；所以之後唔好再撈埋 scanf、printf。[[tie]]第二句：每次讀之前唔使先清 cout 嘅 buffer。"
          "[[endl]]印嘢用反斜線 n，唔好用 endl，endl 每次都會清 buffer，好慢。",
          BulletCard("點解快咗", [("sync_with_stdio(false)：唔再同 C stdio 同步", "sync"), ("cin.tie(nullptr)：讀之前唔清 cout", "tie"), ("用 '\\n'，唔好用 endl", "endl")])),
    Scene("formats",
          "常見輸入格式：[[n]]先俾數量 n，再俾 n 個數；[[t]]先俾 t 組測試，每組自己讀；[[eof]]或者冇講幾多，就讀到檔尾為止，用 while cin 大過號。",
          TableCard("常見輸入格式", ["格式", "寫法"], [
              (["先 n，再 n 個", "cin >> n; for (…) cin >> x;"], "n"),
              (["先 t 組測試", "cin >> t; while (t--) { … }"], "t"),
              (["讀到尾", "while (cin >> x) { … }"], "eof"),
          ], widths=[1.1, 2], code_cols=(1,), size=38)),
    Scene("recap",
          "總結：[[r1]]比賽可以用 bits stdc 加加同 using namespace std；[[r2]]加兩句快速輸入輸出；[[r3]]用反斜線 n，唔用 endl；[[r4]]睇清楚輸入格式。",
          BulletCard("今集重點", [("bits/stdc++.h（只限比賽）", "r1"), ("兩句快速 I/O", "r2"), ("'\\n' 唔用 endl", "r3"), ("輸入格式", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個程式，先讀 t 組測試，每組兩個數，印出佢哋嘅和。[[next]]下一集：時間複雜度。多謝收睇，下次見！",
          EndCard("輸入：第一行 t，之後 t 行每行 a b；每組印 a + b。用今集嘅樣板。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
