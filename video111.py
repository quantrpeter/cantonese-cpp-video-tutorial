#!/usr/bin/env python3
"""Video 111 (syllabus 9.3): noexcept 同 exception safety

A noexcept function that throws: g++ really warns "'throw' will always call 'terminate'" and
the run aborts even inside try/catch. A vector growing to 3 Items really calls the copy
constructor (copy copy copy) while Item's move constructor is not noexcept, and the move
constructor once it is (move move move): the strong guarantee at work.
Run `python3 video111.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 111
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-03"
PROMISE = (CODE / "promise.cpp").read_text()
GROW = (CODE / "grow.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
G1 = GROW.replace("Item(Item&&) noexcept", "Item(Item&&)")

(cp, rp, clr, c1, r1, c2, r2, cch, rch) = cpp.session({"promise.cpp": PROMISE, "grow.cpp": G1}, [
    "g++ -std=c++20 -Wall -Wextra promise.cpp -o pr", "./pr", "clear",
    "g++ -std=c++20 -Wall -Wextra grow.cpp -o grow", "./grow", Write("grow.cpp", GROW), "g++ -std=c++20 -Wall -Wextra grow.cpp -o grow", "./grow",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "'throw' will always call 'terminate'" in cpp.visible(cp.output) and cp.code == 0
assert rp.output.startswith("terminate called after throwing") and "caught" not in rp.output and rp.code != 0, rp.output
assert r1.output == "copy copy copy \n" and r2.output == "move move move \n", (r1.output, r2.output)
assert c1.code == c2.code == cch.code == 0 and rch.output == "1 0\n"

SAY = {"noexcept": "no except", "terminate": "terminate", "std::terminate": "S T D terminate", "risky": "risky", "Item": "Item",
       "emplace_back": "emplace back", "copy": "copy", "move": "move", "strong guarantee": "strong guarantee", "RAII": "R A I I",
       "is_nothrow_move_constructible_v": "is nothrow move constructible", "Safe": "Safe", "Risky": "Risky", "-Wterminate": "W terminate"}

s = Stage({"promise.cpp": PROMISE, "grow.cpp": G1}, title="noexcept 同 exception safety", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！出錯嘅時候，程式嘅資料會唔會變成一半新一半舊？今集講 exception safety 嘅三種保證，同埋 noexcept：一個「我唔會 throw」嘅承諾。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "保證 · noexcept · RAII")),
    Scene("goal",
          "今集會講：[[b1]]三種 exception safety 保證；[[b2]]noexcept 嘅承諾；[[b3]]承諾破咗會點；[[b4]]點解 vector 在乎 noexcept。",
          BulletCard("今集學識", [("basic、strong、no-throw", "b1"), ("noexcept", "b2"), ("throw 咗：terminate", "b3"), ("vector：move 定 copy", "b4")])),
    Scene("levels",
          "出錯之後嘅三種保證：[[basic]]basic：冇漏資源，物件仲用得，但係值可能變咗；[[strong]]strong：好似冇發生過，全部還原；[[nothrow]]no-throw：根本唔會出錯。",
          TableCard("exception safety 保證", ["等級", "出錯之後"], [
              (["basic", "冇漏嘢，物件仲有效"], "basic"),
              (["strong", "完全還原，好似冇做過"], "strong", BLUE),
              (["no-throw（noexcept）", "唔會 throw"], "nothrow", GREEN),
          ], widths=[1.2, 1.8], code_cols=(0,), size=40)),
    Scene("promise",
          "[[open]]risky 寫咗 noexcept，即係承諾唔會 throw，但係入面偏偏 throw。[[try]]main 用 try catch 包住。[[cc]]編譯：[[warn]]g++ 警告：呢個 throw 一定會叫 terminate。"
          "運行：[[o]]真係 terminate，catch 都接唔到！",
          s.scene(Open("promise.cpp", at="open"), Mark((4, 6), at="open"), Mark((9, 13), at="try"), Mark(None, at="cc"),
                  Run(cp, at="cc"), Run(rp, at="o"))),
    Scene("meaning",
          "[[p]]noexcept 唔係「唔准 throw」嘅檢查，而係一個承諾；[[broken]]承諾一破，程式即刻結束，冇得救。[[use]]所以只喺真係唔會出錯嘅函數用，例如搬移、swap、解構子。",
          BulletCard("noexcept 係承諾", [("寫咗：話俾所有人知唔會 throw", "p"), ("破咗：std::terminate，冇得 catch", "broken"),
                                         ("用喺搬移、swap、解構子", "use")])),
    Scene("copy",
          "有咩好處？[[open]]Item 嘅複製印 copy，搬移印 move，但係搬移冇寫 noexcept。[[loop]]vector 放三個 Item，中間會搬家兩次。[[cc]]編譯運行：[[o]]三次都係 copy！明明有搬移建構子，vector 都唔用。點解？",
          s.scene(Run(clr, at="open"), Open("grow.cpp", at="open"), Mark((6, 11), at="open"), Mark((15, 17), at="loop"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("why",
          "[[strong]]vector 搬家要做到 strong 保證：中途出錯，舊嘅資料要完好。[[risk]]如果搬移可能 throw，搬咗一半就冇得還原，所以佢寧願慢慢複製。"
          "[[type]]幫搬移加 noexcept。[[cc]]運行：[[o]]move、move、move。加一個字，就快咗好多。",
          s.scene(Replace("grow.cpp", "Item(Item&&) {", "Item(Item&&) noexcept {", at="type", rate=20), Expect("grow.cpp", GROW), Mark(9, at="type"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("raii",
          "點樣做到呢啲保證？[[raii]]靠 RAII：資源交俾物件管，[[unwind]]exception 飛出去嘅時候，解構子自動清理，[[basic]]至少就有 basic 保證，唔會漏。",
          BulletCard("RAII 令保證成立", [("資源交俾物件：vector、unique_ptr", "raii"), ("出錯：stack unwinding 自動解構", "unwind"),
                                        ("結果：至少 basic，唔會漏", "basic")])),
    Scene("recap",
          "總結：[[r1]]三種保證：basic、strong、no-throw；[[r2]]noexcept 係承諾，破咗就 terminate；[[r3]]搬移建構子加 noexcept，vector 先會用佢；[[r4]]RAII 係所有保證嘅基礎。",
          BulletCard("今集重點", [("basic / strong / no-throw", "r1"), ("noexcept：破咗就 terminate", "r2"), ("搬移加 noexcept", "r3"), ("RAII", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫兩個 struct，一個搬移有 noexcept，一個冇，用 is_nothrow_move_constructible_v 印出分別。[[next]]下一集：assert 同 static_assert。多謝收睇，下次見！",
          EndCard("struct Safe（Safe(Safe&&) noexcept）同 Risky（冇 noexcept）：印 std::is_nothrow_move_constructible_v 兩個，應該係 1 0。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
