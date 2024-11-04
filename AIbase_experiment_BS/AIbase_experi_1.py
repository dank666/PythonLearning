import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageDraw, ImageTk

# 模糊集合定义
temperature_low = [(1, 1), (2, 0.6), (3, 0.3), (4, 0.0), (5, 0.0)]
damper_large = [(1, 0), (2, 0.0), (3, 0.3), (4, 0.6), (5, 1)]


def parse_fuzzy_set(input_values):
    fuzzy_set = []
    for i, value in enumerate(input_values):
        if value >= 0 and value <= 1:
            fuzzy_set.append((i + 1, value))
        else:
            raise ValueError(f"Invalid value {value} for membership degree; should be between 0 and 1.")
    return fuzzy_set


def fuzzy_inference(temperature_membership):
    # 计算模糊推理
    damper_membership = [(value[0], min(value[1], temperature_membership[value[0] - 1][1])) for value in damper_large]
    return damper_membership


def defuzzify_max_membership(damper_membership):
    max_membership = max(value[1] for value in damper_membership)
    return next(value[0] for value in damper_membership if value[1] == max_membership)


def defuzzify_weighted_average(damper_membership):
    numerator = sum(value[0] * value[1] for value in damper_membership)
    denominator = sum(value[1] for value in damper_membership)
    return numerator / denominator if denominator != 0 else 0


def defuzzify_median(damper_membership):
    sorted_membership = sorted(damper_membership, key=lambda x: x[0])
    n = len(sorted_membership)
    midpoint = n // 2
    if n % 2 == 0:
        return (sorted_membership[midpoint - 1][0] + sorted_membership[midpoint][0]) / 2
    else:
        return sorted_membership[midpoint][0]


def calculate_damper():
    try:
        # 获取用户输入的温度隶属度值
        input_values = [float(entry.get()) for entry in entries]

        # 检查输入值是否在有效范围内
        if any(value < 0 or value > 1 for value in input_values):
            raise ValueError("Membership degrees must be between 0 and 1.")

        # 解析输入值为模糊集合
        temperature_membership = parse_fuzzy_set(input_values)

        # 计算风门开度
        damper_membership = fuzzy_inference(temperature_membership)

        # 计算三种去模糊化方法的结果
        max_output = defuzzify_max_membership(damper_membership)
        avg_output = defuzzify_weighted_average(damper_membership)
        median_output = defuzzify_median(damper_membership)

        # 清空结果显示框
        text_results.delete(1.0, tk.END)

        # 显示结果
        result_text = (
            f"Results for the given temperature membership:"
            f"\n- Maximum Membership Method: {max_output:.2f}"
            f"\n- Weighted Average Method: {avg_output:.2f}"
            f"\n- Median Method: {median_output:.2f}"
        )
        text_results.insert(tk.END, result_text)
    except ValueError as e:
        # 处理输入错误
        messagebox.showerror("Error", str(e))


def create_floral_pattern(width, height, pattern_size):
    # 创建一个花朵图案
    pattern = Image.new("RGBA", (pattern_size, pattern_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(pattern)

    # 绘制花朵
    petal_color = "#7986CB"
    center_color = "#FFFFFF"
    petal_radius = 20
    center_radius = 10

    # 绘制中心圆
    draw.ellipse([(pattern_size // 2 - center_radius, pattern_size // 2 - center_radius),
                  (pattern_size // 2 + center_radius, pattern_size // 2 + center_radius)],
                 fill=center_color)

    # 绘制花瓣
    num_petals = 8
    angle_increment = 360 // num_petals
    for i in range(num_petals):
        angle_start = i * angle_increment - 180
        angle_end = angle_start + 180
        draw.pieslice([(pattern_size // 2 - petal_radius, pattern_size // 2 - petal_radius),
                       (pattern_size // 2 + petal_radius, pattern_size // 2 + petal_radius)],
                      start=angle_start, end=angle_end, fill=petal_color)

    return pattern


def update_background(event=None):
    global background_photo
    global background_label

    # 根据窗口大小重新创建背景图案
    pattern_size = 50
    background_image = Image.new("RGBA", (root.winfo_width(), root.winfo_height()), (255, 255, 255, 255))
    floral_pattern = create_floral_pattern(pattern_size, pattern_size, pattern_size)
    for x in range(0, background_image.width, pattern_size):
        for y in range(0, background_image.height, pattern_size):
            background_image.paste(floral_pattern, (x, y), floral_pattern)

    # 更新背景图像
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.config(image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
    update_background()


# 创建主窗口
root = tk.Tk()
root.title('Fuzzy Logic Control')

# 初始窗口大小
root.geometry("600x400")

# 添加菜单项来切换全屏模式
menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Toggle Fullscreen", command=toggle_fullscreen)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# 定义字体样式
font_style = ("Arial", 12)
bold_font_style = ("Arial", 12, "bold")

# 创建背景标签
background_photo = None
background_label = tk.Label(root)
background_label.pack(fill=tk.BOTH, expand=True)

# 初始化背景图案
update_background()

# 创建输入区域框架
frame_input = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10)
frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# 输入标签和输入框
labels = ["Temperature Membership Degree for Value {}: ".format(i) for i in range(1, 6)]
entries = []

# 创建表格布局
for i in range(5):
    tk.Label(frame_input, text=f"Value {i + 1}:", font=bold_font_style, bg="#FFFFFF").grid(row=i, column=0, sticky="e")
    entry = tk.Entry(frame_input, width=10, font=font_style, bg="#FFFFFF")
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

# 提示文本
prompt_label = tk.Label(frame_input, text="Enter values between 0 and 1.", font=font_style, bg="#FFFFFF")
prompt_label.grid(row=5, column=0, columnspan=2, pady=(5, 10))

# 创建结果显示区域框架
frame_results = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10)
frame_results.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# 结果标签
label_results = tk.Label(frame_results, text="Results:", font=bold_font_style, bg="#FFFFFF")
label_results.grid(row=0, column=0, sticky="w")

# 结果显示框
text_results = tk.Text(frame_results, height=5, width=50, font=font_style, bg="#FFFFFF")
text_results.grid(row=1, column=0, padx=5, pady=5)

# 创建按钮
button_calculate = tk.Button(root, text="Calculate Damper Opening", command=calculate_damper, font=bold_font_style,
                             bg="#7986CB", fg="#FFFFFF", padx=10, pady=5)
button_calculate.grid(row=2, column=0, pady=10)

# 设置按钮样式
button_calculate.config(activebackground="#5C6BC0", activeforeground="#FFFFFF")

# 配置网格权重
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# 当窗口大小改变时更新背景
root.bind("<Configure>", update_background)

# 运行主循环
root.mainloop()