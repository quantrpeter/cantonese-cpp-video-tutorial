#!/usr/bin/env python3
"""Video 140 (syllabus 12.8): 位元運算

12 is 1100 and 10 is 1010 (bitset): & gives 8, | gives 14, ^ gives 6; 1 << 5 is 32, 12 >> 2 is 3.
`if (a & b == 8)` really draws "-Wparentheses: suggest parentheses around comparison in operand
of '&'" and never prints (== binds tighter); `(a & b) == 8` prints "and is 8". Masks 000..111
enumerate the subsets of {3, 5, 7} with their sums. Run `python3 video12.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 140
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-08"
FINAL = (CODE / "bits.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
MASKS = "    vector<int> items" + FINAL.split("    vector<int> items")[1].rsplit("}\n", 1)[0]
V2 = FINAL.replace(MASKS, "")
BAD = V2.replace("if ((a & b) == 8)", "if (a & b == 8)")
CC = "g++ -std=c++20 -Wall -Wextra bits.cpp -o bits"
OPS = "1100 1010\n8 14 6\n32 3\n"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"bits.cpp": BAD}, [
    CC, "./bits", "clear", Write("bits.cpp", V2), CC, "./bits", "clear", Write("bits.cpp", FINAL), CC, "./bits",
    Write("challenge.cpp", CHALLENGE), "g++ challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert "suggest parentheses around comparison in operand of '&'" in cpp.visible(c1.output) and r1.output == OPS
assert r2.output == OPS + "and is 8\n" and r3.output == OPS + "and is 8\n000:0 001:3 010:5 011:8 100:7 101:10 110:12 111:15 \n"
assert c2.code == c3.code == cch.code == 0 and rch.output == "2 3\n"

SAY = {"&": "and", "|": "or", "^": "xor", "~": "not", "<<": "左移", ">>": "右移", "bitset<4>": "bitset 四", "bitset": "bitset", "mask": "mask",
       "1 << i": "一左移 i", "mask & (1 << i)": "mask and 一左移 i", "-Wparentheses": "W parentheses", "__builtin_popcount": "builtin popcount",
       "XOR": "X O R", "AND": "AND", "OR": "OR"}

s = Stage({"bits.cpp": BAD}, title="位元運算", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！電腦入面所有數都係零同一。直接處理呢啲位元，可以好快咁做集合、開關、子集。今集學位元運算，同埋用 bitmask 列舉子集。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "& | ^ ~ << >> · bitmask")),
    Scene("goal",
          "今集會講：[[b1]]六個位元運算子；[[b2]]左移右移；[[b3]]一個常見嘅次序陷阱；[[b4]]用 bitmask 列舉子集。",
          BulletCard("今集學識", [("& | ^ ~", "b1"), ("<< >>", "b2"), ("優先次序陷阱", "b3"), ("bitmask 子集", "b4")])),
    Scene("ops",
          "[[ab]]a 係十二，即係一一零零；b 係十，一零一零。[[and]]and：兩個都係一先係一，得八；or：其中一個係一就係一，十四；xor：唔同先係一，六。[[shift]]一左移五係三十二，十二右移二係三。",
          TableCard("位元運算", ["運算", "二進制", "結果"], [
              (["a = 12", "1100", "12"], "ab"), (["b = 10", "1010", "10"], "ab"),
              (["a & b", "1000", "8"], "and"), (["a | b", "1110", "14"], "and"), (["a ^ b", "0110", "6"], "and"),
              (["1 << 5", "100000", "32"], "shift"), (["a >> 2", "11", "3"], "shift"),
          ], widths=[1, 1.2, 0.8], code_cols=(0, 1), size=34)),
    Scene("trap",
          "[[open]]程式印出呢啲數，再試吓：if a and b 等於八。[[cc]]編譯：[[warn]]g++ 警告：建議加括號。運行：[[o]]and is 8 冇印！因為等於等於嘅優先次序高過 and，變咗 a and 括號 b 等於八。",
          s.scene(Open("bits.cpp", mode="instant"), Mark(9, at="open"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("fix",
          "[[type]]加括號：括號 a and b，先至等於八。[[cc]]運行：[[o]]今次印 and is 8。位元運算一律加括號，最安全。",
          s.scene(Run(clr, at="type"), Replace("bits.cpp", "if (a & b == 8)", "if ((a & b) == 8)", at="type", rate=20), Expect("bits.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("masks",
          "[[type]]子集：三樣嘢，每樣揀或者唔揀，可以用三個位表示，mask 由零到七。[[test]]mask and 一左移 i，就係問第 i 樣有冇揀。[[cc]]運行：[[o]]八個子集，連埋總和：零零零係乜都唔揀，一一一係全部揀，總和十五。",
          s.scene(Run(clr2, at="type"), Type("bits.cpp", MASKS, before="}", last=True, at="type", rate=60), Expect("bits.cpp", FINAL),
                  Mark(13, at="type"), Mark(16, at="test"), Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("recap",
          "總結：[[r1]]and、or、xor 逐個位計；[[r2]]一左移 i 就係第 i 個位；[[r3]]位元運算記得加括號；[[r4]]mask 由零到二嘅 n 次方減一，就列舉晒所有子集，n 要細。",
          BulletCard("今集重點", [("& | ^：逐位", "r1"), ("1 << i：第 i 位", "r2"), ("一律加括號", "r3"), ("mask 0 … 2ⁿ−1：所有子集", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]三、五、七、九入面，有幾多個子集加埋等於十二？再用 builtin popcount 數十三有幾多個一。[[next]]下一集：圖嘅表示。多謝收睇，下次見！",
          EndCard("用 mask 列舉 {3, 5, 7, 9} 嘅子集，數總和 = 12 嘅（答案 2）；再印 __builtin_popcount(13)（答案 3）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
