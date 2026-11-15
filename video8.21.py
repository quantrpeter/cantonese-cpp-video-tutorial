#!/usr/bin/env python3
"""Video 108 (syllabus 8.21): 小項目：單字頻率統計

Part 8 together: read text.txt with `./top < text.txt`, clean each word (letters only, lower
case), count with std::map, copy into a vector of pairs, sort with a lambda (count high to low,
then alphabetical) and print the top 10. The real run: 11 the, 5 dog, 4 cat, 3 and, 3 on, ...
Run `python3 video8.21.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 108
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-21"
FINAL = (CODE / "top.cpp").read_text()
TEXT = (CODE / "text.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
HEAD = FINAL.split("std::string clean")[0]
CLEAN = "std::string clean" + FINAL.split("std::string clean")[1].split("int main")[0]
MAIN = "int main" + FINAL.split("int main")[1]
SORT = "    std::vector<Entry> list" + MAIN.split("    std::vector<Entry> list")[1].rsplit("}\n", 1)[0]
SIZE = "    std::cout << count.size() << \" words\\n\";\n"
MAIN_A = MAIN.replace(SORT, SIZE)
S0 = HEAD + "int main() {\n}\n"
VA = HEAD + CLEAN + MAIN_A
CC = "g++ -std=c++20 -Wall -Wextra top.cpp -o top"

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"top.cpp": VA, "text.txt": TEXT}, [
    CC, "./top < text.txt", "clear", Write("top.cpp", FINAL), CC, "./top < text.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch < text.txt",
], refresh=opts.fresh_runs, cols=48)
nwords = int(r1.output.split()[0])
assert r1.output == f"{nwords} words\n" and 15 < nwords < 40, r1.output
top = r2.output.splitlines()
assert top[:5] == ["11 the", "5 dog", "4 cat", "3 and", "3 on"] and len(top) == 10, r2.output
assert c1.code == c2.code == cch.code == 0 and rch.output == "11 the\n5 dog\n4 cat\n"
D = "零一二三四五六七八九"
say_n = (D[nwords // 10] if nwords >= 20 else "") + "十" + (D[nwords % 10] if nwords % 10 else "")

SAY = {"std::map": "S T D map", "std::sort": "S T D sort", "Entry": "Entry", "clean": "clean", "std::isalpha": "is alpha",
       "isalpha": "is alpha", "std::tolower": "to lower", "tolower": "to lower", "text.txt": "text 點 t x t", "< text.txt": "細過號 text 點 t x t",
       "count[w]++": "count w 加加", "the": "the", "dog": "dog", "cat": "cat", "and": "and", "on": "on", "lambda": "lambda"}

s = Stage({"text.txt": TEXT, "top.cpp": S0}, title="小項目：單字頻率統計", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第八部分最後一集，做一個單字頻率統計：讀入一篇文章，搵出最常出現嘅十個字。會用到 map、vector、sort、lambda 同字串處理。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "map · sort · lambda · 頭十名")),
    Scene("plan",
          "計劃：[[b1]]清理每個字：只留字母，變細楷；[[b2]]用 map 數次數；[[b3]]搬入 vector，按次數排序；[[b4]]印頭十名。",
          BulletCard("計劃", [("clean：字母、細楷", "b1"), ("map 數次數", "b2"), ("vector + sort", "b3"), ("印頭十名", "b4")])),
    Scene("text",
          "[[open]]text.txt 係一篇短文，有大楷、有標點：The 同 the，dog 同 dog 加句號，應該當係同一個字。",
          s.scene(Open("text.txt", at="open"), Mark((1, 4), at="open"))),
    Scene("clean",
          "[[type]]clean 逐個字元睇：[[alpha]]isalpha 係字母先要，[[lower]]tolower 變細楷。咁 The 同 the 就一樣，句號同引號都冇咗。",
          s.scene(Mark(None), Open("top.cpp", at="type"), Type("top.cpp", CLEAN, before="int main", at="type", rate=60),
                  Mark(14, at="alpha"), Mark(15, at="lower"))),
    Scene("count",
          "[[type]]main 逐個字讀入，清理之後，唔係空嘅就加入 map。[[cc]]先印 map 有幾多個唔同嘅字。運行嗰陣用細過號 text.txt，將檔案當做輸入。"
          f"[[o]]一共 {say_n} 個唔同嘅字。",
          s.scene(Mark(None), Replace("top.cpp", "int main() {\n}", MAIN_A.rstrip("\n"), at="type", rate=60), Expect("top.cpp", VA),
                  Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("sort",
          "map 係按字母排，唔係按次數。[[type]]將 map 成個搬入一個 vector；[[cmp]]再用 8.12 嘅 lambda 排：次數多嘅排前，一樣就按字母。[[top]]最後印頭十個；如果唔夠十個字，就印晒，所以條件要同時檢查 size。",
          s.scene(Run(clr, at="type"), Replace("top.cpp", SIZE, SORT, at="type", rate=120), Expect("top.cpp", FINAL), Mark(30, at="type"),
                  Mark((31, 37), at="cmp"), Mark((38, 41), at="top"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]the 出現十一次，第一；跟住 dog 五次，cat 四次；and 同 on 都係三次，按字母 and 排先。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("parts",
          "呢個小項目用咗：[[a]]4.8 嘅字元處理；[[b]]8.5 嘅 map；[[c]]8.4 嘅 pair 同 structured bindings；[[d]]8.11 同 8.12 嘅 lambda 同 sort。",
          TableCard("用咗乜？", ["概念", "喺邊度"], [
              (["isalpha、tolower（4.8）", "clean()"], "a"),
              (["std::map（8.5）", "count[w]++"], "b"),
              (["pair、bindings（8.4）", "Entry、[word, n]"], "c"),
              (["lambda + sort（8.11、8.12）", "排次數、再排字母"], "d"),
          ], widths=[1.6, 1.4], code_cols=(), size=36)),
    Scene("recap",
          "總結：[[r1]]先清理資料，再統計；[[r2]]map 負責數；[[r3]]要按次數排，就搬入 vector 再 sort；[[r4]]細過號可以將一個檔案當做輸入。第八部分完成！",
          BulletCard("今集重點", [("清理 → 統計", "r1"), ("map 數次數", "r2"), ("vector + sort 排名", "r3"), ("./top < text.txt", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]唔計少過三個字母嘅字，只印頭三名。[[next]]下一集開始第九部分：錯誤處理，第一集係 exception。多謝收睇，下次見！",
          EndCard("加條件：w.size() >= 3 先計；只印頭三名（the、dog、cat）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
