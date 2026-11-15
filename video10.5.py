#!/usr/bin/env python3
"""Video 122 (syllabus 10.5): 單元測試

doctest (one header, doctest.h 2.4.11) tests isLeapYear. With the simple `year % 4 == 0` the real
run reports test.cpp:11 CHECK_FALSE( isLeapYear(1900) ) is NOT correct, "test cases: 2 | 1 passed
| 1 failed", Status: FAILURE!. With the century rule the run prints 2 passed, Status: SUCCESS!.
Run `python3 video122.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 122
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-05"
LEAP = (CODE / "leap.cpp").read_text()
TEST = (CODE / "test.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
RULE = "(year % 4 == 0 && year % 100 != 0) ||\n           year % 400 == 0"
LEAP0 = LEAP.replace(RULE, "year % 4 == 0")
SUPPORT = {f: (CODE / f).read_text() for f in ["leap.h", "doctest.h"]}
CC = "g++ -std=c++20 test.cpp leap.cpp -o test"

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"leap.cpp": LEAP0, "test.cpp": TEST, **SUPPORT}, [
    CC, "./test", "clear", Write("leap.cpp", LEAP), CC, "./test",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp leap.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
v1, v2 = cpp.visible(r1.output), cpp.visible(r2.output)
assert "CHECK_FALSE( isLeapYear(1900) ) is NOT correct!" in v1 and "1 passed | 1 failed" in v1 and "FAILURE" in v1 and r1.code != 0, v1
assert "2 passed | 0 failed" in v2 and "SUCCESS" in v2 and r2.code == 0, v2
assert c1.code == c2.code == cch.code == 0 and "3 passed | 0 failed" in cpp.visible(rch.output)

SAY = {"doctest": "doc test", "doctest.h": "doc test 點 h", "TEST_CASE": "TEST CASE", "CHECK": "CHECK", "CHECK_FALSE": "CHECK FALSE",
       "isLeapYear": "is leap year", "DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN": "doctest config implement with main", "FAILURE": "FAILURE",
       "SUCCESS": "SUCCESS", "leap.cpp": "leap 點 c p p", "test.cpp": "test 點 c p p", "1900": "一九零零", "2000": "二零零零",
       "2024": "二零二四", "2023": "二零二三", "2100": "二一零零", "2400": "二四零零"}

s = Stage({"leap.cpp": LEAP0, "test.cpp": TEST}, title="單元測試", code_px=24, split=0.45)

scenes = [
    Scene("intro",
          "歡迎返嚟！每次改完 code，都要人手試一次？好易漏。單元測試就係寫一啲小程式，自動檢查你嘅函數。今集用 doctest：成個框架只係一個 header 檔。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "doctest · TEST_CASE · CHECK")),
    Scene("goal",
          "今集會講：[[b1]]寫 TEST_CASE；[[b2]]CHECK 同 CHECK_FALSE；[[b3]]睇失敗報告；[[b4]]修好再跑一次。",
          BulletCard("今集學識", [("TEST_CASE(\"名\")", "b1"), ("CHECK、CHECK_FALSE", "b2"), ("失敗報告", "b3"), ("修好：全部 pass", "b4")])),
    Scene("leap",
          "[[open]]isLeapYear 判斷閏年，寫法好簡單：可以俾四整除就係閏年。啱唔啱呢？",
          s.scene(Open("leap.cpp", at="open"), Mark((3, 5), at="open"))),
    Scene("test",
          "[[open]]test.cpp：[[main]]第一行叫 doctest 幫我哋整 main；[[case1]]第一個 TEST_CASE 試普通年份：二零二四係，二零二三唔係；[[case2]]第二個試世紀年：一九零零唔係，二零零零係。",
          s.scene(Open("test.cpp", at="open"), Mark((1, 2), at="main"), Mark((5, 8), at="case1"), Mark((10, 13), at="case2"))),
    Scene("run1",
          "[[cc]]編譯，連埋 leap.cpp。運行：[[o]]一個失敗！第十一行：CHECK_FALSE 一九零零，結果唔啱。兩個 test case，一個 pass，一個 fail。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("rule",
          "[[r]]真正嘅規則：可以俾四整除，但係唔可以俾一百整除；[[e]]除非可以俾四百整除。所以一九零零唔係閏年，二零零零係。",
          TableCard("閏年規則", ["年份", "÷4", "÷100", "÷400", "閏年？"], [
              (["2024", "得", "唔得", "唔得", "係"], "r"),
              (["1900", "得", "得", "唔得", "唔係"], "r", RED),
              (["2000", "得", "得", "得", "係"], "e", GREEN),
          ], widths=[1, 0.7, 0.8, 0.8, 0.8], code_cols=(), size=40)),
    Scene("fix",
          "[[type]]改返 isLeapYear。[[cc]]再編譯運行：[[o]]兩個 test case 全部 pass，SUCCESS。以後再改呢個函數，一跑測試就知有冇整壞嘢，唔使再人手逐個試。",
          s.scene(Open("leap.cpp", at="type"), Replace("leap.cpp", "year % 4 == 0;", RULE + ";", at="type", rate=40), Expect("leap.cpp", LEAP),
                  Run(clr, at="cc"), Run(c2), Run(r2, at="o"))),
    Scene("why",
          "測試嘅好處：[[auto]]自動，幾秒就檢查晒；[[edge]]逼你諗清楚邊界情況，例如一九零零；[[safe]]改 code 嘅時候有安全網。",
          BulletCard("點解要測試", [("自動：一按就跑", "auto"), ("逼你諗邊界情況", "edge"), ("改 code 有安全網", "safe")])),
    Scene("recap",
          "總結：[[r1]]doctest 得一個 header；[[r2]]TEST_CASE 包住一組檢查；[[r3]]CHECK 同 CHECK_FALSE 檢查結果，失敗會講檔名同行號；[[r4]]測試要包括邊界情況。",
          BulletCard("今集重點", [("doctest.h", "r1"), ("TEST_CASE", "r2"), ("CHECK / CHECK_FALSE", "r3"), ("測試邊界", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加多一個 TEST_CASE，試二一零零唔係閏年，二四零零係。[[next]]下一集：用第三方庫。多謝收睇，下次見！",
          EndCard("加 TEST_CASE(\"more centuries\")：CHECK_FALSE(isLeapYear(2100))、CHECK(isLeapYear(2400))。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
