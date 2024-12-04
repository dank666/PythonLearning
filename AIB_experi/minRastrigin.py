import numpy as np
import math
import matplotlib.pyplot as plt
import time

# Rastrigin
def rastrigin(x1, x2):
    return 20 + x1**2 + x2**2 - 10 * (math.cos(2 * math.pi * x1) + math.cos(2 * math.pi * x2))

# 初始化种群，返回一个随机的二进制矩阵
def initialize_population(pop_size, chrom_length):  # pop_size:种群大小， chrom_length:染色体长度
    return np.random.randint(0, 2, (pop_size, chrom_length))  # 返回一个二维矩阵，行数表示种群规模，列数表示一个染色体的长度，每行都是由0,1组成的二进制串

# 将二进制染色体解码为实际变量值(处理单个染色体)
def decode_chromosome(chrom, bounds):  # bounds:变量的范围
    n_vars = len(bounds)  # 确定有多少个变量， n_vars=2
    vars_length = len(chrom) // n_vars  # 每个变量对应染色体二进制长度的一半, vars_length=50
    decoded = []  # 存储解码后的变量值
    for i, bound in enumerate(bounds):  # enumerate是一个内置函数，用来提取可迭代对象的元素及其索引，在这里依次提取0,(-5.12, 5.12)   1,(-5.12, 5.12)
        start, end = i * vars_length, (i + 1) * vars_length  # 每个变量对应的二进制段
        substring = chrom[start:end]  # 提取染色体中对应变量的二进制子串
        decimal = int("".join(map(str, substring)), 2)  # 二进制子串转换为十进制整数， “map(str, substring”中，substring是一个可迭代对象，map（）将substring中每个元素转换为字符，返回一个列表，然后int("".join(), 2)先将列表转换为一个字符串，然后将二进制字符串转换为一个十进制整数
        # 根据变量的范围将整数映射到实际变量值
        real_value = bound[0] + (bound[1] - bound[0]) * (decimal / (2**vars_length - 1))  # bound=(-5.12, 5.12)，2**vars_length - 1表示当前基因编码能表示的最大整数值
        decoded.append(real_value)
    return decoded  # 返回包含x1,x2的列表[x1, x2]

# 计算适应度函数值，负的rastrigin函数值(适应度越大越好)
def fitness_function(chrom, bounds):
    decoded = decode_chromosome(chrom, bounds)  # [x1, x2]
    return -rastrigin(*decoded)  # 返回负的目标函数值，*decoded是解包，将decoded列表中的元素x1,x2作为独立的参数传递给rastrigin函数，rastrigin(*decoded)等价于rastrigin(x1, x2)
    # 因为在遗传算法中，适应度通常越大越好，所以对目标函数取负，可以使适应度越大越好

# 选择，轮盘赌，根据适应度选择种群中的个体
def selection(population, fitness):  # population:种群，二维数组，每行表示一个个体， fitness:个体的适应度值，一维数组，与种群的个体一一对应
    probs = fitness / fitness.sum()  # 归一化适应度值作为选择概率， /表示浮点除法，  返回一个归一化后的一维数组，每个元素表示对应个体被选择的概率
    indices = np.random.choice(len(population), size=len(population), p=probs)  # 按概率选择个体，np.random.choice(...) 用于根据给定的概率分布随机选择元素。len(population)表示选取的行数，size=len(population)表示生成的样本数量为 a 的行数
    return population[indices]  # 返回选择后的种群

# 交叉，单点交叉
# parent1, parent2: 两个父代染色体，p_c:交叉概率
def crossover(parent1, parent2, p_c):
    if np.random.rand() < p_c:  # 随机决定是否进行交叉,p_c=0.8
        point = np.random.randint(1, len(parent1))  # 随机选择交叉点
            # 交叉生成两个子代
        return np.concatenate((parent1[:point], parent2[point:])), np.concatenate((parent2[:point], parent1[point:]))
    return parent1, parent2  # 不进行交叉则直接返回父代

# 变异， 对染色体中的每个位以概率p_m进行翻转
def mutation(chrom, p_m):
    for i in range(len(chrom)):
        if np.random.rand() < p_m:  # 变异概率0.01,rand产生的随机数小于0.01就变异
            chrom[i] = 1 - chrom[i]  # 翻转，1->0 0->1
    return chrom

# 遗传算法主算法
def genetic_algorithm(bounds, precision, pop_size, chrom_length, max_generations, p_c, p_m):
    # 初始化种群
    population = initialize_population(pop_size, chrom_length)  # population是一个二进制数组
    best_solution = None  # 用于记录当前最优解
    best_fitness = -np.inf  # 当前最优适应度值, np.inf表示无穷大
    best_solutions = []  # 记录每代的最优解
    best_fitnesses = []  # 记录每代的最优适应度
    
    # 主循环，迭代 max_generations 次
    for generation in range(max_generations):
        # 计算种群中每个个体的适应度
        fitness = np.array([fitness_function(ind, bounds) for ind in population])  # ind是一个一维二进制列表，表示一条染色体，fitness为一个一维矩阵，每个元素代表每个个体对应的适应度函数值
        # 更新当前最优解和最优适应度
        if fitness.max() > best_fitness:
            best_fitness = fitness.max()  # 更新最优适应度
            best_solution = population[fitness.argmax()]  # 更新最优解    fitness.argmax()用来获取数组中最大值索引    best_solution是适应度函数值最大的二进制串
        
        best_fitnesses.append(fitness.max())
        best_solutions.append(decode_chromosome(best_solution, bounds))

        # 选择操作
        population = selection(population, fitness)
        
        # 交叉操作，生成新种群
        new_population = []
        for i in range(0, len(population), 2):  # 两个个体一组 i=0 2 4 6 ...
            parent1, parent2 = population[i], population[i + 1]
            child1, child2 = crossover(parent1, parent2, p_c)  # 交叉生成两个子代
            new_population.append(child1)
            new_population.append(child2)
        
        # 变异操作，对新种群的每个个体进行变异
        population = np.array([mutation(ind, p_m) for ind in new_population])
    
    # 解码最终的最优解
    decoded_solution = decode_chromosome(best_solution, bounds)
    return decoded_solution, -best_fitness, best_fitnesses, best_solutions  # 返回最优解及其目标函数值

# 参数设置
bounds = [(-5.12, 5.12), (-5.12, 5.12)]  # 搜索空间，每个变量的上下界
precision = 1e-15  # 求解精度
pop_size = 10000  # 种群规模
chrom_length = 1000  # 每个染色体的总长度（x1 和 x2 各占一半）
max_generations = 100  # 最大迭代次数
p_c = 0.8  # 交叉概率
p_m = 0.01  # 变异概率

start_time = time.perf_counter()

# 运行遗传算法
solution, min_value, best_fitnesses, best_solutions = genetic_algorithm(bounds, precision, pop_size, chrom_length, max_generations, p_c, p_m)

end_time = time.perf_counter()
elapsed_time = end_time - start_time

# 输出结果和运行时间
print("运行时间为：", elapsed_time)
print(f"最优解：{solution}")  # 打印最优解
print(f"最小值：{min_value}")  # 打印最小值

# 绘制结果图
# 1. 绘制每代的最佳适应度
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(best_fitnesses, label="Best Fitness")
plt.xlabel("Generation")
plt.ylabel("Best Fitness Value")
plt.title("Best Fitness Over Generations")
plt.legend()

# 2. 绘制每代的最优解（x1 和 x2）
best_solutions = np.array(best_solutions)
plt.subplot(1, 2, 2)
plt.plot(best_solutions[:, 0], label="x1 (Best Solution)", color="r")
plt.plot(best_solutions[:, 1], label="x2 (Best Solution)", color="b")
plt.xlabel("Generation")
plt.ylabel("Solution Value")
plt.title("Best Solution (x1, x2) Over Generations")
plt.legend()

plt.savefig('/home/wtejing/Python/AIB_experi/best_solution_plot.png')