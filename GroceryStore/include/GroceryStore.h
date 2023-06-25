//
// Created by 陈焕新 on 2023-06-15.
//

#ifndef GROCERYSTORE_GROCERYSTORE_H
#define GROCERYSTORE_GROCERYSTORE_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <iomanip>
#include <queue>

namespace _GroceryStore_ {

    using namespace  std;
    using PDI = pair<double,int>;

    // 商品类
    class Commodity {
    public:
        double price; // 价格
        int stock; // 库存

        // 构造函数
        Commodity(double p = 0.0, int s = 0) : price(p), stock(s) {}
    };

    // 杂货店类
    class GroceryStore {
    private:
        map <string, Commodity> inventory; // 商品库存
        multimap<string, pair<double,int>> salesRecord; // 销售记录
    public:
        // 注册商品及价格
        void registerCommodity(string name, double price);
        // 查询指定商品价格及余量
        void checkCommodity(string name);
        // 上架商品
        void addCommodity(string name, int stock);
        // 销售商品
        void sellCommodity(string name, int quantity);
        // 更改商品价格
        void changePrice(string name, double price);
        //打印现有商品信息列表，并保存到文件中
        void printInventory(string filename);
        //打印已销售清单,并保存到文件
        void printSalesRecord(string fileName);
    };

    class SystemManager: public GroceryStore{
    private:
        string line_command;
    public:
        void parser();
        void memu();
        void start();
    };
}
#endif //GROCERYSTORE_GROCERYSTORE_H
