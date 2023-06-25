//
// Created by 陈焕新 on 2023-06-14.
//

#ifndef TRANSLATION_COMPUTER_H
#define TRANSLATION_COMPUTER_H
namespace _Translator_ {
    class Computer {
    public:
        // 求两个数的最大公约数
        int GCD(int a, int b) {
            while (b != 0) {
                int temp = b;
                b = a % b;
                a = temp;
            }
            return a;
        }

        // 求两个数的最小公倍数
        int LCM(int a, int b) {
            //if (a == 0) return  0;
            return a * b / GCD(a, b);
        }

        // 根据日期计算该天是星期几
        int getWeekday(int year, int month, int day) {
            int monthDays[] = {31,28,31,30,31,30,31,31,30,31,30,31};
            int sum = 0;
            for (int i = 0; i < month - 1; i++) {
                sum += monthDays[i];
            }
            sum += day - 1;
            int weekday = (sum + year - 1 + (year - 1)/4 - (year - 1)/100 + (year - 1)/400) % 7;
            return weekday + 1;
        }

        // 计算阶乘
        long long Factorial(int n) {
            long long result = 1;
            for (int i = 1; i <= n; i++) {
                result *= i;
            }
            return result;
        }

        // 求组合数C(n,m)
        long long Combination(int n, int k) {
            //参数检查
            if (n < 0 || k < 0 || k > n)
            {
                return -1; // 返回一个默认值或错误码
            }
            if (k > n - k)
                k = n - k;

            int result = 1;

            for (int i = 0; i < k; i++)
            {
                result *= (n - i);
                result /= (i + 1);
            }

            return result;
        }

        // 计算雇员的工资
        int CalculateSalary(int hours, double wage) {
            if (hours < 0 || hours > 168)
                return 0;

            double salary = 0;
            if (hours <= 40) {
                salary = hours * wage; // 不加班
            } else if (hours <= 60) {
                salary = 40 * wage + (hours-40) * 1.5 * wage; // 加班但不超过60小时
            } else {
                salary = 40 * wage + 20 * 1.5 * wage + (hours-60) * 3 * wage; // 超过60小时加班
            }
            return (int)salary;
        }
    };
}
#endif //TRANSLATION_COMPUTER_H
