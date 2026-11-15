cmake_minimum_required(VERSION 3.20)
project(Scores CXX)
set(CMAKE_CXX_STANDARD 20)

include(FetchContent)
FetchContent_Declare(json
    URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(json)

add_executable(scores main.cpp)
target_link_libraries(scores PRIVATE nlohmann_json::nlohmann_json)
