#!/usr/bin/env python3
"""Video 110 (syllabus 9.2): 標準同自訂 exception

v.at(5) on a 3-element vector really throws std::out_of_range ("vector::_M_range_check: __n
(which is 5) >= this->size() (which is 3)"). A custom NotEnoughMoney derives from
std::runtime_error. With catch (std::exception) first, g++ really warns "will be caught by
earlier handler" and the run prints "other: short by 130"; in the right order it prints
"money: short by 130"; the balance stays 70. Run `python3 video9.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 110
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-02"
FINAL = (CODE / "errors.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
A = "    } catch (const NotEnoughMoney& e) {\n        std::cout << \"money: \" << e.what() << '\\n';\n"
B = "    } catch (const std::exception& e) {\n        std::cout << \"other: \" << e.what() << '\\n';\n"
WRONG = FINAL.replace(A + B, B + A)
CLASS = "class NotEnoughMoney" + FINAL.split("class NotEnoughMoney")[1].split("int main")[0]
MONEY = "    int balance = 100;" + FINAL.split("    int balance = 100;")[1].rsplit("}\n", 1)[0]
V1 = FINAL.replace(CLASS, "").replace(MONEY, "").replace("#include <string>\n", "")
CC = "g++ -std=c++20 -Wall -Wextra errors.cpp -o err"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"errors.cpp": V1}, [
    CC, "./err", "clear", Write("errors.cpp", WRONG), CC, "./err", "clear", Write("errors.cpp", FINAL), CC, "./err",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
RANGE = "range: vector::_M_range_check: __n (which is 5) >= this->size() (which is 3)\n"
assert r1.output == RANGE and r2.output == RANGE + "other: short by 130\n70\n" and r3.output == RANGE + "money: short by 130\n70\n", r3.output
assert "will be caught by earlier handler" in cpp.visible(c2.output) and c2.code == 0
assert c1.code == c3.code == cch.code == 0 and rch.output == "bad age -5\n"

SAY = {"std::exception": "S T D exception", "std::runtime_error": "S T D runtime error", "runtime_error": "runtime error",
       "std::out_of_range": "S T D out of range", "out_of_range": "out of range", "std::logic_error": "S T D logic error",
       "logic_error": "logic error", "std::invalid_argument": "S T D invalid argument", "invalid_argument": "invalid argument",
       "NotEnoughMoney": "Not Enough Money", "withdraw": "withdraw", "v.at(5)": "v 點 at 五", "at": "at", "what()": "what",
       "catch": "catch", "throw": "throw", "BadAge": "Bad Age"}

s = Stage({"errors.cpp": V1}, title="標準同自訂 exception", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！標準庫自己都會 throw exception，而且分好多種。今集睇標準 exception 嘅家族，再自己寫一個新嘅 exception 類別。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "out_of_range · runtime_error · 自訂")),
    Scene("goal",
          "今集會講：[[b1]]標準庫會 throw 乜；[[b2]]exception 嘅家族；[[b3]]繼承 runtime_error 寫自己嘅；[[b4]]catch 嘅次序。",
          BulletCard("今集學識", [("v.at(5) → out_of_range", "b1"), ("std::exception 家族", "b2"), ("class X : public std::runtime_error", "b3"),
                                ("catch：由具體到一般", "b4")])),
    Scene("at",
          "[[at]]4.3 講過，at 會檢查範圍。三個元素，攞第五個，[[c]]佢 throw 一個 out_of_range，我哋接住，印 what。[[cc]]編譯運行，[[o]]說明講得好清楚：五大過等於 size 三。程式冇當機，繼續行。",
          s.scene(Open("errors.cpp", at="at"), Mark(8, at="at"), Mark((9, 11), at="c"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("family",
          "[[root]]全部標準 exception 都由 std::exception 衍生，都有 what。[[logic]]logic_error 係程式邏輯錯，例如 out_of_range、invalid_argument；"
          "[[rt]]runtime_error 係運行時先知嘅問題，例如檔案開唔到、錢唔夠。",
          BoxesCard("std::exception 家族", [
              BoxRow([Box("", "std::exception", "what()", at="root", color=PURPLE, w=420, key="r")]),
              BoxRow([Box("", "logic_error", "", at="logic", color=BLUE, w=340, key="l"), Box("", "runtime_error", "", at="rt", color=AMBER, w=400, key="t")], gap=60),
              BoxRow([Box("", "out_of_range", "", at="logic", color=BLUE, w=340, key="o"), Box("", "NotEnoughMoney", "我哋自己寫", at="rt", color=GREEN, w=400, key="n")], gap=60),
          ], notes=[("下面嘅都係上面嘅一種", "rt")], top=CONTENT_TOP - 20, row_h=190, box_h=95, size=38)),
    Scene("custom",
          "[[cls]]自己寫：NotEnoughMoney 繼承 runtime_error，[[ctor]]建構子將說明傳上去：差幾多錢。[[wd]]withdraw 唔夠錢就 throw。[[two]]main 先提三十，再提二百。"
          "[[order]]catch 嘅次序：先寫 std::exception，再寫 NotEnoughMoney。咁寫啱唔啱？",
          s.scene(Run(clr, at="cls"), Replace("errors.cpp", "#include <stdexcept>\n", "#include <stdexcept>\n#include <string>\n", at="cls", rate=40),
                  Type("errors.cpp", CLASS, before="int main", rate=130), Mark((6, 10), at="ctor"), Mark((12, 17), at="wd"),
                  Type("errors.cpp", MONEY.replace(A + B, B + A), before="}", last=True, at="two", rate=130), Expect("errors.cpp", WRONG),
                  Mark((30, 33), at="order"))),
    Scene("wrong",
          "[[cc]]編譯：[[warn]]有警告：NotEnoughMoney 會俾前面嗰個 handler 接咗。運行：[[o]]印 other，唔係 money！因為 NotEnoughMoney 都係一種 std::exception，第一個 catch 已經接咗。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Scroll(at="warn"), Run(r2, at="o"))),
    Scene("fix",
          "[[type]]調轉次序：具體嘅放前，一般嘅放後。[[cc]]運行：[[o]]money，short by 一百三十；餘額係七十，第二次提款冇扣錢。",
          s.scene(Run(clr2, at="type"), Replace("errors.cpp", B + A, A + B, at="type", rate=60), Expect("errors.cpp", FINAL), Mark((30, 33), at="type"),
                  Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("recap",
          "總結：[[r1]]標準 exception 全部由 std::exception 衍生，用 what 攞說明；[[r2]]logic_error 同 runtime_error 兩大類；[[r3]]自己嘅 exception 繼承 runtime_error，"
          "將說明傳上去；[[r4]]catch 由具體寫到一般。",
          BulletCard("今集重點", [("std::exception + what()", "r1"), ("logic_error / runtime_error", "r2"), ("自訂：繼承 runtime_error", "r3"),
                                ("catch：具體 → 一般", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 BadAge，繼承 invalid_argument；throw 一個，再用 logic_error 接住，印出說明。[[next]]下一集：noexcept 同 exception safety。多謝收睇，下次見！",
          EndCard("寫 class BadAge : public std::invalid_argument；throw BadAge(-5)，用 catch (const std::logic_error&) 接住，印 bad age -5。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
