//
// Created by 陈焕新 on 2023-06-14.
//

#include "../include/Translator.h"
#include<sstream>
#include<stack>
using namespace _Translator_;


void Translator::parser_dict( ) {
    std::ifstream file(this->dict_name);

    FILE_CERR(this->dict_name)

    std::string line;
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') {
            continue; // ignore empty lines and comments
        }

        size_t pos = 0;
        std::string key, value;
        try {
            key = line.substr(0, line.find(' '));
            value = line.substr(line.find(' ') + 1);
            dict_obj[key] = value; // convert value to integer
        } catch (const std::exception& e) {
            std::cerr << "Error parsing line: " << line << std::endl;
        }
    }
    file.close();
}


void removeExtraSpaces(string& text) {
    string result;
    bool hasSpace = false;
    for(char c : text) {
        if(c == ' ') {
            if(hasSpace) {
                continue;
            } else {
                result.push_back(' ');
                hasSpace = true;
            }
        } else {
            result.push_back(c);
            hasSpace = false;
        }
    }
    text = result;
    result.clear();
    bool hasbound = false;
    for(char c : text) {
        if(c == '(' || c == '{' || c == '<' || c == '[') {
            hasbound = true;
        }
        else if(c == ')' || c == '}' || c == '>' || c == ']') {
            hasbound = false;
        }

        if(hasbound) {
            if(c==' ')continue;
            else result.push_back(c);
        }
        else {
            result.push_back(c);
        }
    }
    text = result;
}


void Translator::parser_ans() {
    std::ifstream file(this->input_name);
    FILE_CERR(this->input_name);
    this->text = std::string((std::istreambuf_iterator<char>(file)),
                             std::istreambuf_iterator<char>());
    removeExtraSpaces(this->text);
    file.close();

    string tmp="";
    string tmp2="";
    string text_tmp="";

    for(int pos = 0; pos < text.size(); pos++) {
        if(skip_char(pos)) {
            if(!tmp.empty() ) {
                if(dict_obj.count(tmp))tmp = dict_obj[tmp];
                tmp2+=tmp;
                tmp2+=text[pos];
                tmp ="";
            }
            else {
                tmp2+=text[pos];
            }

            if(text[pos] == ' ') {
                Insert(tmp2);
                text_tmp+=tmp2;
                tmp2="";
                tmp="";
            }
        }
        else {
            tmp+=text[pos];
        }

        if(pos == text.size()-1) {
            text_tmp+=tmp2;
            Insert(tmp2);
        }
    }
    this->text_ans = text_tmp;
}

void Translator::print_text( ) {
    cout << std::endl;
    cout <<"This is the text : " << std::endl;
    cout << this->text;
    cout << std::endl;
    cout <<"This is the text_ans: " << std::endl;
    cout << this->text_ans;
    cout << std::endl;
    cout << std::endl;
}

void Translator::print_dict( ) {
    for(auto it = dict_obj.begin(); it != dict_obj.end();it++) {
        cout <<it->first <<" " << it->second << endl;
    }
}


bool Translator::skip_char(int pos) {
    if(text[pos]=='(' || text[pos] == ')'||
       text[pos] =='{' || text[pos] == '}' ||
       text[pos] == '/' || text[pos] == ',' ||
       text[pos] == '<' || text[pos] == '>' ||
       text[pos] == '[' || text[pos] == ']' || text[pos] == ' ')
        return true;
    else return false;
}



int Translator::Eval_to_int(const string &Data) {
    return stoi(Data);
}

string Translator::Eval_to_string(const int Data) {
    return to_string(Data);
}

#define Try(name) do{ \
    if(expression.find(name) == string::npos) { \
        puts("Find invalid message");                       \
        cout << current->data<< std::endl;      \
        Node* tmp = current->next;              \
        Delete(current);                        \
        current = tmp;\
        goto Process; } \
    }while(0);

#define onlynum(current)  do { \
    if(expression.find('}') != string::npos|| expression.find(')') != string::npos|| \
       expression.find('>') != string::npos || expression.find(',') != string::npos|| \
       expression.find('/') != string::npos ) {                       \
       puts("Find invalid message");   \
       cout << current->data << std::endl;                                           \
       Node* tmp = current->next;                                                    \
       Delete(current);        \
       current=tmp;                        \
       goto Process;}                   \
       }while(0);

// 解析符号条件并调用相应的函数进行计算
void Translator::ParseAndReplace()
{
    Node* current = list_head;
    //Process:
    while(current != nullptr)
    {
        string& expression = current->data;
        if(!expression.empty())
        {
            char symbol = expression[0];
            string content = expression;
            //cout << content << std::endl;

            if(symbol == '[') {
                //Try(']')
                replace(content.begin(), content.end(), ',', ' ');
                replace(content.begin(), content.end(), '[', ' ');
                replace(content.begin(), content.end(), ']', ' ');
                stringstream ss(content);
                int a, b;
                ss >> a >> b;
                int lcmResult = LCM(a, b);
                current->data = " " + to_string(lcmResult) + " ";
            }
            else if(symbol == '{') {
                //Try('}')
                replace(content.begin(), content.end(), ',', ' ');
                replace(content.begin(), content.end(), '{', ' ');
                replace(content.begin(), content.end(), '}', ' ');
                stringstream ss1(content);
                int c, d;
                ss1 >> c >> d;
                int gcdResult = GCD(c, d);
                current->data = " " + to_string(gcdResult)+" ";
            }
            else if (symbol == '<') {
                //Try('>')
                replace(content.begin(), content.end(), ',', ' ');
                replace(content.begin(), content.end(), '>', ' ');
                replace(content.begin(), content.end(), '<', ' ');
                stringstream ss2(content);
                int e, f;
                ss2 >> e >> f;
                //double weeklySalaryResult = CalculateSalary(e, f);
                int weeklySalaryResult = CalculateSalary(e, f);
                current->data = " " + to_string(weeklySalaryResult) + " ";
            }
            else if (symbol == '(') {
                //Try(')')
                //cerr <<content;
                replace(content.begin(), content.end(), ',', ' ');
                replace(content.begin(), content.end(), '/', ' ');
                size_t pos1 = content.find('(');
                size_t pos2 = content.find(')');
                content = content.substr(pos1+1,pos2-1);
                //cerr <<content;
                stringstream ss3(content);
                int size = 1;
                for (int i = 0; i < content.size(); i++) {
                    if(content[i] == ' ') size ++ ;
                }
                //cout << size << ' ' << endl;
                if (size == 1) {
                    int n = stoi(content);
                    //cout << n;
                    long  long  factorialResult = Factorial(n);
                    current->data = " " + to_string(factorialResult) + " ";
                } else if (size == 2) {
                    int n, m;
                    ss3 >> n >> m;
                    long long combinationResult = Combination(n, m);
                    current->data = " " + to_string(combinationResult) + " ";
                } else if (size == 3) {
                    int year, month, day;
                    ss3 >> year >> month >> day;
                    int weekday = getWeekday(year, month, day);
                    current->data = " " + to_string(weekday) + " ";
                }
            }
            else {
                //onlynum(current)
                current->data = " " + current->data;
            }
        }
        current = current->next;
    }
}


// 快速排序算法实现
void Translator::quicksort(vector<double>& vec, int left, int right) {
    if(left < right) {
        int pivot = vec[left];
        int i = left, j = right + 1;
        while(1) {
            do ++i; while(vec[i] < pivot && i <= right);
            do --j; while(vec[j] > pivot && j >= left + 1);
            if(i >= j) break;
            swap(vec[i], vec[j]);
        }
        swap(vec[left], vec[j]);
        quicksort(vec, left, j - 1);
        quicksort(vec, j + 1, right);
    }
}

