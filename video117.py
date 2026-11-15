#!/usr/bin/env python3
"""Video 117 (syllabus 9.9): 小項目：記帳簿

Part 9 together: a Book class keeps a vector<Expense>, throws std::invalid_argument for amounts
<= 0, saves to expenses.csv with ofstream and loads it with ifstream + istringstream + getline.
Real session 1: "add abc bus" gives error: stod (std::stod threw), "add -5 gift" gives
error: amount <= 0, the list is lunch 12.5 / book 30, total 42.5; `cat expenses.csv` shows
12.5,lunch / 30,book. Real session 2 loads them back: after adding coffee the total is 50.
Run `python3 video117.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 117
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-09"
FINAL = (CODE / "book.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text, start=1):
    """1-based number of the first line at or after `start` containing `text`."""
    for i in range(start - 1, len(LINES)):
        if text in LINES[i]:
            return i + 1
    raise ValueError(text)


CC = "g++ -std=c++20 -Wall -Wextra book.cpp -o book"
IN1 = ["add 12.5 lunch", "add abc bus", "add -5 gift", "add 30 book", "list", "total", "quit"]
IN2 = ["add 7.5 coffee", "list", "total", "quit"]

(c1, r1, cat, r2, cch, rch) = cpp.session({"book.cpp": FINAL}, [
    CC, Input("./book", IN1), "cat expenses.csv", Input("./book", IN2),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["count", "quit"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output == ("add 12.5 lunch\nadd abc bus\nerror: stod\nadd -5 gift\nerror: amount <= 0\nadd 30 book\nlist\n"
                     "lunch 12.5\nbook 30\ntotal\n42.5\nquit\n"), r1.output
assert cat.output == "12.5,lunch\n30,book\n" and r2.output == "add 7.5 coffee\nlist\nlunch 12.5\nbook 30\ncoffee 7.5\ntotal\n50\nquit\n", r2.output
assert c1.code == cch.code == 0 and rch.output == "count\n3\nquit\n"

SAY = {"Book": "Book", "Expense": "Expense", "expenses.csv": "expenses 點 c s v", "CSV": "C S V", "std::stod": "S T D s to d",
       "stod": "s to d", "std::invalid_argument": "S T D invalid argument", "invalid_argument": "invalid argument", "ofstream": "o f stream",
       "ifstream": "i f stream", "istringstream": "i string stream", "getline": "get line", "save()": "save", "load()": "load",
       "lunch": "lunch", "book": "book", "coffee": "coffee", "bus": "bus", "gift": "gift", "abc": "a b c", "cat": "cat", "count": "count"}

s = Stage({"book.cpp": FINAL}, title="小項目：記帳簿", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第九部分最後一集，做一個記帳簿：輸入每筆支出，列出嚟、計總數，仲要存入檔案，下次開返都仲喺度。會用到 class、vector、檔案同 exception。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "class · vector · CSV · exception")),
    Scene("plan",
          "計劃：[[b1]]Expense 記住金額同用途；[[b2]]Book 管理所有支出，金額唔啱就 throw；[[b3]]用 CSV 檔案儲存同讀返；[[b4]]main 讀指令：add、list、total、quit。",
          BulletCard("計劃", [("struct Expense", "b1"), ("class Book：add 會 throw", "b2"), ("save / load：expenses.csv", "b3"), ("指令：add、list、total、quit", "b4")])),
    Scene("data",
          "程式已經寫好，我哋逐段睇。[[exp]]Expense 得兩個成員：金額同用途。[[ctor]]Book 一建立，就由檔案 load 返舊資料。[[add]]add 檢查金額，零或者負數就 throw invalid_argument，唔會加入 vector。",
          s.scene(Open("book.cpp", mode="instant"), Mark((ln("struct Expense"), ln("};")), at="exp"), Mark((ln("Book(const"), ln("Book(const") + 2), at="ctor"),
                  Mark((ln("void add"), ln("void add") + 5), at="add"))),
    Scene("files",
          "[[save]]save 用 ofstream，每筆寫一行：金額、逗號、用途，即係 CSV。[[load]]load 用 ifstream 逐行讀，[[split]]再用 istringstream 同 getline 按逗號拆開，stod 變返數字。",
          s.scene(Mark((ln("void save"), ln("void save") + 5), at="save"), Mark((ln("void load"), ln("void load") + 10), at="load"),
                  Mark((ln("std::istringstream row"), ln("items_.push_back({std::stod")), at="split"))),
    Scene("main",
          "[[loop]]main 不斷讀指令。[[add]]add 讀金額同用途，用 try 包住：stod 讀唔到數字會 throw，add 都可能 throw，[[catch]]一個 catch std::exception 全部接住。[[quit]]quit 就 save 再離開。",
          s.scene(Mark(ln("while (std::cin >> cmd)"), at="loop"), Mark((ln('if (cmd == "add")'), ln("book.add(std::stod")), at="add"),
                  Mark((ln("} catch (const std::exception"), ln('std::cout << "error: "')), at="catch"), Mark((ln('cmd == "quit"'), ln("book.save();", 60)), at="quit"))),
    Scene("run1",
          "[[cc]]編譯運行。[[t]]加 lunch 十二點五；abc 唔係數字，error stod；負五，error，金額要大過零；再加 book 三十；list 同 total：四十二點五；最後 quit，存檔離開。兩個錯誤都冇令程式當機，exception 俾 main 接住咗。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="t", type_rate=40))),
    Scene("csv",
          "[[cat]]睇吓 expenses.csv：兩行，每行金額逗號用途，錯嘅兩筆冇入到去。",
          s.scene(Run(cat, at="cat"))),
    Scene("run2",
          "[[t]]再開一次程式，加一杯 coffee，list：lunch 同 book 由檔案讀返嚟，加埋 coffee，總數五十。資料真係儲低咗。",
          s.scene(Run(r2, at="t", type_rate=26))),
    Scene("parts",
          "呢個小項目用咗：[[a]]class 同 vector 管資料；[[b]]exception 處理錯誤輸入；[[c]]fstream 讀寫檔案；[[d]]stringstream 拆 CSV。",
          TableCard("用咗乜？", ["概念", "喺邊度"], [
              (["class + vector（6.x、4.1）", "Book、items_"], "a"),
              (["exception（9.1、9.2）", "add 嘅 throw、main 嘅 catch"], "b"),
              (["fstream（9.6）", "save()、load()"], "c"),
              (["stringstream（9.7）", "拆 CSV 一行"], "d"),
          ], widths=[1.4, 1.6], code_cols=(), size=36)),
    Scene("recap",
          "總結：[[r1]]用 class 包住資料同操作；[[r2]]唔合法嘅輸入就 throw，喺 main 統一處理；[[r3]]CSV 簡單易讀，用 fstream 同 getline 就處理到；[[r4]]程式關咗，資料仲喺檔案入面。第九部分完成！",
          BulletCard("今集重點", [("class 包住資料", "r1"), ("throw / catch 處理錯誤", "r2"), ("CSV + fstream", "r3"), ("資料儲落檔案", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 count 指令，印出而家有幾多筆支出。[[next]]下一集開始第十部分：工具同工程，第一集係編譯三部曲。多謝收睇，下次見！",
          EndCard("加指令 count：Book 加 std::size_t count() const，印出有幾多筆支出（讀返檔案之後應該係 3）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
