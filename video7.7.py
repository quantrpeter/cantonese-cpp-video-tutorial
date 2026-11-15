#!/usr/bin/env python3
"""Video 87 (syllabus 7.7): 小項目：自己寫 MiniVector

Part 7 together: a template MiniVector<T> owning a new[] array (RAII destructor), push_back that
doubles the capacity (the real run prints 1/1 2/2 3/4 4/4 5/8), then the rule of five: copy
constructor, move constructor, and one by-value operator= that swaps. The real run prints
99 10 0 (b is a real copy, a was moved from) and "there 2" for MiniVector<std::string>; built
with -fsanitize=address it really prints the same and reports nothing.
Run `python3 video87.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 87
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "07-07"
FINAL = (CODE / "vec.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()


def cut(a, b):
    return a + FINAL.split(a, 1)[1].split(b, 1)[0]


HEAD = FINAL.split("template <typename T>")[0]
FIVE = cut("    MiniVector(const MiniVector& other) {", "    ~MiniVector() {")
PUSH = cut("    void push_back", "    T& operator[]")
GROW = cut("    void grow()", "    T* data_ = nullptr;")
CLASS = cut("template <typename T>", "int main")
MAIN = "int main" + FINAL.split("int main")[1]
REST = MAIN.split("    std::cout << '\\n';\n", 1)[1]
MAIN1 = MAIN.replace(REST, "}\n")
CORE = CLASS.replace(FIVE, "").replace(PUSH, "").replace(GROW, "")
S1 = HEAD + CORE + "int main() {\n}\n"
S2 = HEAD + CLASS.replace(FIVE, "") + MAIN1
assert HEAD + CLASS + MAIN == FINAL
CC = "g++ -std=c++20 -Wall -Wextra vec.cpp -o vec"
ASAN = "g++ -fsanitize=address vec.cpp -o vec"
OUT2 = "1/1 2/2 3/4 4/4 5/8 \n99 10 0\nthere 2\n"

(c1, r1, clr, c2, r2, c3, r3, cch, rch) = cpp.session({"vec.cpp": S2}, [
    CC, "./vec", "clear", Write("vec.cpp", FINAL), CC, "./vec", ASAN, "./vec",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "1/1 2/2 3/4 4/4 5/8 \n" and r2.output == OUT2 and r3.output == OUT2, (r1.output, r2.output, r3.output)
assert c1.code == c2.code == c3.code == r3.code == cch.code == 0 and rch.output == "2 2\n"

SAY = {"MiniVector": "Mini Vector", "MiniVector<T>": "Mini Vector T", "MiniVector<int>": "Mini Vector int",
       "MiniVector<std::string>": "Mini Vector string", "push_back": "push back", "pop_back": "pop back", "back()": "back",
       "capacity": "capacity", "size_": "size 底線", "cap_": "cap 底線", "data_": "data 底線", "grow": "grow", "std::swap": "S T D swap",
       "std::move": "S T D move", "operator=": "operator 等號", "noexcept": "no except", "delete[]": "delete 中括號", "RAII": "R A I I",
       "rule of five": "rule of five", "AddressSanitizer": "Address Sanitizer", "-fsanitize=address": "f sanitize address", "nullptr": "null pointer"}

s = Stage({"vec.cpp": HEAD + "int main() {\n}\n"}, title="小項目：MiniVector", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第七部分最後一集，自己寫一個簡單版嘅 vector：MiniVector。會用晒模板、RAII、複製同搬移。寫完你就會明白，std::vector 入面大概做緊乜。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "template · RAII · rule of five")),
    Scene("plan",
          "計劃：[[b1]]用 new 開一排 T，記住 size 同 capacity；[[b2]]push_back 滿咗就加倍；[[b3]]rule of five：解構、複製、搬移；"
          "[[b4]]最後用 address sanitizer 檢查。",
          BulletCard("計劃", [("data_、size_、cap_", "b1"), ("push_back：滿咗就加倍", "b2"), ("rule of five", "b3"),
                            ("-fsanitize=address 檢查", "b4")])),
    Scene("core",
          "[[type]]MiniVector 係一個類別模板。[[mem]]三個成員：指住一排 T 嘅指標，用咗幾多格 size，同埋總共有幾多格 capacity，一開始全部係零。"
          "[[dtor]]解構子 delete 中括號：RAII，物件消失就還記憶體。",
          s.scene(Open("vec.cpp", mode="instant"), Type("vec.cpp", CORE, before="int main", at="type", rate=90),
                  Mark((23, 25), at="mem"), Mark((9, 11), at="dtor"))),
    Scene("push",
          "[[push]]push_back：如果 size 等於 capacity，即係滿咗，就叫 grow。[[grow]]grow 開一排兩倍大嘅新記憶體，[[mv]]用 std::move 將舊嘅搬過去，"
          "[[swap]]delete 舊嗰排，再指住新嗰排。",
          s.scene(Mark(None), Type("vec.cpp", PUSH, before="    T& operator[]", at="push", rate=90),
                  Type("vec.cpp", GROW, before="    T* data_ = nullptr;", at="grow", rate=110), Mark((31, 32), at="grow"),
                  Mark((33, 35), at="mv"), Mark((36, 38), at="swap"))),
    Scene("run1",
          "[[main]]main 逐個 push 五個數，每次印 size 斜線 capacity。[[cc]]編譯運行：[[o]]一一、二二、三四、四四、五八。容量一、二、四、八咁加倍。",
          s.scene(Mark(None), Replace("vec.cpp", "int main() {\n}", MAIN1.rstrip("\n"), at="main", rate=70), Expect("vec.cpp", S2),
                  Run(c1, at="cc"), Run(r1))),
    Scene("double",
          "點解要加倍，唔係每次加一格？[[one]]每次加一格，每個 push 都要搬晒所有舊嘢，好慢。[[two]]加倍嘅話，搬嘅次數好少：push 一千次，只係搬十次左右。",
          TableCard("每次加幾多？", ["方法", "push 1000 次要搬幾多次"], [
              (["每次 +1", "1000 次，越嚟越慢"], "one", RED),
              (["每次 ×2", "大約 10 次"], "two", GREEN),
          ], widths=[1, 1.6], code_cols=(), size=42)),
    Scene("five",
          "而家 MiniVector 自己管記憶體，所以要寫齊 rule of five。[[type]]複製建構子：逐個 push_back，有自己一排。[[mv]]搬移建構子：攞走指標，再將對方清空。"
          "[[as]]等號：參數係傳值，即係已經複製或者搬移咗一份，再同自己交換。",
          s.scene(Run(clr, at="type"), Type("vec.cpp", FIVE, before="    ~MiniVector() {", at="type", rate=120),
                  Mark((9, 13), at="type"), Mark((14, 20), at="mv"), Mark((21, 26), at="as"))),
    Scene("swap",
          "[[call]]more 等於 words 嗰陣：[[copy]]other 先由 words 複製出嚟；[[sw]]然後 more 同 other 交換三個成員；[[old]]函數完咗，other 帶住 more 舊嘅嘢消失，"
          "解構子幫你還記憶體。",
          TableCard("more = words 發生咩事？", ["步驟", "結果"], [
              (["① 參數 other", "複製 words 一份"], "copy"),
              (["② std::swap ×3", "more 攞到新嘅；other 攞走舊嘅"], "sw"),
              (["③ other 消失", "~MiniVector() 還舊嘅記憶體"], "old", GREEN),
          ], widths=[1, 1.8], code_cols=(), size=38)),
    Scene("run2",
          "[[type]]main 再試：b 係 a 嘅副本，改 b 第一格；c 由 a 搬過去；仲有一個裝 string 嘅 MiniVector，用等號複製。"
          "[[cc]]編譯運行：[[o]]九十九、十、零：b 係真正嘅副本，a 被搬空咗；there，兩個。",
          s.scene(Mark(None), Type("vec.cpp", REST[:-2], before="}", last=True, at="type", rate=80),
                  Expect("vec.cpp", FINAL), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("asan",
          "[[cc]]最後用 address sanitizer 再編譯運行：[[o]]結果一樣，冇任何報告：冇 double free，冇漏記憶體。",
          s.scene(Run(c3, at="cc"), Run(r3), Note("ASan：乜報告都冇", at="o", where="editor"))),
    Scene("recap",
          "總結：[[r1]]模板令 MiniVector 裝乜都得；[[r2]]解構子還記憶體，就係 RAII；[[r3]]滿咗就加倍，搬嘅時候用 std::move；"
          "[[r4]]自己管資源，就寫齊 rule of five。第七部分完成！",
          BulletCard("今集重點", [("template：MiniVector<T>", "r1"), ("RAII：~MiniVector()", "r2"), ("capacity ×2 + std::move", "r3"),
                                ("rule of five", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]幫 MiniVector 加 pop_back，同埋 back，攞最後一個。[[next]]下一集開始第八部分：標準函式庫。多謝收睇，下次見！",
          EndCard("加 void pop_back()（size_ 減一）同 T& back()（最後一個）。push 1、2、3，pop 一次，back() 應該係 2。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)
