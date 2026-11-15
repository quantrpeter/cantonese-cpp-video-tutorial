#!/usr/bin/env python3
"""Video 7 (syllabus 1.1): 變數：俾資料一個名

A variable as a named box: declare an int, print it, change it with `age = age + 1`, and a real
case-sensitivity error (`Age` vs `age`). Run `python3 video7.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 7
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-01"
FINAL = (CODE / "age.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINE4 = "    int age = 13;\n"
LINE5 = "    std::cout << \"Age: \" << age << '\\n';\n"
LINE7 = "\n    age = age + 1;\n"
LINE8 = "    std::cout << \"Next year: \" << age << '\\n';\n"
SKEL = "#include <iostream>\n\nint main() {\n}\n"
V1 = SKEL.replace("}\n", LINE4 + LINE5 + "}\n")
TYPO = V1.replace("}\n", LINE7 + LINE8.replace("<< age", "<< Age") + "}\n")
assert V1.replace("}\n", LINE7 + LINE8 + "}\n") == FINAL
CC = "g++ -std=c++20 -Wall -Wextra age.cpp -o age"

(c1, r1, c2, c3, r3, cch, rch) = cpp.session({"age.cpp": V1}, [
    CC, "./age",
    Write("age.cpp", TYPO), CC,
    Write("age.cpp", FINAL), CC, "./age",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.strip() == "Age: 13" and r3.output.split() == ["Age:", "13", "Next", "year:", "14"]
assert "'Age' was not declared in this scope; did you mean 'age'?" in cpp.visible(c2.output), c2.output
assert c1.code == c3.code == cch.code == 0 and "Taller: 165" in rch.output

SAY = {"int age = 13": "int age 等如十三", "age = age + 1": "age 等如 age 加一",
       "Age: 13": "Age 十三", "Next year: 14": "Next year 十四"}

s = Stage({"age.cpp": SKEL}, title="第一個變數")

scenes = [
    Scene("intro",
          "歡迎嚟到第一章！由今集開始，我哋學點樣叫程式記住資料。第一樣要識嘅，就係變數。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "variable · int · =")),
    Scene("goal",
          "今集會講：[[b1]]乜嘢係變數；[[b2]]點樣宣告一個 int 變數；[[b3]]點樣改佢個值，再印出嚟。",
          BulletCard("今集學識", [("變數 variable 係乜", "b1"), ("宣告一個 int 變數", "b2"),
                                ("改變數嘅值，再印出嚟", "b3")])),
    Scene("box",
          "變數就好似一個貼咗名嘅盒。[[name]]呢個盒個名叫 age，只可以裝整數，所以佢嘅型別係 int。"
          "[[val]]而家入面裝住十三。[[use]]程式要用嗰陣，叫個名，就攞到入面個值。",
          BoxesCard("變數 = 一個有名嘅盒", [BoxRow([Box("age", [("13", "val")], "int", at="name", w=380)])],
                    box_h=170, size=80, top=CONTENT_TOP + 90,
                    footer=("名：age　型別：int　值：13", "use"))),
    Scene("declare",
          "用返 Hello World 嘅骨架。[[type]]喺 main 入面打：int age = 13，最尾加分號。",
          s.scene(Open("age.cpp", mode="instant"), Type("age.cpp", LINE4, before="}", last=True, at="type"))),
    Scene("anatomy",
          "呢一句叫做宣告變數。[[t]]int 係型別，即係整數；[[n]]age 係變數嘅名；[[eq]]個等號唔係數學嘅等如，"
          "而係將右邊個值放入去；[[v]]十三就係一開始放入去嘅值。[[semi]]最尾記得加分號。",
          AnatomyCard("宣告一個變數", [
              Part("int", "型別：整數", BLUE, "t"),
              Part(" age", "變數名", PURPLE, "n"),
              Part(" =", "放入去", AMBER, "eq"),
              Part(" 13", "初始值", GREEN, "v"),
              Part(";", "完", RED, "semi"),
          ], size=96)),
    Scene("print",
          "[[type]]下一行用 cout 印佢出嚟，留意 age 冇加引號。[[cc]]編譯，[[run]]運行，印出 Age: 13。"
          "[[note]]引號入面係照印嘅文字；冇引號，就會印出變數入面嘅值。",
          s.scene(Type("age.cpp", LINE5, before="}", last=True, at="type"), Expect("age.cpp", V1),
                  Run(c1, at="cc"), Run(r1, at="run"),
                  Note("\"Age: \" 有引號：照印文字\nage 冇引號：印出佢個值", at="note", where="editor"))),
    Scene("assign",
          "變數嘅值可以改。[[type]]空一行，再加一句：age = age + 1。[[read]]呢句要由右邊睇起："
          "先攞 age 而家嘅值，十三加一，得十四，[[put]]再放返入 age 呢個盒度。",
          s.scene(Note(None), Type("age.cpp", LINE7, before="}", last=True, at="type"), Mark(7, at="read"),
                  Note("先計右邊：13 + 1 = 14\n再放入左邊嘅 age", at="put", where="editor"))),
    Scene("box2",
          "用盒嚟睇就好清楚：[[old]]age 本來係十三，[[calc]]右邊計出十四，[[new]]放入去之後，"
          "舊嘅十三就冇咗，而家 age 係十四。",
          BoxesCard("age = age + 1", [BoxRow([Box("age", [("13", None), ("14", "new")], "int", at="old", w=380)])],
                    box_h=170, size=80, top=CONTENT_TOP + 40,
                    notes=[("① 先計右邊：13 + 1 = 14", "calc"), ("② 再放入 age，舊嘅 13 被蓋過", "new")])),
    Scene("typo",
          "[[type]]再印一次。今次故意打錯，將 age 嘅 a 打咗大楷。[[cc]]編譯，[[err]]出錯：佢話 Age 呢個名未宣告過，"
          "[[hint]]仲問你係咪想打細楷嘅 age。因為 C++ 分大細楷，Age 同 age 係兩個唔同嘅名。",
          s.scene(Note(None), Mark(None), Type("age.cpp", LINE8.replace("<< age", "<< Age"), before="}", last=True, at="type"),
                  Expect("age.cpp", TYPO), Run(c2, at="cc"),
                  Note("C++ 分大細楷\nAge 同 age 係兩個名", at="hint", where="editor"))),
    Scene("fix",
          "[[fix]]改返做細楷，[[cc]]再編譯，[[run]]運行。[[out]]第一行係 Age: 13，第二行係 Next year: 14，"
          "因為中間我哋將 age 加咗一。",
          s.scene(Note(None), Replace("age.cpp", "<< Age", "<< age", at="fix"), Expect("age.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3, at="run"))),
    Scene("rules",
          "改名有幾條規則：[[r1]]可以用英文字母、數字同底線，[[r2]]但唔可以用數字開頭，[[r3]]唔可以有空格，"
          "[[r4]]亦唔可以用 int 呢啲 C++ 自己用咗嘅字。[[r5]]最好用有意思嘅英文名，好似 age、score。",
          TableCard("變數名嘅規則", ["名", "得唔得", "點解"], [
              (["age", "得", "英文字母"], "r1", GREEN),
              (["myAge", "得", "大細楷可以混合"], ("r1", 0.4), GREEN),
              (["score_2", "得", "數字同底線放後面"], ("r1", 0.8), GREEN),
              (["2score", "唔得", "數字開頭"], "r2", RED),
              (["my age", "唔得", "有空格"], "r3", RED),
              (["int", "唔得", "C++ 嘅關鍵字"], "r4", RED),
          ], widths=[1, 0.8, 2], note=("用有意思嘅名：age、score、height", "r5"))),
    Scene("recap",
          "總結：[[r1]]變數係一個有名、有型別嘅盒；[[r2]]int age = 13 宣告變數，同時放入初始值；"
          "[[r3]]等號即係放入去，唔係數學嘅等如；[[r4]]C++ 分大細楷。",
          BulletCard("今集重點", [("變數：有名、有型別嘅盒", "r1"), ("int age = 13; 宣告兼放入初始值", "r2"),
                                ("= 係「放入去」，先計右邊", "r3"), ("C++ 分大細楷：Age ≠ age", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個變數 height，裝住你嘅身高，印出嚟；再將佢加五，印出長高之後嘅身高。"
          "[[next]]下一集，我哋會講點樣正確咁初始化變數。多謝收睇，下次見！",
          EndCard("整一個變數 height，裝住你嘅身高，印出嚟；再將佢加 5，印出長高之後嘅身高。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
