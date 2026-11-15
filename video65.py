#!/usr/bin/env python3
"""Video 65 (syllabus 6.3): 封裝：public / private

BankAccount with a private balance_ and public deposit/withdraw that check their input; setting
acc.balance_ = -1000 from main is a real "is private within this context" error; withdrawing 150
from 70 is refused ("Not enough money"), so the balance can never go negative; a getter.
Run `python3 video65.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 65
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-03"
FINAL = (CODE / "bank.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
HEAD = "#include <iostream>\n\n"
CLASS = "class BankAccount" + FINAL.split("class BankAccount")[1].split("int main")[0]
BODY = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
HACK = HEAD + CLASS + "int main() {\n    BankAccount acc;\n    acc.balance_ = -1000;\n}\n"
SKEL = HEAD + "int main() {\n}\n"
CC = "g++ -std=c++20 -Wall -Wextra bank.cpp -o bank"

(c0, clr, c1, r1, cch, rch) = cpp.session({"bank.cpp": HACK}, [
    CC, "clear", Write("bank.cpp", FINAL), CC, "./bank",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "'double BankAccount::balance_' is private within this context" in cpp.visible(c0.output), c0.output[:300]
assert r1.output == "Not enough money\nBalance: 70\n" and c1.code == cch.code == 0 and rch.output.strip() == "60 40"

SAY = {"private": "private", "public": "public", "balance_": "balance 底線", "balance()": "balance", "deposit": "deposit",
       "withdraw": "withdraw", "invariant": "invariant", "getter": "getter", "Not enough money": "Not enough money"}

s = Stage({"bank.cpp": SKEL}, title="封裝：public / private", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集嘅戶口，餘額可以變負數，外面仲可以隨便改。今集用封裝保護佢。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "private · public · 保護資料")),
    Scene("goal",
          "今集會講：[[b1]]用 private 收埋資料；[[b2]]用 public 成員函數做檢查；[[b3]]不變條件；[[b4]]只讀嘅 getter。",
          BulletCard("今集學識", [("private：收埋資料", "b1"), ("public 函數：做檢查", "b2"), ("不變條件 invariant", "b3"),
                                ("getter：只讀", "b4")])),
    Scene("class",
          "[[pub]]public 下面係大家用得嘅：存錢同提錢。[[check]]兩個都會先檢查：金額要大過零，提錢唔可以多過餘額，唔啱就回傳 false。"
          "[[priv]]private 下面係餘額，名後面加底線，代表佢係私家嘅成員。",
          s.scene(Open("bank.cpp", mode="instant"), Type("bank.cpp", CLASS, before="int main", at="pub", rate=70),
                  Mark((12, 17), at="check"), Mark((23, 24), at="priv"))),
    Scene("hack",
          "[[try]]如果 main 想直接將餘額改做負一千……[[cc]]編譯：[[err]]出錯，balance 底線係 private，外面根本掂唔到；g++ 仲提你，可以經 balance() 呢個函數攞佢個值。",
          s.scene(Mark(None), Type("bank.cpp", "    BankAccount acc;\n    acc.balance_ = -1000;\n", before="}", last=True, at="try"),
                  Expect("bank.cpp", HACK), Run(c0, at="cc"), Note("private：外面改唔到", at="err", where="editor"))),
    Scene("use",
          "[[fix]]所以 main 只可以經公開嘅函數做嘢：存一百，提三十，[[big]]再試吓提一百五十，withdraw 回傳 false，就印句提示。"
          "[[cc]]編譯運行，[[o]]唔夠錢；餘額七十，冇變負數。",
          s.scene(Note(None), Run(clr, at="fix"), Replace("bank.cpp", "    BankAccount acc;\n    acc.balance_ = -1000;\n", "".join(BODY), at="fix", rate=40),
                  Expect("bank.cpp", FINAL), Mark((31, 33), at="big"), Run(c1, at="cc", recall=True), Run(r1))),
    Scene("invariant",
          "呢個就係封裝嘅意義：[[rule]]戶口有一條規則，餘額永遠唔可以係負數，叫做不變條件。[[only]]資料係 private，只有成員函數改得到；"
          "[[safe]]只要呢幾個函數檢查好，規則就一定成立，唔怕外面亂改。",
          TileCard("封裝：保護不變條件", [
              Tile("📏", "規則", "餘額永遠 ≥ 0", "rule", BLUE),
              Tile("🔒", "private", "外面改唔到 balance_", "only", PURPLE),
              Tile("✅", "public 函數", "每次改之前都檢查", "safe", GREEN),
          ], height=330)),
    Scene("getter",
          "[[get]]外面想知餘額，就用 balance 呢個 getter：佢只係交個值出嚟，唔俾人改。[[style]]一般做法：資料 private，函數 public。",
          s.scene(Mark(None), Mark((19, 21), at="get"), Note("getter：只讀出\n唔俾改", at="get", where="editor"))),
    Scene("recap",
          "總結：[[r1]]資料放 private，外面掂唔到；[[r2]]public 成員函數係唯一嘅入口，入面做檢查；[[r3]]咁就保證到不變條件；"
          "[[r4]]想俾人睇，就寫一個 getter。",
          BulletCard("今集重點", [("資料：private", "r1"), ("public 函數：檢查後先改", "r2"), ("保證不變條件", "r3"), ("getter：只讀", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 transfer 成員函數，由一個戶口轉錢去另一個戶口，唔夠錢就唔轉。"
          "[[next]]下一集，我哋學建構子，令物件一出世就有啱嘅值。多謝收睇，下次見！",
          EndCard("加成員函數 transfer(BankAccount& other, double amount)：唔夠錢就唔轉，回傳 false。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
