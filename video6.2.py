#!/usr/bin/env python3
"""Video 64 (syllabus 6.2): class 同成員函數

class BankAccount with deposit, withdraw and show; without public: every member is private and
acc.owner is a real "is private within this context" error; member functions use the object's
own data; withdrawing 150 from 70 really leaves -80, the problem 6.3 fixes.
Run `python3 video6.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 64
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-02"
FINAL = (CODE / "bank.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
HEAD = "#include <iostream>\n#include <string>\n\n"
CLASS = "class BankAccount" + FINAL.split("class BankAccount")[1].split("int main")[0]
BODY = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
V1 = HEAD + CLASS + "int main() {\n" + "".join(BODY[:5]) + "}\n"
NOPUB = V1.replace("public:\n", "")
SKEL = HEAD + "int main() {\n}\n"
CC = "g++ -std=c++20 -Wall -Wextra bank.cpp -o bank"

(c0, c1, r1, c2, r2, cch, rch) = cpp.session({"bank.cpp": NOPUB}, [
    CC, Write("bank.cpp", V1), CC, "./bank", Write("bank.cpp", FINAL), CC, "./bank",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "is private within this context" in cpp.visible(c0.output), c0.output[:300]
assert r1.output == "Amy: $70\n" and r2.output == "Amy: $70\nAmy: $-80\n"
assert c1.code == c2.code == cch.code == 0 and rch.output.strip() == "Amy: $1050"

SAY = {"class": "class", "struct": "struct", "public": "public", "private": "private", "BankAccount": "Bank Account",
       "acc.deposit(100)": "acc 點 deposit 一百", "deposit": "deposit", "withdraw": "withdraw", "show": "show", "acc": "acc"}

s = Stage({"bank.cpp": SKEL}, title="class 同成員函數", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集嘅 struct 只係裝資料。今集學 class：除咗資料，仲可以有自己嘅函數，叫成員函數。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "class · 成員函數 · public")),
    Scene("goal",
          "今集會講：[[b1]]class 同 struct 有乜分別；[[b2]]成員函數；[[b3]]用點號呼叫；[[b4]]每個物件有自己嘅資料。",
          BulletCard("今集學識", [("class vs struct", "b1"), ("成員函數 member function", "b2"), ("acc.deposit(100)", "b3"),
                                ("每個物件有自己嘅資料", "b4")])),
    Scene("define",
          "[[cls]]寫一個 BankAccount：[[data]]有戶主同餘額兩個資料；[[fns]]仲有三個成員函數：存錢、提錢、顯示。[[main]]main 開一個戶口，"
          "存一百，提三十，再顯示戶口嘅狀況。資料同操作，全部包埋喺一齊。",
          s.scene(Open("bank.cpp", mode="instant"),
                  Type("bank.cpp", "".join(CLASS.replace("public:\n", "").splitlines(True)[:4]), before="int main", at="cls", rate=60),
                  Type("bank.cpp", "".join(CLASS.replace("public:\n", "").splitlines(True)[4:]), before="int main", at="fns", rate=80),
                  Type("bank.cpp", "".join(BODY[:5]), before="}", last=True, at="main", rate=60), Expect("bank.cpp", NOPUB))),
    Scene("err",
          "[[cc]]編譯：[[err]]出錯！佢話 owner 係 private，喺 main 呢度用唔到。點解會咁？",
          s.scene(Run(c0, at="cc"), Scroll(at="err"))),
    Scene("public",
          "class 同 struct 幾乎一樣，唯一分別係：[[priv]]class 入面嘅嘢，預設係 private，即係外面唔用得。[[fix]]加一句 public 冒號，"
          "下面嘅嘢就公開俾外面用。[[cc]]再編譯運行，[[o]]Amy，七十蚊。",
          s.scene(Note("class 預設：private\nstruct 預設：public", at="priv", where="editor"), Note(None, at="fix"),
                  Type("bank.cpp", "public:\n", after="class BankAccount {\n", at="fix"), Expect("bank.cpp", V1),
                  Run(c1, at="cc", recall=True), Run(r1))),
    Scene("anatomy",
          "[[obj]]acc 係一個物件，即係 BankAccount 呢個 class 嘅一份實物；[[dot]]點號；[[fn]]deposit 係佢嘅成員函數；[[arg]]一百係參數。"
          "[[own]]函數入面直接寫 balance，用嘅就係 acc 自己嘅 balance。",
          AnatomyCard("acc.deposit(100);", [
              Part("acc", "物件 object", BLUE, "obj"), Part(".", "嘅", AMBER, "dot"),
              Part("deposit", "成員函數", PURPLE, "fn"), Part("(100)", "參數", GREEN, "arg"), Part(";", "", MUTED, "arg"),
          ], size=90, note=("函數入面嘅 balance ＝ acc 自己嘅 balance", "own"))),
    Scene("problem",
          "不過有個問題：[[type]]再提一百五十蚊，[[cc]]運行，[[o]]餘額變咗負八十！銀行戶口唔應該可以咁。[[why]]而且外面仲可以直接改 balance，"
          "完全冇保護。下一集，就用 private 保護佢。",
          s.scene(Type("bank.cpp", "".join(BODY[5:]), before="}", last=True, at="type", rate=30), Expect("bank.cpp", FINAL),
                  Run(c2, at="cc", recall=True), Run(r2), Note("餘額變咗 -80！", at="o", where="editor"))),
    Scene("recap",
          "總結：[[r1]]class 可以有資料，亦可以有成員函數；[[r2]]class 預設 private，要用 public 公開；[[r3]]用點號呼叫成員函數；"
          "[[r4]]成員函數入面，直接用自己物件嘅資料。",
          BulletCard("今集重點", [("class：資料 + 成員函數", "r1"), ("預設 private；public: 公開", "r2"), ("acc.deposit(100)", "r3"),
                                ("函數入面用自己嘅資料", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]為 BankAccount 加一個 addInterest 成員函數，按利率增加餘額。[[next]]下一集：封裝，用 private 保護資料。多謝收睇，下次見！",
          EndCard("為 BankAccount 加一個成員函數 addInterest(double rate)，按利率增加餘額。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
