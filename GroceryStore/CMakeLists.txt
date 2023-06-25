cmake_minimum_required(VERSION 3.24)
project(GroceryStore)

set(CMAKE_CXX_STANDARD 17)

add_executable(GroceryStore src/main.cpp include/GroceryStore.h src/GroceryStore..cpp src/SystemManager.cpp include/Test.h)
