#!/usr/bin/env python3
"""Video 154 (syllabus 13.6): 下一步去邊？

The closing video: no program is built. Cards look back over the 13 parts and point to five
directions to go next: game development (raylib), desktop GUIs (Qt), embedded boards (Arduino,
ESP32), competitive programming (HKOI), and open source; then how to keep learning.
Run `python3 video13.6.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)

N = 154
opts = options(N)
ep = course.episode(N)

scenes = [
    Scene("intro",
          "歡迎返嚟！呢個係 C++ 全攻略嘅最後一集。恭喜你行到呢度！今集唔寫 code，一齊回顧學過乜，再睇吓學完 C++ 可以去邊。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "回顧 · 五個方向 · 繼續學")),
    Scene("review",
          "回顧一下：[[b1]]由變數、迴圈、函數開始；[[b2]]vector、字串、指標同記憶體；[[b3]]物件導向同模板；[[b4]]標準函式庫、錯誤處理、工具；[[b5]]並行、演算法，同埋兩個綜合項目。",
          BulletCard("十三個部分", [("基礎：變數、迴圈、函數", "b1"), ("vector、字串、指標、記憶體", "b2"), ("物件導向、模板", "b3"),
                                 ("STL、錯誤處理、工具", "b4"), ("並行、演算法、綜合項目", "b5")])),
    Scene("games",
          "第一個方向：[[game]]遊戲開發。raylib 係一個好簡單嘅 C 同 C++ 遊戲庫，幾十行就可以開視窗、畫圖、播聲。[[engine]]再大啲，Unreal Engine 都係用 C++。可以試吓將我哋嘅貪食蛇變成有圖像嘅版本。",
          TileCard("方向一：遊戲", [
              Tile("🎮", "raylib", "簡單易上手\n開視窗、畫圖、聲音", "game", BLUE),
              Tile("🕹️", "Unreal Engine", "大型 3D 遊戲\n核心用 C++", "engine", PURPLE),
          ], cols=2, height=360)),
    Scene("gui",
          "第二個方向：[[qt]]桌面應用程式。Qt 係好成熟嘅 C++ 介面庫，Windows、Mac、Linux 都用得，好多專業軟件都係用佢寫。",
          TileCard("方向二：桌面程式", [
              Tile("🖥️", "Qt", "跨平台視窗程式\n按鈕、表格、圖表", "qt", BLUE),
          ], cols=1, height=360)),
    Scene("embedded",
          "第三個方向：[[ard]]嵌入式。Arduino 用嘅語言其實就係 C++，可以控制燈、感應器、摩打；[[esp]]ESP32 仲有 Wi-Fi 同藍牙，可以整智能家居。",
          TileCard("方向三：嵌入式", [
              Tile("🔌", "Arduino", "C++ 控制燈、感應器", "ard", GREEN),
              Tile("📡", "ESP32", "Wi-Fi、藍牙、物聯網", "esp", GREEN),
          ], cols=2, height=360)),
    Scene("contest",
          "第四個方向：[[hkoi]]比賽。香港電腦奧林匹克競賽 HKOI，用嘅就係第十二部分嘅演算法；[[online]]平時可以喺網上判題系統練習，由易到難慢慢做。",
          TileCard("方向四：比賽", [
              Tile("🏆", "HKOI", "香港電腦奧林匹克競賽", "hkoi", AMBER),
              Tile("💻", "網上判題", "每日練一兩題", "online", AMBER),
          ], cols=2, height=360)),
    Scene("open",
          "第五個方向：[[os]]開源。好多大型項目都係 C++ 寫嘅，你可以喺 GitHub 睇佢哋點寫，[[pr]]由改文件、修細 bug 開始參與。睇真正嘅 code，進步最快。",
          TileCard("方向五：開源", [
              Tile("🌍", "讀真正嘅 code", "大型 C++ 項目", "os", BLUE),
              Tile("🔧", "由細開始", "改文件、修細 bug", "pr", BLUE),
          ], cols=2, height=360)),
    Scene("habits",
          "無論揀邊個方向，記住幾個習慣：[[h1]]日日寫少少；[[h2]]開晒警告，用 sanitizer；[[h3]]寫測試；[[h4]]遇到唔明，睇官方文件 cppreference，再自己試一個細例子。",
          BulletCard("繼續學嘅習慣", [("日日寫少少 code", "h1"), ("-Wall -Wextra、sanitizer", "h2"), ("寫測試", "h3"), ("cppreference + 細例子", "h4")])),
    Scene("outro",
          "多謝你睇晒成個 C++ 全攻略！[[ch]]最後一個挑戰：揀一個方向，整一個屬於你自己嘅小項目。[[bye]]祝你寫 code 愉快，我哋下次見！",
          EndCard("揀一個方向，整一個屬於你自己嘅小項目。", "全課程完成，多謝收睇！", challenge_at="ch", next_at="bye")),
]

build(N, scenes, opts)
