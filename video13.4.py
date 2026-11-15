#!/usr/bin/env python3
"""Video 152 (syllabus 13.4): 圖書館管理系統（一）：設計

Designing before coding: nouns become classes (Book, Member, Library), "who owns what" decides the
containers (Library owns a vector<Book> and a map<int, Member>), and a borrowed book stores the
member's id in a std::optional<int> instead of a pointer, so nothing dangles when containers grow
(8.3). The first version adds three books and two members and really lists them.
Run `python3 video13.4.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 152
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "13-04"
FINAL = (CODE / "library.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text, start=1):
    return next(i + 1 for i in range(start - 1, len(LINES)) if text in LINES[i])


(c1, r1, cch, rch) = cpp.session({"library.cpp": FINAL}, [
    "g++ -std=c++20 -Wall -Wextra library.cpp -o lib", "./lib", Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "1 Harbour Stories / Chan\n2 Night Market / Wong\n3 Learning C++ / Lee\n2 members\n" and c1.code == cch.code == 0 and rch.output == "2\n"

SAY = {"Book": "Book", "Member": "Member", "Library": "Library", "borrowedBy": "borrowed by", "std::optional<int>": "optional int",
       "optional": "optional", "vector<Book>": "vector Book", "map<int, Member>": "map int Member", "addBook": "add book", "addMember": "add member",
       "list": "list", "nextBook_": "next book 底線", "id": "I D", "Harbour Stories": "Harbour Stories", "Night Market": "Night Market",
       "Learning C++": "Learning C 加加", "countBooks": "count books"}

s = Stage({"library.cpp": FINAL}, title="圖書館系統（一）：設計", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！最後一個綜合項目：圖書館管理系統，分兩集。今集唔急住寫，先設計：有咩類別、邊個擁有邊個、用咩容器。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "類別 · 擁有權 · 容器")),
    Scene("needs",
          "系統要做乜？[[b1]]加書、加會員；[[b2]]搵書；[[b3]]借書、還書；[[b4]]儲存同讀返。今集做第一樣，下集做晒其他。",
          BulletCard("需求", [("加書、加會員", "b1"), ("用書名搵書", "b2"), ("借書、還書", "b3"), ("存檔、讀檔", "b4")])),
    Scene("nouns",
          "[[nouns]]設計嘅第一步：將需求入面嘅名詞變成類別：書、會員、圖書館。[[data]]書有編號、書名、作者，仲有「借咗俾邊個」；會員有編號同名。[[lib]]圖書館負責管理晒佢哋。",
          TableCard("名詞 → 類別", ["類別", "資料"], [
              (["Book", "id、title、author、borrowedBy"], "nouns"),
              (["Member", "id、name"], "data"),
              (["Library", "所有書、所有會員"], "lib", GREEN),
          ], widths=[1, 2.2], code_cols=(0,), size=40)),
    Scene("owner",
          "[[own]]擁有權：圖書館擁有所有書同會員，用 vector 同 map 裝住，佢消失就一齊消失。[[ref]]書借咗俾邊個，只記住會員嘅編號，唔用指標。[[why]]因為 vector 變大會搬家，舊指標會失效，8.3 講過；編號就永遠安全。",
          BoxesCard("邊個擁有邊個", [
              BoxRow([Box("Library", "擁有", "", at="own", color=PURPLE, w=360, key="l")]),
              BoxRow([Box("vector<Book>", "books_", "", at="own", color=BLUE, w=320, key="b"), Box("map<int, Member>", "members_", "", at="own", color=BLUE, w=360, key="m")], gap=60),
              BoxRow([Box("Book::borrowedBy", "optional<int>：會員編號", "", at="ref", color=AMBER, w=560)]),
          ], notes=[("用編號，唔用指標：唔會懸空", "why")], top=CONTENT_TOP - 20, row_h=200, box_h=95, size=34)),
    Scene("code",
          "[[book]]Book 同 Member 係簡單嘅 struct；[[opt]]borrowedBy 係 optional int：冇值就係喺架上。[[add]]Library 嘅 addBook 同 addMember 自動派編號；[[list]]list 印晒所有書，借咗嘅加 out。[[priv]]資料全部 private。",
          s.scene(Open("library.cpp", mode="instant"), Mark((ln("struct Book"), ln("};")), at="book"), Mark(ln("std::optional<int> borrowedBy;"), at="opt"),
                  Mark((ln("int addBook"), ln("return nextMember_++;") + 1), at="add"), Mark((ln("void list() const"), ln('std::cout << members_.size()') + 1), at="list"),
                  Mark((ln("private:"), ln("int nextMember_ = 1;")), at="priv"))),
    Scene("run",
          "[[cc]]main 加三本書，兩個會員，再 list。編譯運行：[[o]]三本書，各有編號同作者；兩個會員。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("recap",
          "總結：[[r1]]先列需求，名詞變類別；[[r2]]諗清楚擁有權：Library 擁有書同會員；[[r3]]用編號連結，唔用會失效嘅指標；[[r4]]optional 表示可能冇。下集完成所有功能。",
          BulletCard("今集重點", [("需求 → 類別", "r1"), ("擁有權決定容器", "r2"), ("用編號，唔用指標", "r3"), ("optional：可能冇", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]幫 Library 加一個 countBooks，數某個作者有幾多本書。[[next]]下一集：完成圖書館系統：搵書、借還、存檔同測試。多謝收睇，下次見！",
          EndCard("加 int countBooks(const std::string& author) const：數作者係 author 嘅書。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
