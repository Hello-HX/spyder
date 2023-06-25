//
// Created by 陈焕新 on 2023-06-15.
//

#include "../include/GroceryStore.h"

using namespace std;
using namespace _GroceryStore_;


inline void SystemManager::memu() {
    cout << "请输入以下指令进行操作：" << endl;
    cout << "register 商品名 价格：注册商品及价格" << endl;
    cout << "check 商品名：查询指定商品价格及余量" << endl;
    cout << "add 商品名 数量：上架商品" << endl;
    cout << "sell 商品名 数量：销售商品" << endl;
    cout << "change 商品名 价格：更改商品价格" << endl;
    cout << "print have 文件名：打印现有商品信息列表，并保存到文件中" << endl;
    cout << "print sell 文件名：打印已销售清单，并保存到文件中" << endl;
    cout << "exit：退出程序" << endl;
    cout << "请输入:" ;
}


void SystemManager::start() {
    cout << "欢迎来到购物系统！" << endl;
    parser();
}

void SystemManager::parser() {
    string command, name, fileName;
    double price;
    int stock, quantity;
    while (true) {
        memu();
        getline(cin, line_command);
        istringstream iss(line_command);
        iss >> command;

        if (command == "register") { // 注册商品及价格
            iss >> name >> price;
            registerCommodity(name, price);
        }
        else if (command == "check") { // 查询指定商品价格及余量
            iss >> name;
            checkCommodity(name);
        }
        else if (command == "add") { // 上架商品
            iss >> name >> stock;
            addCommodity(name, stock);
        }
        else if (command == "sell") { // 销售商品
            iss >> name >> quantity;
            sellCommodity(name, quantity);
        }
        else if (command == "change") { // 更改商品价格
            iss >> name >> price;
            changePrice(name, price);
        }
        else if (command == "print") { // 打印现有商品信息列表或已销售清单，并保存到文件中
            iss >> command >> fileName;
            if (command == "have") {
                printInventory(fileName);
            }
            else if (command == "sell") {
                printSalesRecord(fileName);
            }
        }
        else if (command == "exit") { // 退出程序
            break;
        }
        else {
            cout << "无效的指令！" << endl;
        }
    }
}