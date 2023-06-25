cmake_minimum_required(VERSION 3.24)
project(translation)

set(CMAKE_CXX_STANDARD 17)

add_executable(translation src/main.cpp src/Translator.cpp include/Translator.h src/List.cpp include/Computer.h)
