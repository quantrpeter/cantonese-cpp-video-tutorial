#!/usr/bin/env python3
"""Video 148 (syllabus 12.16): 數論基礎

Euclid's gcd (84, 36 → 12, same as std::gcd; std::lcm(4, 6) = 12), the sieve of Eratosthenes up to
50, and modular arithmetic with MOD = 1e9+7 including fast power (2^100 mod MOD = 976371285).
With `int x = 100000, y = 100000` the product overflows before the % and the real run prints
410065401; with long long it prints the correct 999999937. Run `python3 video148.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 148
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-16"
FINAL = (CODE / "numbers.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BAD = FINAL.replace("    long long x = 100000, y = 100000;\n", "    int x = 100000, y = 100000;\n")
LINES = FINAL.split("\n")


def ln(text):
    return next(i + 1 for i, l in enumerate(LINES) if text in l)


CC = "g++ -std=c++20 -O2 -Wall numbers.cpp -o num"
HEAD = "12 12 12\n2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 \n"

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"numbers.cpp": BAD}, [
    CC, "./num", "clear", Write("numbers.cpp", FINAL), CC, "./num", Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == HEAD + "410065401 976371285\n" and r2.output == HEAD + "999999937 976371285\n", (r1.output, r2.output)
assert c1.code == c2.code == cch.code == 0 and rch.output == "437918130\n"

SAY = {"gcd": "G C D", "lcm": "L C M", "myGcd": "my G C D", "std::gcd": "S T D G C D", "MOD": "MOD", "1'000'000'007": "十億零七",
       "1e9+7": "十億零七", "power": "power", "sieve": "篩法", "Eratosthenes": "埃拉托色尼", "long long": "long long", "%": "取餘",
       "O(log n)": "O log n", "O(n log log n)": "O n log log n"}

s = Stage({"numbers.cpp": BAD}, title="數論基礎", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！第十二部分最後一集：數論基礎。最大公因數、搵質數、同埋比賽成日要求答案取餘十億零七，都係必學嘅工具。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "gcd · 篩法 · 取餘")),
    Scene("goal",
          "今集會講：[[b1]]輾轉相除法；[[b2]]埃拉托色尼篩法；[[b3]]取餘同快速冪；[[b4]]溢位陷阱。",
          BulletCard("今集學識", [("gcd：輾轉相除", "b1"), ("篩法搵質數", "b2"), ("% MOD、快速冪", "b3"), ("溢位：用 long long", "b4")])),
    Scene("gcd",
          "[[loop]]輾轉相除：a 除 b 嘅餘數做新嘅 b，舊嘅 b 做新嘅 a，直到 b 係零，a 就係最大公因數。八十四同三十六，答案十二。[[std]]C++17 已經有 std::gcd 同 std::lcm。",
          s.scene(Open("numbers.cpp", mode="instant"), Mark((ln("long long myGcd"), ln("return a;") + 1), at="loop"), Mark(ln("cout << myGcd(84, 36)"), at="std"))),
    Scene("sieve",
          "[[init]]篩法：先當所有數都係質數。[[loop]]由二開始，見到質數，就將佢嘅倍數全部劃走，由 i 二次方開始就得。[[fast]]剩低嘅就係質數，時間大約係 n log log n，好快。",
          s.scene(Mark((ln("vector<bool> prime(n + 1, true);"), ln("prime[0] = prime[1] = false;")), at="init"),
                  Mark((ln("for (int i = 2; i * i <= n; i++)"), ln("prime[j] = false;")), at="loop"))),
    Scene("mod",
          "[[why]]答案太大，題目就叫你取餘十億零七。[[pow]]快速冪：指數係單數，就乘落答案；底數自己平方，指數除二。二嘅一百次方，只要七次左右。[[rule]]每次乘完都即刻取餘。",
          s.scene(Mark(ln("const long long MOD"), at="why"), Mark((ln("long long power"), ln("return result;") + 1), at="pow"),
                  Mark(ln("result = result * base % MOD;"), at="rule"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]十二、十二、十二；五十以下嘅質數；二嘅一百次方取餘，啱。但係十萬乘十萬取餘，印咗四億一千萬幾？答案應該係九億九千九百九十九萬九千九百三十七。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("overflow",
          "[[int]]因為 x 同 y 係 int，十萬乘十萬係一百億，超過 int 嘅上限，喺取餘之前已經溢位。[[fix]]改做 long long，先乘先取餘就啱。[[cc]]運行：[[o]]九億九千幾，正確。",
          s.scene(Mark(ln("long long x = 100000"), at="int"), Run(clr, at="fix"), Replace("numbers.cpp", "    int x = 100000", "    long long x = 100000", at="fix", rate=20),
                  Expect("numbers.cpp", FINAL), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("rules",
          "數論貼士：[[ll]]涉及乘法同取餘，一律用 long long；[[each]]每一步都取餘，唔好等到最後；[[mod]]十億零七係質數，之後學除法取餘會用到。",
          BulletCard("貼士", [("乘法 + 取餘：long long", "ll"), ("每步都 % MOD", "each"), ("1e9+7 係質數", "mod")])),
    Scene("recap",
          "總結：[[r1]]輾轉相除求 gcd，或者用 std::gcd；[[r2]]篩法一次過搵晒質數；[[r3]]快速冪 O log n；[[r4]]取餘之前小心溢位。第十二部分完成！",
          BulletCard("今集重點", [("gcd：輾轉相除", "r1"), ("篩法", "r2"), ("快速冪：O(log n)", "r3"), ("小心溢位", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]計一百嘅階乘，取餘十億零七。[[next]]下一集開始最後一部分：綜合項目，第一個係貪食蛇。多謝收睇，下次見！",
          EndCard("用 long long，每乘一次就 % 1'000'000'007，計 100!（答案 437918130）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
