//
// Created by 陈焕新 on 2023-06-14.
//

#include"../include/Translator.h"
using namespace _Translator_;

void Translator::Insert(string Data) {
    Node* node = (Node*)new(Node);
    node->data = Data;
    node->next = NULL;
    //cout << node->data << std::endl;
    if(!list_head) {
        list_head = node;
        list_tail = node;
    }
    else {
        list_tail->next = node;
        list_tail = node;
    }
}


void Translator::Delete(Node *node) {
    Node* head = list_head;
    if(node == list_head) {
        list_head = list_head->next;
        delete(node);
    }
    else {
        while(head && head->next != node) {
            head = head->next;
        }
        head->next = node->next;
        delete(node);
    }
}

void Translator::Print() {
    Node* node = list_head;
    while(node) {
        cout << node->data;
        node = node->next;
    }
    cout << std::endl;
}

// 读取data并转换为相应的数据类型，存到vector中
vector<double> Translator::readData( ) {
    vector<double> vec;
    Node* current = list_head;
    while(current != nullptr) {
        string& expression = current->data;
        if(!expression.empty() ) {
            try {
                double value = stod(expression);
                vec.push_back(value);
            } catch (const invalid_argument& e) {

            }
        }
        current = current->next;
    }
    return vec;
}

//最终结果
void Translator::Result() {
    vector<double> vec = readData();
    quicksort(vec,0,vec.size()-1);
    ofstream out(this->out_name);
    for(int i = 0; i < vec.size(); i++) {
        out << vec[i] <<" ";
    }
    out.close();
}

void Translator::Clear( ) {
    Node* tmp = list_head;
    while(list_head) {
        tmp = list_head->next;
        free(list_head);
        list_head = tmp;
    }
}