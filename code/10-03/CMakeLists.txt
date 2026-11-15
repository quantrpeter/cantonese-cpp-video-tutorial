cmake_minimum_required(VERSION 3.20)
project(Calculator CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(calc main.cpp calc.cpp)
target_compile_options(calc PRIVATE -Wall -Wextra)
