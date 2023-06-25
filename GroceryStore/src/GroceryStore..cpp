//
// Created by 陈焕新 on 2023-06-15.
//


#include "../include/GroceryStore.h"

using namespace std;
using namespace _GroceryStore_;

#define TABLE_SPACE <<"     "<<

void GroceryStore::registerCommodity(string name, double price) {
        if (inventory.find(name) == inventory.end()) { // 如果该商品不存在
            inventory[name] = Commodity(price, 0);
            cout << "商品 " << name << " 已注册，价格为 " << price << endl;
        } else {
            cout << "商品 " << name << " 已存在，无法注册！" << endl;
        }
    }

    // 查询指定商品价格及余量
    void GroceryStore::checkCommodity(string name) {
        if (inventory.find(name) != inventory.end()) { // 如果该商品存在
            cout << "商品 " << name << " 的价格为 " << inventory[name].price << "，余量为 " << inventory[name].stock
                 << endl;
        } else {
            cout << "商品 " << name << " 不存在！" << endl;
        }
    }

    // 上架商品
    void GroceryStore::addCommodity(string name, int stock) {
        if (inventory.find(name) != inventory.end()) { // 如果该商品存在
            inventory[name].stock += stock;
            cout << "商品 " << name << " 已上架，余量为 " << inventory[name].stock << endl;
        } else {
            cout << "商品 " << name << " 不存在！" << endl;
        }
    }

    // 销售商品
    void GroceryStore::sellCommodity(string name, int quantity) {
        if (inventory.find(name) != inventory.end()) { // 如果该商品存在
            if (inventory[name].stock >= quantity) { // 如果库存充足
                inventory[name].stock -= quantity;
                salesRecord.insert(make_pair(name, make_pair(inventory[name].price,quantity)));
                cout << "商品 " << name << " 已售出 " << quantity << " 个，售价为 " << inventory[name].price * quantity
                     << " 元，剩余库存为 " << inventory[name].stock << endl;
            } else { // 如果库存不足
                cout << "商品 " << name << " 库存不足！" << endl;
            }
        } else {
            cout << "商品 " << name << " 不存在！" << endl;
        }
    }

    // 更改商品价格
    void GroceryStore::changePrice(string name, double price) {
        if (inventory.find(name) != inventory.end()) { // 如果该商品存在
            inventory[name].price = price;
            cout << "商品 " << name << " 的价格已更改为 " << price << endl;
        } else {
            cout << "商品 " << name << " 不存在！" << endl;
        }
    }

    // 打印现有商品信息列表，并保存到文件中
    void GroceryStore::printInventory(string fileName) {
        ofstream outFile(fileName);
        if (outFile.is_open()) {
            outFile << left << setw(14) << "商品名" << setw(15) << "价格" << setw(10) << "余量" << endl;
            for (auto it = inventory.begin(); it != inventory.end(); ++it) {
                outFile << left << setw(10) << it->first << setw(12) << it->second.price << setw(10) << it->second.stock << endl;
            }
            outFile.close();
            cout << "现有商品信息列表已保存到文件 " << fileName << " 中！" << endl;
        } else {
            cout << "无法打开文件 " << fileName << "！" << endl;
        }
    }


// 打印已销售清单，并保存到文件中
void GroceryStore::printSalesRecord(string fileName) {
    ofstream outFile(fileName);
    if (outFile.is_open()) {
        outFile << left << setw(14) << "商品名" << setw(17) << "销售时价格" << setw(10) << "销售个数" << endl;
        for (auto it = salesRecord.begin(); it != salesRecord.end(); ++it) {
            outFile << left << setw(10) << it->first << setw(12) << it->second.first<< setw(10) << it->second.second << endl;
        }
        outFile.close();
        cout << "已销售清单已保存到文件 " << fileName << " 中！" << endl;
    }
    else {
        cout << "无法打开文件 " << fileName << "！" << endl;
    }
}
