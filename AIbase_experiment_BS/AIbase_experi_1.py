import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

# 模糊集合定义
temperature_low = [(1, 1), (2, 0.6), (3, 0.3), (4, 0.0), (5, 0.0)]
damper_large = [(1, 0), (2, 0.0), (3, 0.3), (4, 0.6), (5, 1)]


def parse_fuzzy_set(input_values):
    return [(i + 1, value) for i, value in enumerate(input_values) if 0 <= value <= 1]


def fuzzy_inference(temperature_membership):
    return [(value[0], min(value[1], temperature_membership[value[0] - 1][1])) for value in damper_large]


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
        input_values = [float(entry.get()) for entry in entries]
        if any(value < 0 or value > 1 for value in input_values):
            raise ValueError("Membership degrees must be between 0 and 1.")

        temperature_membership = parse_fuzzy_set(input_values)
        damper_membership = fuzzy_inference(temperature_membership)

        max_output = defuzzify_max_membership(damper_membership)
        avg_output = defuzzify_weighted_average(damper_membership)
        median_output = defuzzify_median(damper_membership)

        text_results.delete(1.0, tk.END)
        result_text = (
            f"Results for the given temperature membership:"
            f"\n- Maximum Membership Method: {max_output:.2f}"
            f"\n- Weighted Average Method: {avg_output:.2f}"
            f"\n- Median Method: {median_output:.2f}"
        )
        text_results.insert(tk.END, result_text)
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def create_floral_pattern(width, height, pattern_size):
    pattern = Image.new("RGBA", (pattern_size, pattern_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(pattern)

    petal_color = "#7986CB"
    center_color = "#FFFFFF"
    petal_radius = pattern_size // 4
    center_radius = pattern_size // 8

    draw.ellipse([(pattern_size // 2 - center_radius, pattern_size // 2 - center_radius),
                  (pattern_size // 2 + center_radius, pattern_size // 2 + center_radius)],
                 fill=center_color)

    num_petals = 8
    angle_increment = 360 / num_petals
    for i in range(num_petals):
        angle = i * angle_increment
        x_offset = petal_radius * 0.8 * (-1 if i % 2 == 0 else 1)
        y_offset = petal_radius * 0.8 * (1 if i < 4 else -1)

        draw.ellipse([(pattern_size // 2 - petal_radius + x_offset, pattern_size // 2 - petal_radius + y_offset),
                      (pattern_size // 2 + petal_radius + x_offset, pattern_size // 2 + petal_radius + y_offset)],
                     fill=petal_color)

    return pattern


def update_background(event=None):
    global background_photo, background_label

    pattern_size = 50
    background_image = Image.new("RGBA", (root.winfo_width(), root.winfo_height()), (255, 255, 255, 255))
    floral_pattern = create_floral_pattern(pattern_size, pattern_size, pattern_size)
    for x in range(0, background_image.width, pattern_size):
        for y in range(0, background_image.height, pattern_size):
            background_image.paste(floral_pattern, (x, y), floral_pattern)

    background_photo = ImageTk.PhotoImage(background_image)
    background_label.config(image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


root = tk.Tk()
root.title('Fuzzy Logic Control')
root.geometry("600x400")

menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Toggle Fullscreen",
                      command=lambda: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

font_style = ("Arial", 12)
bold_font_style = ("Arial", 12, "bold")

background_photo = None
background_label = tk.Label(root)
background_label.pack(fill=tk.BOTH, expand=True)
update_background()

frame_input = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10)
frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

entries = []
for i in range(5):
    tk.Label(frame_input, text=f"Value {i + 1}:", font=bold_font_style, bg="#FFFFFF").grid(row=i, column=0, sticky="e")
    entry = tk.Entry(frame_input, width=10, font=font_style, bg="#FFFFFF")
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

prompt_label = tk.Label(frame_input, text="Enter values between 0 and 1.", font=font_style, bg="#FFFFFF")
prompt_label.grid(row=5, column=0, columnspan=2, pady=(5, 10))

frame_results = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10)
frame_results.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

label_results = tk.Label(frame_results, text="Results:", font=bold_font_style, bg="#FFFFFF")
label_results.grid(row=0, column=0, sticky="w")

text_results = tk.Text(frame_results, height=5, width=50, font=font_style, bg="#FFFFFF")
text_results.grid(row=1, column=0, padx=5, pady=5)

button_calculate = tk.Button(root, text="Calculate Damper Opening", command=calculate_damper, font=bold_font_style,
                             bg="#7986CB", fg="#FFFFFF", padx=10, pady=5)
button_calculate.grid(row=2, column=0, pady=10)
button_calculate.config(activebackground="#5C6BC0", activeforeground="#FFFFFF")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

root.bind("<Configure>", update_background)
root.mainloop()
