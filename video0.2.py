#!/usr/bin/env python3
"""Video 2 (syllabus 0.2): 安裝開發環境

The two tools (g++ and VS Code), install steps for Windows (MSYS2), Mac (Command Line Tools) and
Linux (apt / dnf), checking with `g++ --version` (a real run), what to do when g++ is not found,
and online compilers as a fallback. Run `python3 video0.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)

N = 2
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

(version,) = cpp.session({}, ["g++ --version"], refresh=opts.fresh_runs)
assert version.code == 0 and "g++" in version.output, version.output

check = Stage(title="檢查：g++ 裝好未？", split=0)

scenes = [
    Scene("intro",
          "大家好！歡迎返嚟 C++ 全攻略。今集我哋會喺你部電腦度，裝好寫 C++ 要用嘅工具。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "Windows · Mac · Linux")),
    Scene("goal",
          "今集會講：[[b1]]編譯器同編輯器分別做乜；[[b2]]Windows、Mac 同 Linux 點樣安裝；[[b3]]點樣檢查裝好未；"
          "[[b4]]仲有，如果部電腦裝唔到，可以點算。",
          BulletCard("今集學識", [("編譯器同編輯器分別做乜", "b1"), ("Windows、Mac、Linux 點樣安裝", "b2"),
                                ("點樣檢查裝好未", "b3"), ("裝唔到嘅話點算", "b4")])),
    Scene("tools",
          "寫 C++ 要兩樣工具。[[compiler]]第一樣係編譯器，我哋用 g++，佢負責將 C++ 翻譯做機器碼。"
          "[[editor]]第二樣係編輯器，我哋用 VS Code，用嚟寫程式，入面仲有個 Terminal 可以打指令。[[free]]兩樣都係免費嘅。",
          TileCard("兩樣工具", [
              Tile("🧰", "編譯器：g++", "將 C++ 翻譯做機器碼", "compiler", PURPLE),
              Tile("📝", "編輯器：VS Code", "寫程式、睇錯誤、開 Terminal 打指令", "editor", BLUE),
          ], cols=2, height=330, footer=("兩樣都係免費", "free"))),
    Scene("pick",
          "跟住，揀返你部電腦用緊嘅系統：[[win]]Windows，[[mac]]Mac，[[linux]]定係 Linux？[[skip]]你只需要睇你嗰一段，其他可以跳過。",
          TileCard("你用緊邊個系統？", [
              Tile("🪟", "Windows", "MSYS2 + g++ + VS Code", "win", BLUE),
              Tile("🍎", "Mac", "Command Line Tools + VS Code", "mac", PURPLE),
              Tile("🐧", "Linux", "apt / dnf + VS Code", "linux", TEAL),
          ], height=330, footer=("只需要睇你嗰一段", "skip"))),
    Scene("win1",
          "Windows 用家，我哋用 MSYS2 嚟裝 g++。[[s1]]第一步，去 MSYS2 嘅官方網站，下載安裝程式，一路撳 Next 就得。"
          "[[s2]]第二步，打開 MSYS2 UCRT64 呢個終端機，輸入呢句 pacman 指令，佢問你嘅時候撳 Y。"
          "[[s3]]第三步，喺 Windows 嘅環境變數度，將呢個資料夾加入 Path，咁樣喺邊度都搵到 g++。",
          StepsCard("Windows：安裝 g++", [
              Step("去 MSYS2 官網下載安裝程式，一路撳 Next", "msys2.org", "s1"),
              Step("打開「MSYS2 UCRT64」，輸入呢句，問你嘅時候撳 Y", "pacman -S mingw-w64-ucrt-x86_64-gcc", "s2"),
              Step("喺「環境變數」將呢個資料夾加入 Path", r"C:\msys64\ucrt64\bin", "s3"),
          ], icon="🪟")),
    Scene("win2",
          "[[s4]]跟住裝 VS Code，喺佢嘅官方網站下載，安裝就得。[[s5]]打開 VS Code，喺 Extensions 搜尋 C/C++，裝 Microsoft 出嗰個。"
          "[[s6]]最後，開一個新嘅 Terminal，打 g++ --version，見到版本號碼，就代表裝好喇。",
          StepsCard("Windows：安裝 VS Code", [
              Step("去 VS Code 官網下載並安裝", "code.visualstudio.com", "s4"),
              Step("喺 Extensions 搜尋「C/C++」，裝 Microsoft 出嗰個", "", "s5"),
              Step("開一個新嘅 Terminal（例如 PowerShell），輸入：", "g++ --version", "s6"),
          ], icon="🪟", start=4)),
    Scene("mac",
          "Mac 用家最簡單。[[s1]]打開終端機，輸入 xcode-select --install。[[s2]]彈出視窗之後撳安裝，等佢裝完。"
          "[[s3]]跟住打 g++ --version 檢查。你會見到 Apple clang，即係 Apple 版嘅編譯器，跟呢個課程大部分內容都冇問題，"
          "有分別嘅地方我哋會講。[[s4]]VS Code 同 C/C++ extension，就同 Windows 一樣咁裝。",
          StepsCard("Mac：安裝", [
              Step("打開「終端機」（Terminal），輸入：", "xcode-select --install", "s1"),
              Step("彈出視窗之後撳「安裝」，等佢裝完", "", "s2"),
              Step("檢查：見到 Apple clang 就得", "g++ --version", "s3"),
              Step("VS Code 同 C/C++ extension：同 Windows 一樣", "", "s4"),
          ], icon="🍎", color=PURPLE)),
    Scene("linux",
          "Linux 用家，一句指令就搞掂。[[s1]]Ubuntu 或者 Debian，打 sudo apt install g++。[[s2]]Fedora 就打 sudo dnf install gcc-c++。"
          "[[s3]]裝完一樣打 g++ --version 檢查。[[s4]]VS Code 都有 Linux 版。",
          StepsCard("Linux：安裝", [
              Step("Ubuntu／Debian：", "sudo apt install g++", "s1"),
              Step("Fedora：", "sudo dnf install gcc-c++", "s2"),
              Step("檢查：", "g++ --version", "s3"),
              Step("VS Code 都有 Linux 版，一樣喺官網下載", "", "s4"),
          ], icon="🐧", color=TEAL)),
    Scene("check",
          "唔理你用邊個系統，檢查方法都一樣：[[run]]打 g++ --version。[[out]]見到好似咁嘅版本資料，就代表編譯器裝好喇。"
          "你見到嘅號碼可能唔同，唔緊要。",
          check.scene(Run(version, at="run"), Note("見到版本號碼 ＝ 裝好！\n號碼唔同都唔緊要", at="out"))),
    Scene("notfound",
          "如果打 g++ 嘅時候，佢話搵唔到呢個指令，通常係以下原因：[[r1]]裝完之後，冇關咗個 Terminal 再開過；"
          "[[r2]]Windows 嘅 Path 冇加啱；[[r3]]或者 Mac 嘅工具未裝完。逐樣檢查一次就得。",
          BulletCard("搵唔到 g++？", [("裝完要關咗 Terminal，再開過一個新嘅", "r1"),
                                    ("Windows：檢查 Path 有冇加啱資料夾", "r2"),
                                    ("Mac：再打一次 xcode-select --install", "r3")], color=AMBER)),
    Scene("online",
          "如果用緊學校電腦或者平板，裝唔到嘢，[[ce]]可以先用網上編譯器，例如 Compiler Explorer，喺瀏覽器寫、喺瀏覽器行。"
          "[[limit]]不過網上版有限制，例如讀寫檔案就唔方便，[[advice]]所以長遠都係建議裝喺自己部電腦。",
          TileCard("裝唔到？用網上編譯器", [
              Tile("🌐", "Compiler Explorer", "godbolt.org：揀 C++，寫完即刻行", "ce", BLUE),
              Tile("🏫", "學校電腦、平板", "開瀏覽器就用得", ("ce", 0.8), TEAL),
              Tile("🚧", "有限制", "讀寫檔案、大項目都唔方便", "limit", AMBER),
          ], height=330, footer=("長遠：裝喺自己部電腦", "advice"))),
    Scene("recap",
          "總結一下：[[r1]]編譯器 g++ 負責翻譯，編輯器 VS Code 用嚟寫程式；[[r2]]Windows 用 MSYS2，Mac 用 xcode-select，"
          "Linux 用 apt；[[r3]]打 g++ --version 見到版本號碼，就代表裝好。",
          BulletCard("今集重點", [("g++ 負責翻譯，VS Code 用嚟寫程式", "r1"),
                                ("Windows：MSYS2　Mac：xcode-select　Linux：apt", "r2"),
                                ("g++ --version 見到版本號碼 ＝ 裝好", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]喺你部電腦裝好 g++ 同 VS Code，打 g++ --version，見到版本號碼就成功。"
          "[[next]]下一集，我哋終於會寫第一個 C++ 程式：Hello World！多謝收睇，下次見！",
          EndCard("喺你部電腦裝好 g++ 同 VS Code，打 g++ --version，見到版本號碼就成功！",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts)
