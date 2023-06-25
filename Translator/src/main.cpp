#include "../include/Translator.h"
using namespace _Translator_;

#define BEGIN(order,str) std::cout << "现在进行第 " \
                                   << order << " 个测试，测试功能为: " \
                                   << str << std::endl;
#define END  std::cout << "测试完毕，一切正常"  <<std::endl; \
              system("pause");

void Test( ) {
    system("chcp 65001");
    std::cout << "--- 简单的机器翻译器---" <<std::endl;
    std::cout << "Created by 陈焕新 on 2023-06-14." << std::endl;

    Translator tra("D:\\Translation\\src\\dict.txt","D:\\Translation\\src\\input.txt","D:\\Translation\\src\\out.txt");

    //Translator tra;

    BEGIN("一","映射字典并打印出字典")
    tra.parser_dict();
    tra.print_dict();
    END

    BEGIN("二","根据字典转换到链表，并打印出原始和转换数据")
    tra.parser_ans();
    tra.print_text();
    END


    BEGIN("三","打印链表符号串")
    tra.Print();
    END

    BEGIN("四","解析并调用程序替代原始符号串")
    tra.ParseAndReplace();
    END

    BEGIN("五","打印解析情况")
    tra.Print();
    END

    BEGIN("六","对结果排序并输出")
    tra.Result();
    END


    BEGIN("七","自己调用，包括切换解析文件等，详细看Translator.声明的API")
    END

}

int main() {
    Test();
    return 0;
}
