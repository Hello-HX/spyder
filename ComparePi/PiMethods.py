import math
import random
import time
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

'''
1、MonteCarlo(num_iterations)：
用蒙特卡洛方法计算圆周率，参数num_iterations表示模拟的点数。
返回值为pi_estimate和time_cost，分别表示计算得到的圆周率估计值和计算时间。
'''


# 蒙特卡洛方法计算圆周率
def MonteCarlo(num_iterations):
    print("蒙特卡洛方法计算")
    # begin = time.time()
    begin = time.perf_counter()
    inside_circle = 0
    total_points = 0
    getcontext().prec = 100
    for i in range(1, num_iterations + 1):
        x = Decimal(str(random.uniform(-1.0, 1.0)))
        y = Decimal(str(random.uniform(-1.0, 1.0)))
        if (x * x + y * y) < Decimal(1.0):
            inside_circle += 1
        total_points += 1
    pi_estimate = Decimal(4) * Decimal(inside_circle) / Decimal(total_points)
    end = time.perf_counter()
    time_cost = end - begin
    return round(pi_estimate, 10), time_cost * 1000000


'''
2、bbp(N)：
用BBP公式计算圆周率，参数N表示计算的级数项数。
返回值为pi和time_cost，分别表示计算得到的圆周率值和计算时间。
'''


# 公式法
def bbp(N):
    print("公式法计算")
    begin = time.perf_counter()
    pi = Decimal(0)
    getcontext().prec = 100
    for k in range(N):
        term1 = Decimal(4) / Decimal(8 * k + 1)
        term2 = Decimal(2) / Decimal(8 * k + 4)
        term3 = Decimal(1) / Decimal(8 * k + 5)
        term4 = Decimal(1) / Decimal(8 * k + 6)
        term = (term1 - term2 - term3 - term4) / Decimal(16) ** Decimal(k)
        pi += term
    end = time.perf_counter()
    time_cost = end - begin
    return round(pi, 10), time_cost * 1000000


'''
3、trigonometric(k)：
用三角迭代法计算圆周率，参数k表示迭代次数。
返回值为pi_val和time_cost，分别表示计算得到的圆周率估计值和计算时间。
'''


# 三角迭代
def trigonometric(k):
    print("三角迭代法计算")
    begin = time.perf_counter()
    a = Decimal(1)
    b = Decimal(1) / Decimal(math.sqrt(2))
    t = Decimal(1) / Decimal(4)
    p = Decimal(1)
    getcontext().prec = 1000000
    for i in range(k):
        atemp = (a + b) / Decimal(2)
        btemp = Decimal(math.sqrt(a * b))
        ttemp = t - p * (a - atemp) ** Decimal(2)
        ptemp = Decimal(2) * p
        a, b, t, p = atemp, btemp, ttemp, ptemp
    end = time.perf_counter()
    time_cost = end - begin
    pi_val = (a + b) ** Decimal(2) / (Decimal(4) * t)
    return round(pi_val, 10), time_cost * 1000000


'''
4、Infinite(num_terms)：
用无穷级数法计算圆周率，参数num_terms表示计算的级数项数。
返回值为pi_val和time_cost，分别表示计算得到的圆周率值和计算时间。
'''


# 无穷级数的方法
def Infinite(num_terms):
    print("无穷级数方法计算")
    begin = time.perf_counter()
    pi = Decimal(0)
    sign = Decimal(1)
    getcontext().prec = 1000000
    for i in range(1, num_terms * 2, 2):
        term = sign / Decimal(i)
        pi += term
        sign *= -1
    end = time.perf_counter()
    time_cost = end - begin
    pi_val = pi * Decimal(4)
    return round(pi_val, 10), time_cost * 1000000


'''
5、calculate_accuracy(pi)：
计算pi与标准圆周率的精度，参数pi为计算得到的圆周率估计值。
返回值为accuracy，表示pi与标准圆周率的精度。
'''


# 精度计算
def calculate_accuracy(pi):
    getcontext().prec = len(str(pi)) + 5
    pi_val = Decimal(str(pi))
    std_val = Decimal(str(math.pi))
    error = abs(pi_val - std_val)
    accuracy = -Decimal.log10(error)
    return round(accuracy, 2)


'''
6、plot_accuracy_iterations(results)：
绘制精度-循环次数曲线，参数results为一个列表，包含了所有计算得到的圆周率估计值、循环次数、计算时间和精度。
该函数将绘制每种方法的精度-循环次数曲线，并将结果保存为Accuracy--Iterations.jpg文件。
'''


# 绘制精度-循环次数曲线
def plot_accuracy_iterations(results):
    # 获取所有方法名称
    methods = list(set([result[0] for result in results]))
    results.sort(key=lambda x: x[1], reverse=False)

    # 绘制多条曲线
    for method in methods:
        iterations = []
        accuracies = []
        for result in results:
            if result[0] == method:
                iterations.append(result[1])
                accuracies.append(result[3])
                print(result[1])
        plt.plot(iterations, accuracies, 'o--', label=method)

    # 添加坐标轴标签、标题和网格线
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy')
    # 设置x轴坐标范围和缩放方式
    plt.xlim([1, 1000])
    plt.xscale('log')
    plt.title('Accuracy--Iterations')
    plt.grid(True)

    # 显示图形
    plt.legend()
    plt.savefig('Accuracy--Iterations.jpg', dpi=300, bbox_inches='tight')
    plt.show()


'''
7、plot_accuracy_speed(results)：
绘制精度-速度曲线，参数results为一个列表，包含了所有计算得到的圆周率估计值、循环次数、计算时间和精度。
该函数将绘制每种方法的精度-速度曲线，并将结果保存为time_cost--Accuracy.jpg文件。
'''


# 绘制精度-速度曲线
def plot_accuracy_speed(results):
    # 获取所有方法名称
    methods = list(set([result[0] for result in results]))
    results.sort(key=lambda x: x[1], reverse=False)
    results.sort(key=lambda x: x[4], reverse=False)
    # 绘制多条曲线
    for method in methods:
        time_cost = []
        accuracies = []
        for result in results:
            if result[0] == method:
                time_cost.append(result[4])
                accuracies.append(result[3])
        plt.plot(time_cost, accuracies, 'o--', label=method)

    # 添加坐标轴标签、标题和网格线
    plt.xlabel('time_cost')
    plt.ylabel('Accuracy')
    plt.xlim([1, 5000000])
    plt.xscale('log')
    plt.title('time_cost--Accuracy')
    plt.grid(True)

    # 显示图形
    plt.legend()
    plt.savefig('time_cost--Accuracy.jpg', dpi=300, bbox_inches='tight')
    plt.show()


'''
8、sort_accuracy(results)：
按精度对结果进行排序，参数results为一个列表，包含了所有计算得到的圆周率估计值、循环次数、计算时间和精度。
该函数将按照精度从高到低的顺序对结果进行排序。
'''


# 按精度排序结果
def sort_accuracy(results):
    results.sort(key=lambda x: x[3], reverse=True)
