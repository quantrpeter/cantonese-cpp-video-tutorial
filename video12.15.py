#!/usr/bin/env python3
"""Video 147 (syllabus 12.15): 經典 DP

Three classic dynamic programmes in one file: 0/1 knapsack (weights 1 3 4 5, values 1 4 5 7,
capacity 7) with a one-row table filled from high capacity down; longest increasing subsequence
of 10 9 2 5 3 7 101 18 in O(n²); longest common subsequence of ABCBDAB and BDCABA with a 2D
table. The real run prints knapsack 9, lis 4, lcs 4. The challenge is minimum coins (1, 3, 4 → 6
needs 2). Run `python3 video147.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 147
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-15"
FINAL = (CODE / "classic.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text):
    return next(i + 1 for i, l in enumerate(LINES) if text in l)


(c1, r1, cch, rch) = cpp.session({"classic.cpp": FINAL}, [
    "g++ -std=c++20 -O2 -Wall -Wextra classic.cpp -o dp", "./dp", Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "knapsack 9\nlis 4\nlcs 4\n" and c1.code == cch.code == 0 and rch.output == "2\n"

SAY = {"knapsack": "knapsack", "0/1 knapsack": "零一背包", "LIS": "L I S", "lis": "L I S", "LCS": "L C S", "lcs": "L C S", "dp": "D P",
       "cap": "cap", "ABCBDAB": "A B C B D A B", "BDCABA": "B D C A B A", "O(nW)": "O n W", "O(n²)": "O n 二次方", "O(nm)": "O n m"}

s = Stage({"classic.cpp": FINAL}, title="經典 DP", code_px=19)

scenes = [
    Scene("intro",
          "歡迎返嚟！比賽成日出現幾條經典動態規劃：背包、最長上升子序列、最長公共子序列。今集逐個睇佢哋嘅狀態同轉移。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "背包 · LIS · LCS")),
    Scene("goal",
          "今集會講：[[b1]]零一背包；[[b2]]最長上升子序列；[[b3]]最長公共子序列；[[b4]]點樣諗狀態。",
          BulletCard("今集學識", [("0/1 背包", "b1"), ("LIS", "b2"), ("LCS", "b3"), ("狀態同轉移", "b4")])),
    Scene("knap",
          "[[state]]背包：dp c 係容量唔超過 c 時最大嘅價值。[[item]]逐件物品考慮，[[trans]]放唔放：唔放就係 dp c，放就係 dp c 減重量，加價值，揀大嗰個。[[down]]c 要由大到細行，"
          "咁每件物品先只會用一次。",
          s.scene(Open("classic.cpp", mode="instant"), Mark(ln("vector<int> dp(cap + 1, 0);"), at="state"), Mark(ln("for (size_t i = 0; i < w.size(); i++)"), at="item"),
                  Mark(ln("dp[c] = max(dp[c], dp[c - w[i]] + v[i]);"), at="trans"), Mark(ln("for (int c = cap; c >= w[i]; c--)"), at="down"))),
    Scene("lis",
          "[[state]]最長上升子序列：dp i 係以第 i 個結尾、最長嘅上升子序列長度，起碼係一。[[trans]]睇前面每個 j，如果 a j 細過 a i，就可以接上去：dp j 加一。[[ans]]答案係所有 dp 入面最大嗰個。",
          s.scene(Mark(ln("vector<int> dp(a.size(), 1);"), at="state"), Mark((ln("if (a[j] < a[i])"), ln("dp[i] = max(dp[i], dp[j] + 1);")), at="trans"),
                  Mark(ln("return *max_element"), at="ans"))),
    Scene("lcs",
          "[[state]]最長公共子序列：dp i j 係 s 頭 i 個字同 t 頭 j 個字嘅答案。[[same]]最後一個字一樣，就係左上角加一；[[diff]]唔一樣，就揀上面或者左面大嗰個。",
          s.scene(Mark(ln("vector<vector<int>> dp(n + 1"), at="state"), Mark((ln("if (s[i - 1] == t[j - 1])"), ln("dp[i][j] = dp[i - 1][j - 1] + 1;")), at="same"),
                  Mark(ln("dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);"), at="diff"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]背包最多九，揀重三同重四嘅；上升子序列長度四，例如二、三、七、一百零一；公共子序列長度四，例如 B C B A。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("summary",
          "三條題目嘅狀態同複雜度：[[k]]背包，O n 乘容量；[[l]]LIS，O n 二次方；[[c]]LCS，O n 乘 m。",
          TableCard("三個經典 DP", ["題目", "狀態", "時間"], [
              (["0/1 背包", "dp[c]：容量 c 最大價值", "O(nW)"], "k"),
              (["LIS", "dp[i]：以 i 結尾最長", "O(n²)"], "l"),
              (["LCS", "dp[i][j]：兩個前綴", "O(nm)"], "c"),
          ], widths=[0.9, 2, 0.8], code_cols=(), size=36)),
    Scene("recap",
          "總結：[[r1]]背包：揀定唔揀，容量由大到細；[[r2]]LIS：接喺細過自己嘅後面；[[r3]]LCS：一樣就斜上加一，唔一樣就揀大；[[r4]]DP 嘅關鍵係定義好狀態。",
          BulletCard("今集重點", [("背包：c 由大到細", "r1"), ("LIS：dp[j] + 1", "r2"), ("LCS：二維表", "r3"), ("先定義狀態", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]有面值一、三、四嘅硬幣，湊六蚊最少要幾個？dp a 係湊 a 蚊最少幾多個。[[next]]下一集：數論基礎。多謝收睇，下次見！",
          EndCard("硬幣 {1, 3, 4}，dp[a] = min(dp[a − c] + 1)：湊 6 最少 2 個（3 + 3）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
