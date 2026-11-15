#!/usr/bin/env python3
"""Video 134 (syllabus 12.2): 時間複雜度

Checking a permutation for duplicates two ways, built with -O2: a double loop (O(n²)) and sort +
neighbours (O(n log n)). Real runs for n = 20000, 40000, 80000: the double loop's time roughly
quadruples each time n doubles, the sorted version stays at a few milliseconds. Then the rule of
thumb (about 10⁸ simple steps a second) applied to constraints. Spoken numbers are measured.
Run `python3 video134.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 134
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-02"
FINAL = (CODE / "dup.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text):
    return next(i + 1 for i, l in enumerate(LINES) if text in l)


(c1, a, b, c, cch, rch) = cpp.session({"dup.cpp": FINAL}, [
    "g++ -std=c++20 -O2 dup.cpp -o dup", "echo 20000 | ./dup", "echo 40000 | ./dup", "echo 80000 | ./dup",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)


def t(r, which):
    return int(re.search(re.escape(which) + r"\s+0 (\d+)ms", r.output).group(1))


sq = [t(r, "O(n^2)") for r in (a, b, c)]
lg = [t(r, "O(n log n)") for r in (a, b, c)]
assert sq[1] > 2.5 * sq[0] and sq[2] > 2.2 * sq[1] and max(lg) < 50, (sq, lg)
assert rch.output == "10000000000 too slow\n1700000 ok\n"
D = "零一二三四五六七八九"


def zh(n):
    if n == 0:
        return "零"
    out, gap = "", False
    for unit, name in ((1000, "千"), (100, "百"), (10, "十"), (1, "")):
        d = n // unit % 10
        if d:
            if gap and out:
                out += "零"
            out += ("" if (unit == 10 and d == 1 and not out) else D[d]) + name
            gap = False
        elif out:
            gap = True
    return out


SAY = {"O(n^2)": "O n 二次方", "O(n²)": "O n 二次方", "O(n log n)": "O n log n", "O(n)": "O n", "O(log n)": "O log n", "O(1)": "O 一",
       "Big-O": "Big O", "10⁸": "十的八次方", "slowHasDup": "slow has dup", "fastHasDup": "fast has dup", "sort": "sort", "-O2": "O 二",
       "ms": "毫秒", "echo": "echo"}

s = Stage({"dup.cpp": FINAL}, title="時間複雜度", code_px=20, split=0.5)

scenes = [
    Scene("intro",
          "歡迎返嚟！比賽嘅題目通常有時間限制，例如一秒。點樣喺寫之前就知道自己嘅方法夠唔夠快？今集講時間複雜度，大 O 記法，同埋睇題目限制嘅方法。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "Big-O · 10⁸ 步一秒 · 睇限制")),
    Scene("goal",
          "今集會講：[[b1]]大 O 係乜；[[b2]]實測 O n 二次方 同 O n log n；[[b3]]一秒大約做一億步；[[b4]]由 n 嘅上限揀演算法。",
          BulletCard("今集學識", [("Big-O", "b1"), ("實測：O(n²) vs O(n log n)", "b2"), ("≈ 10⁸ 步一秒", "b3"), ("由限制揀方法", "b4")])),
    Scene("code",
          "問題：一堆數入面有冇重複？[[slow]]第一個方法：每一對都比一次，兩層迴圈，大約 n 二次方 除二步，叫 O n 二次方。[[fast]]第二個方法：先 sort，重複嘅一定排埋一齊，再睇隔籬就得，"
          "O n log n。[[data]]測試資料係零到 n 減一打亂，冇重複，兩個都要行晒。",
          s.scene(Open("dup.cpp", at="slow"), Mark((ln("bool slowHasDup"), ln("bool slowHasDup") + 9), at="slow"),
                  Mark((ln("bool fastHasDup"), ln("bool fastHasDup") + 8), at="fast"), Mark((ln("vector<int> v(n);"), ln("v[i] = 1LL")), at="data"))),
    Scene("run",
          f"[[cc]]用 O 二編譯，n 等於二萬：[[a]]兩層迴圈 {zh(sq[0])} 毫秒。[[b]]n 加倍到四萬：{zh(sq[1])} 毫秒，差唔多四倍！[[c]]再加倍到八萬：{zh(sq[2])} 毫秒。"
          "sort 嘅方法，三次都只係幾毫秒。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(a, at="a"), Run(b, at="b"), Run(c, at="c"))),
    Scene("growth",
          "[[sq]]n 加倍，n 二次方就變四倍；[[lg]]n log n 只係大約加倍多少少。[[big]]n 去到一百萬，兩層迴圈要五千億步，幾分鐘都未完；sort 嘅方法唔使一秒。",
          TableCard("n 加倍會點", ["複雜度", "n → 2n", "n = 10⁶ 大約"], [
              (["O(n²)", "× 4", "10¹² 步：太慢"], "sq", RED),
              (["O(n log n)", "× 2 多少少", "2 × 10⁷ 步：好快"], "lg", GREEN),
          ], widths=[1.2, 1, 1.6], code_cols=(0,), size=40, note=("n 越大，差距越大", "big"))),
    Scene("rule",
          "比賽嘅經驗法則：[[rate]]一秒大約做到一億步簡單運算。[[how]]睇 n 嘅上限，代入複雜度：[[t1]]n 十萬，n 二次方 係一百億，太慢；n log n 大約二百萬，冇問題。",
          TableCard("n 嘅上限 → 可以用嘅複雜度（一秒）", ["n 最大", "可以用"], [
              (["≤ 20", "O(2ⁿ)、O(n!)：暴力"], "rate"),
              (["≤ 5000", "O(n²)"], "how"),
              (["≤ 10⁶", "O(n log n)、O(n)"], "t1", GREEN),
              (["≤ 10¹⁸", "O(log n)、O(1)"], "t1"),
          ], widths=[1, 2], code_cols=(), size=38)),
    Scene("recap",
          "總結：[[r1]]大 O 講步數點樣跟住 n 增長；[[r2]]n 加倍，n 二次方 變四倍；[[r3]]一秒大約一億步；[[r4]]寫之前先睇 n 嘅上限，揀啱複雜度。",
          BulletCard("今集重點", [("Big-O：增長速度", "r1"), ("O(n²)：n 加倍 → ×4", "r2"), ("≈ 10⁸ 步 / 秒", "r3"), ("先睇限制", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫幾行計數：n 等於十萬，n 二次方 同 n log n 各係幾多步，超過一億就印 too slow。[[next]]下一集：前綴和。多謝收睇，下次見！",
          EndCard("n = 100000：計 n × n 同 n × 17（≈ n log n），超過 10⁸ 就印 too slow。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
