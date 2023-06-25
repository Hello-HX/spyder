from PiMethods import *

if __name__ == '__main__':

    results = []

    # Monte Carlo 方法
    for n in [1, 5, 10, 25, 50, 75, 100, 250, 500, 1000, 2000]:
        pi, time_cost = MonteCarlo(n * 1000)
        accuracy = calculate_accuracy(pi)
        results.append(("MonteCarlo", n, pi, accuracy, time_cost))

    # BBP 公式方法
    for n in [1, 5, 10, 25, 50, 75, 100, 250, 500, 1000, 2000]:
        pi, time_cost = bbp(n)
        accuracy = calculate_accuracy(pi)
        results.append(("BBP", n, pi, accuracy, time_cost))

    # Trigonometric 方法
    for n in [1, 5, 10, 25, 50, 75, 100, 250, 500, 1000, 2000]:
        pi, time_cost = trigonometric(n)
        accuracy = calculate_accuracy(pi)
        results.append(("Trigonometric", n, pi, accuracy, time_cost))

    # Infinite 方法
    for n in [1, 5, 10, 25, 50, 75, 100, 250, 500, 1000, 2000]:
        pi, time_cost = Infinite(n)
        accuracy = calculate_accuracy(pi)
        results.append(("Infinite", n, pi, accuracy, time_cost))

    backup = results

    # 将结果按 n 值输出到文件
    for n in [1, 5, 10, 25, 50, 75, 100, 250, 500, 1000, 2000]:
        file = str(n) + '.txt'
        with open(file, 'w') as file:
            for method, loop, pi, accuracy, time_cost in results:
                if loop == n:
                    file.write(f"{method} {pi} {accuracy:.10f} {time_cost:.6f}\n")
    # 打印结果
    for result in results:
        print(result)

    '''
    # Infinite 方法验证
    results=[]
    for n in [1,5,10,25,50,75,100,250,500, 1000,2000,20000,100000]:
        pi,time_cost = Infinite(n)
        accuracy = calculate_accuracy(pi)
        results.append(("Infinite",n,pi,accuracy,time_cost))

    backup = results
    # 绘制精度-循环次数曲线和精度-速度曲线
    plot_accuracy_iterations(backup)

    plot_accuracy_speed(backup)
    '''
    # 绘制精度-循环次数曲线和精度-速度曲线
    plot_accuracy_iterations(backup)
    plot_accuracy_speed(backup)

    # 按精度排序结果
    sort_accuracy(results)
