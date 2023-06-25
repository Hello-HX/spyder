//
// Created by 陈焕新 on 2023-06-14.
//

#ifndef TRANSLATOR_H
#define TRANSLATOR_H

#include<string>
#include<iostream>
#include<fstream>
#include<map>
#include<queue>
#include<variant>
#include<iterator>
#include<algorithm>
#include "Computer.h"
#include<vector>

namespace _Translator_ {

#define FILE_CERR(name)  \
    do{ \
        if(!file.is_open()) { \
        std::cerr << "Error opening file " << name << std::endl;\
        return;\
      } \
    } while(0);

    using namespace std;

    class Node { //链表
    public:
        std::string data;
        Node* next;
    };

    //翻译器，继承计算类
    class Translator:public Computer{
    public:
        /**
         * 做泛化
         */
        //抽象类型
        //using T_Key = variant<string,int,float>;
        using T_Key = string;
        //using T_Value = variant<int,float>;
        using T_Value = string;
        using T_dict = map<T_Key,T_Value>;
        using T_list = class Node*;

        //折构函数
        Translator(string Dict_name="E:\\dict60.txt",
                   string Input_name="E:\\input60.txt",
                   string Out_name="E:\\output60.txt")
            :dict_name(Dict_name),input_name(Input_name),list_head(NULL),list_tail(NULL),out_name(Out_name) {
        }
        //保证内存安全
        ~Translator( ) {
            Clear();
        }
        //解析字典对象
        void parser_dict( );

        //解析符合串
        void parser_ans( );//解析字符串
        bool skip_char(int pos);//跳过关键token

        //打印对象
        void print_dict( );
        void print_text( );

        //链表操作
        void Insert(string Data); //插入
        void Delete(Node* node); //删除
        void Print(); //打印
        vector<double> readData(); //加载
        void Result(); //排序
        void Clear(); //清空所有

        //字符串与数字转换
        int Eval_to_int(const string& Data);
        string Eval_to_string(const int Data);

        //解析调用
        void ParseAndReplace( ); //程序解析调用

        //排序算法
        void quicksort(vector<double>& vec, int left, int right); //排序算法

        //设置解析路径和输出地址等
        void set_outfile(string name) { out_name = name;}
        void set_dictfile(string name) { Clear(); list_head = NULL; list_tail = NULL; dict_name = name;}
        void set_inputfile(string name) { Clear(); list_head = NULL; list_tail = NULL; input_name = name;}

    private:
        string input_name;
        string dict_name;
        string out_name;
        T_dict dict_obj;
        T_list list_head;
        T_list list_tail;
        string text;
        string text_ans;
    };


}


#endif //TRANSLATOR_H
