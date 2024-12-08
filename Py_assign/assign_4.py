def isPrime(number):
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def analyze_string(string):
    upper_count = 0
    lower_count = 0
    digit_count = 0
    other_count = 0

    for char in string:
        if char.isupper():
            upper_count += 1
        elif char.islower():
            lower_count += 1
        elif char.isdigit():
            digit_count += 1
        else:
            other_count += 1
    
    return (upper_count, lower_count, digit_count, other_count)

def swapCase(input_file, output_file):
    try:  # try是异常处理机制的一部分，主要用于使程序更加健壮
        with open(input_file, 'r', encoding='utf-8') as file:  # with是一种上下文管理器，主要用于避免资源浪费
            content = file.read()
        
        swapped_content = content.swapcase()

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(swapped_content)
        
        print(f"Swapped successfully -> {output_file}!")
    
    except FileNotFoundError:
         print(f"错误: 文件 '{input_file}' 未找到！")
    except Exception as e:
        print(f"Error{e}")



print("王特警，42312205")
number = int(input("请输入一个整数： "))
if isPrime(number):
    print(f"{number}是一个素数。")
else:
    print(f"{number}不是一个素数。")
print("--------------------")

string = input("请输入一个字符串： ")
result = analyze_string(string)
print(f"统计结果为：大写字母：{result[0]}，小写字母：{result[1]}，数字：{result[2]},其他：{result[3]}")
print("--------------------")

input_file = input("请输入要读取的文件路径： ")
output_file = input("请输入转换后文件的保存路径： ")
swapCase(input_file, output_file)
print("--------------------")

import pickle

# 保存字典到二进制文件
def save_grades_to_file(grades, filename):
    """
    将包含学生成绩的字典保存为二进制文件。
    """
    try:
        with open(filename, 'wb') as file:
            pickle.dump(grades, file)
        print(f"成绩字典已保存到文件: {filename}")
    except Exception as e:
        print(f"保存失败: {e}")

# 从二进制文件读取字典
def load_grades_from_file(filename):
    """
    从二进制文件读取学生成绩字典。
    """
    try:
        with open(filename, 'rb') as file:
            grades = pickle.load(file)
        print(f"从文件中读取的成绩字典: {grades}")
        return grades
    except Exception as e:
        print(f"读取失败: {e}")
        return None

# 测试程序
if __name__ == "__main__":
    # 学生成绩字典
    student_grades = {
        "Alice": 85,
        "Bob": 90,
        "Charlie": 78,
        "David": 92
    }

    # 保存和读取文件
    filename = "student_grades.pkl"
    save_grades_to_file(student_grades, filename)
    loaded_grades = load_grades_from_file(filename)
