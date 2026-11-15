#!/usr/bin/env python3
"""Video 47 (syllabus 4.6): std::array

Days in each month in a std::array<int, 12>: size(), at(), range-for; days.at(month) really
gives 31 for February (off by one) until it becomes month - 1; thirteen values are a real
compile-time "too many initializers" error. Run `python3 video47.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 47
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-06"
FINAL = (CODE / "days.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BUG = FINAL.replace("days.at(month - 1)", "days.at(month)")
EXTRA = FINAL.replace("30, 31, 30, 31};", "30, 31, 30, 31, 30};")
CC = "g++ -std=c++20 -Wall -Wextra days.cpp -o days"

(c1, r1, c2, r2, r3, clr, c3, cch, rch) = cpp.session({"days.cpp": BUG}, [
    CC, Input("./days", ["2"]), Write("days.cpp", FINAL), CC, Input("./days", ["2"]), Input("./days", ["12"]),
    Write("days.cpp", EXTRA), "clear", CC,
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("Days: 31\nYear: 365\n") and "Months: 12" in r1.output
assert r2.output.endswith("Days: 28\nYear: 365\n") and r3.output.endswith("Days: 31\nYear: 365\n")
assert "too many initializers" in cpp.visible(c3.output), c3.output
assert c1.code == c2.code == cch.code == 0 and "Highest: 29.5" in rch.output

SAY = {"std::array<int, 12>": "S T D array int 十二", "std::array": "S T D array", "days.at(month)": "days at month",
       "days.at(month - 1)": "days at month 減一", "size()": "size", "at()": "at"}

s = Stage({"days.cpp": BUG}, title="std::array：每月日數", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集嘅 C 風格陣列有唔少陷阱。今集學 std::array：大小一樣固定，但係好用好多。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::array<型別, 大小>")),
    Scene("goal",
          "今集會講：[[b1]]點樣宣告 std::array；[[b2]]size 同 at；[[b3]]同 C 風格陣列比較。",
          BulletCard("今集學識", [("std::array<int, 12>", "b1"), ("size() 同 at()", "b2"), ("同 C 陣列比較", "b3")])),
    Scene("declare",
          "[[inc]]要 include array。[[decl]]角括號入面有兩樣嘢：型別 int，同埋大小十二，一年十二個月。[[init]]大括號入面，就係每個月嘅日數，"
          "太長可以分兩行寫。[[size]]佢有 size，知道自己有幾多格。",
          s.scene(Open("days.cpp", at="inc"), Mark(1, at="inc"), Mark(5, at="decl"), Mark((5, 6), at="init"), Mark(7, at="size"))),
    Scene("run1",
          "[[read]]讀入月份，用 at 攞嗰個月嘅日數。[[cc]]編譯運行，[[t]]輸入二月，[[o]]三十一日？二月點會有三十一日！問題出喺邊？",
          s.scene(Mark(11, at="read"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1, keys=("t",)),
                  Note("2 月有 31 日？", at="o", where="editor"))),
    Scene("fix",
          "因為位置由零開始：[[idx]]一月係 at(0)，二月係 at(1)。我哋攞咗 at(2)，即係三月。[[fix]]要用月份減一。"
          "[[cc]]再運行，[[t1]]二月，[[o1]]二十八日；[[t2]]十二月，[[o2]]三十一日，啱晒。位置由零開始，記住要減一。",
          s.scene(Note(None), Replace("days.cpp", "days.at(month)", "days.at(month - 1)", at="fix"), Expect("days.cpp", FINAL),
                  Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=("t1",)), Run(r3, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("year",
          "[[loop]]std::array 一樣可以用 range-based for：將十二個月加埋，[[o]]一年係三百六十五日。",
          s.scene(Mark((13, 15), at="loop"), Note("for (int d : days)\n加埋 = 365", at="o", where="editor"))),
    Scene("extra",
          "大小係型別嘅一部分，編譯器會幫你檢查。[[type]]如果唔小心多打一個數，變咗十三個，[[cc]]編譯：[[err]]出錯，初始值太多。"
          "[[undo]]刪返佢。",
          s.scene(Note(None), Mark(None), Replace("days.cpp", "30, 31, 30, 31};", "30, 31, 30, 31, 30};", at="type"),
                  Expect("days.cpp", EXTRA), Run(clr, at="cc"), Run(c3, recall=True),
                  Replace("days.cpp", "30, 31, 30, 31, 30};", "30, 31, 30, 31};", at="undo"), Expect("days.cpp", FINAL))),
    Scene("compare",
          "同 C 風格陣列比較：[[s]]std::array 有 size；[[a]]有 at 檢查出界；[[f]]傳入函數唔會退化，仲知道自己幾大；"
          "[[c]]可以用等號成個複製。[[rule]]大小固定嘅資料，就用 std::array；會變嘅，就用 vector。",
          TableCard("int a[12] vs std::array<int, 12>", ["", "int a[12]", "std::array"], [
              (["size()", "冇", "有"], "s"),
              (["at() 檢查出界", "冇", "有"], "a"),
              (["傳入函數", "退化做指標", "完整傳入"], "f"),
              (["= 複製", "唔得", "得"], "c"),
          ], widths=[1.2, 1, 1], code_cols=(), size=40, note=("大小固定：std::array；會變：std::vector", "rule"))),
    Scene("recap",
          "總結：[[r1]]std::array<型別, 大小>，大小固定；[[r2]]有 size 同 at；[[r3]]編譯器會檢查初始值嘅數量；[[r4]]傳入函數唔會退化。",
          BulletCard("今集重點", [("std::array<int, 12>：大小固定", "r1"), ("size()、at()、range-for", "r2"),
                                ("初始值多咗：編譯錯誤", "r3"), ("傳入函數唔會退化", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 std::array 裝一個星期七日嘅氣溫，計平均溫度同最高溫度。[[next]]下一集，我哋學字串嘅常用操作。多謝收睇，下次見！",
          EndCard("用 std::array<double, 7> 裝一星期嘅氣溫，計平均溫度同最高溫度。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
