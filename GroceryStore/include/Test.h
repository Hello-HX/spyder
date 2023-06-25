//
// Created by 陈焕新 on 2023-06-15.
//

#ifndef GROCERYSTORE_TEST_H
#define GROCERYSTORE_TEST_H
#include "GroceryStore.h"
#include<iostream>
using namespace _GroceryStore_;

#define FINISH(name) do { \
    cout << "Test " << name << " Finish" << endl; \
    system("pause"); \
} while(0);

void test_register(SystemManager& sys) {
    puts("Now test the register");
    sys.registerCommodity("one",100);
    sys.registerCommodity("two",100);
    sys.registerCommodity("three",100);
    sys.registerCommodity("four",100);
    sys.registerCommodity("five",100);
    FINISH("test_register")
}

void test_add(SystemManager& sys) {
    puts("Now test the add");
    sys.addCommodity("one",100);
    sys.addCommodity("two",100);
    sys.addCommodity("three",100);
    sys.addCommodity("four",100);
    sys.addCommodity("five",100);
    FINISH("test_add")
}

void test_check(SystemManager& sys) {
    puts("Now test the sell");
    sys.checkCommodity("one");
    sys.checkCommodity("two");
    sys.checkCommodity("three");
    sys.checkCommodity("four");
    sys.checkCommodity("five");
    FINISH("test_check")
}

void test_sell(SystemManager& sys) {
    puts("Now test the sell");
    sys.sellCommodity("one",50);
    sys.sellCommodity("two",50);
    sys.sellCommodity("three",50);
    sys.sellCommodity("four",50);
    sys.sellCommodity("five",50);
    FINISH("test_sell")
}

void test_change(SystemManager& sys) {
    puts("Now test the change");
    sys.changePrice("one",200);
    sys.changePrice("two",200);
    sys.changePrice("three",200);
    sys.changePrice("four",200);
    sys.changePrice("five",200);
    FINISH("test_change")
}

void test_printInventory(SystemManager& sys) {
    puts("Now test the printInventory");
    sys.printInventory("../src/Inventory.txt");
    FINISH("test_printInventory")
}

void test_printSalesRecord(SystemManager& sys) {
    puts("Now test the printSalesRecord");
    sys.printSalesRecord("../src/SalesRecord.txt");
    FINISH("test_printSalesRecord")
}

void test_start(SystemManager& sys) {
    puts("Now test the start");
    sys.start();
    FINISH("test_start")
}

void test_error(SystemManager& sys) {
    puts("Now test the error");
    sys.registerCommodity("one",100);
    sys.checkCommodity("six");
    sys.addCommodity("six",100);
    sys.sellCommodity("six",100);
    sys.changePrice("six",100);
    sys.printInventory("");
    sys.printSalesRecord("");
    FINISH("test_error")
}

void test( ) {
    system("chcp 65001");
    SystemManager sys;
    test_register(sys);
    test_add(sys);
    test_check(sys);
    test_sell(sys);
    test_change(sys);
    test_printInventory(sys);
    test_printSalesRecord(sys);
    test_error(sys);
    test_start(sys);
    FINISH("ALL")
}
#endif //GROCERYSTORE_TEST_H
