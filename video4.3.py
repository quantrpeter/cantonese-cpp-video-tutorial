#!/usr/bin/env python3
"""Video 44 (syllabus 4.3): vector 常用操作

A show() helper (const reference + range-for), then insert, erase, front, back and clear, each
result printed by a real run; nums[5] is caught by g++ 15's debug assertion at -O0, but with -O2 it really prints
whatever is in memory while nums.at(5) still stops with std::out_of_range. Run `python3 video44.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 44
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-03"
OPS = (CODE / "ops.cpp").read_text()
AT = (CODE / "at.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SHOW = OPS.split("#include <vector>\n\n")[1].split("int main")[0]
BODY = OPS.split("int main() {\n")[1].rsplit("}", 1)[0]
SKEL = "#include <iostream>\n#include <vector>\n\nint main() {\n}\n"
LINES = BODY.splitlines(True)
CO = "g++ -std=c++20 -Wall -Wextra ops.cpp -o ops"
CA = "g++ -std=c++20 -Wall -Wextra at.cpp -o at"

CA2 = "g++ -std=c++20 -Wall -Wextra -O2 at.cpp -o at"

(c1, r1, clr, c2, r2, c3, r3, cch, rch) = cpp.session({"ops.cpp": OPS, "at.cpp": AT}, [
    CO, "./ops", "clear", CA, "./at", CA2, "./at",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
out = r1.output.rstrip("\n").split("\n")
assert out == ["10 20 30 (size 3)", "5 10 20 30 (size 4)", "5 20 30 (size 3)", "5 30", "(size 0)"], out
assert "Assertion '__n < this->size()' failed" in r2.output and r2.code != 0, r2.output     # g++ 15 checks [] at -O0
o2 = cpp.visible(r3.output).rstrip("\n").split("\n")
garbage = o2[0]
assert "std::out_of_range" in r3.output and o2[-1] == "Aborted" and r3.code != 0, r3.output
assert "array subscript 5 is outside array bounds" in cpp.visible(c3.output)
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.strip() == "Amy Fay"

SAY = {"insert": "insert", "erase": "erase", "front": "front", "back": "back", "clear": "clear", "at()": "at",
       "nums[5]": "nums 五", "nums.at(5)": "nums 點 at 五", "begin()": "begin", "show": "show", "out_of_range": "out of range", "-O2": "dash O 二", "Assertion": "Assertion"}

s = Stage({"ops.cpp": SKEL, "at.cpp": AT}, title="vector 常用操作", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集學咗 push_back 同 range-based for。今集多學幾個 vector 常用嘅操作，同埋點樣避免用錯位置。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "insert · erase · front · back · at()")),
    Scene("goal",
          "今集會講：[[b1]]insert 同 erase：喺中間加入同刪除；[[b2]]front、back 同 clear；[[b3]]at 同中括號有乜分別。",
          BulletCard("今集學識", [("insert、erase", "b1"), ("front、back、clear", "b2"), ("at() vs []", "b3")])),
    Scene("show",
          "[[fn]]先寫一個 show 函數，印出成個 vector 同佢嘅 size。[[cref]]參數用 const reference，3.6 學過：唔使複製，又唔會改到；"
          "[[loop]]入面用 range-based for。",
          s.scene(Open("ops.cpp", mode="instant"), Type("ops.cpp", SHOW, before="int main", at="fn", rate=30), Mark(4, at="cref"),
                  Mark((5, 7), at="loop"))),
    Scene("ops",
          "[[init]]vector 一開始有十、二十、三十。[[ins]]insert 喺開頭加入五：begin 係開頭嘅位置；[[era]]erase 刪走第二個：begin 加一，即係第二個位；"
          "[[fb]]front 係第一個，back 係最後一個；[[clr]]clear 就清空晒。",
          s.scene(Mark(None), Type("ops.cpp", "".join(LINES[0:2]), before="}", last=True, at="init", rate=30),
                  Type("ops.cpp", "".join(LINES[2:4]), before="}", last=True, at="ins", rate=30),
                  Type("ops.cpp", "".join(LINES[4:6]), before="}", last=True, at="era", rate=30),
                  Type("ops.cpp", LINES[6], before="}", last=True, at="fb", rate=30),
                  Type("ops.cpp", "".join(LINES[7:]), before="}", last=True, at="clr", rate=30), Expect("ops.cpp", OPS))),
    Scene("run1",
          "[[cc]]編譯運行。[[o]]逐行睇：一開始三個；insert 之後，五排咗喺最前；erase 之後，十冇咗；front 係五，back 係三十；"
          "clear 之後，size 係零。",
          s.scene(Run(c1, at="cc"), Run(r1))),
    Scene("table",
          "[[t]]總結一下呢幾個操作：佢哋都係 vector 嘅成員函數，用點號呼叫。",
          TableCard("vector 常用操作", ["寫法", "做咩", "結果"], [
              (["nums.insert(nums.begin(), 5)", "喺開頭加入 5", out[1].split(" (")[0]], ("t", 0.3)),
              (["nums.erase(nums.begin() + 1)", "刪走第二個", out[2].split(" (")[0]], ("t", 0.8)),
              (["nums.front() / nums.back()", "第一個 / 最後一個", out[3].replace(" ", " / ")], ("t", 1.3)),
              (["nums.clear()", "清空", "（空）"], ("t", 1.8)),
          ], widths=[1.9, 1.2, 1], code_cols=(0, 2), size=36)),
    Scene("at",
          "最後講出界。[[open]]vector 得三個值，但係我哋攞第六個：[[sq]]一次用中括號，[[at]]一次用 at。[[cc]]用平時嘅指令編譯運行，"
          "[[o]]喺中括號嗰句已經停咗：Assertion failed。",
          s.scene(Run(clr, at="open"), Open("at.cpp", at="open"), Mark(6, at="sq"), Mark(7, at="at"), Mark(None, at="cc"),
                  Run(c2, at="cc"), Run(r2))),
    Scene("assert",
          "呢個係 g++ 十五嘅額外保護：[[debug]]冇開優化嘅時候，佢會幫你檢查中括號。[[but]]但係 C++ 標準冇要求中括號檢查；"
          "比賽同正式發佈，通常會加 -O2 開優化，[[o2]]試吓加 -O2 再編譯：今次 g++ 睇得出出界，畀咗個警告；照運行睇吓。",
          s.scene(Note("g++ 15 冇優化：幫你檢查 []\nC++ 標準冇保證", at="debug", where="editor"), Note(None, at="o2"),
                  Run(c3, at="o2"), Run(r3))),
    Scene("at_why",
          f"[[sq]]今次中括號乜都唔檢查，直接讀咗記憶體入面嘅嘢，印出{zh_int(int(garbage))}，仲當冇事發生，好危險。"
          "[[at]]at 就一定會檢查：位置五超出咗 size 三，即刻停低程式，仲話你知原因：out of range。",
          s.scene(Note(f"-O2：nums[5] 唔檢查 → {garbage}", at="sq", where="editor"),
                  Note("nums.at(5)：一定檢查\n→ out_of_range，停低", at="at", where="editor"))),
    Scene("rule",
          "所以：[[a]]中括號快，但係標準唔保證檢查，開咗優化，出界就係未定義行為；[[b]]at 慢少少，但係一定會檢查。[[tip]]學習同開發嘅時候，用 at 會幫你更快搵到錯。",
          TileCard("[] 定 at()？", [
              Tile("⚡", "nums[i]", "標準唔保證檢查\n-O2：出界係未定義行為", "a", RED),
              Tile("🛡️", "nums.at(i)", "會檢查\n出界：即刻報錯", "b", GREEN),
          ], cols=2, height=330, footer=("學習同開發：用 at() 搵錯", "tip"))),
    Scene("recap",
          "總結：[[r1]]insert 同 erase 用 begin 加位置；[[r2]]front 同 back 攞頭同尾，clear 清空；[[r3]]中括號唔保證檢查出界，at 一定會檢查。",
          BulletCard("今集重點", [("insert / erase：begin() + 位置", "r1"), ("front()、back()、clear()", "r2"),
                                ("[] 唔保證檢查；at() 一定檢查", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個裝住五個英文名嘅 vector，刪走第三個，喺最尾加多一個，再用 at 印出第一個同最後一個。"
          "[[next]]下一集，我哋學二維 vector。多謝收睇，下次見！",
          EndCard("整一個裝五個英文名嘅 vector，刪走第三個，最尾加多一個，用 at() 印出第一個同最後一個。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
