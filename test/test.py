import difflib
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

################################ CODE ################################

def compare_text(text1, text2):
    if text1 == text2:
        return 1.0

    ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    return ratio

def toggle_plagiarism_input_state(*args):
    comparison_mode = comparison_var.get()

    if comparison_mode == "So sánh với file văn bản":
        plagiarism_input.config(state='disabled')
    else:
        plagiarism_input.config(state='normal')

def get_matching_text(text1, text_list):
    matching_text = ""

    for i, plagiarism in enumerate(text_list, start=1):
        matcher = difflib.SequenceMatcher(None, text1, plagiarism)
        matching_blocks = matcher.get_matching_blocks()

        matching_text += f"\nĐoạn {i}:\n"
        for match in matching_blocks:
            start, end, length = match
            if length > 0:
                matching_text += f"    - Từ {start} đến {start + length - 1}: {text1[start:start+length]}\n"

    return matching_text

def check_plagiarism():
    input_text = text_input.get("1.0", "end-1c").strip()
    comparison_mode = comparison_var.get()
    plagiarism_list = []  

    if not input_text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đoạn văn bản cần kiểm tra.")
        return

    if comparison_mode == "Nhập văn bản":
        plagiarism_list = plagiarism_input.get("1.0", "end-1c").split("\n")
        browse_button.config(state='disabled')  
    elif comparison_mode == "So sánh với file văn bản":
        browse_button.config(state='normal')  
        file_path = file_path_var.get()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                plagiarism_list = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file. Vui lòng chọn lại.")
            return

    if not plagiarism_list:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đoạn văn mẫu hoặc chọn một file văn bản mẫu.")
        return

    max_ratio = 0

    matching_text = ""

    for i, plagiarism in enumerate(plagiarism_list, start=1):
        ratio = compare_text(input_text, plagiarism)
        max_ratio = max(max_ratio, ratio)
        matching_text += f"Đoạn {i} - Tỉ lệ khớp: {ratio * 100:.2f}%\n"
        matching_text += get_matching_text(input_text, [plagiarism])

    result_label.config(text=f"Tỉ lệ khớp cao nhất là: {max_ratio * 100:.2f}%", anchor="e")

    if max_ratio > 0.25:
        result_label.config(text=result_label.cget("text") + "\nPhát hiện có độ trùng lặp CAO !!!")
        result_label.config(text=result_label.cget("text") + "\n\n> PHÁT HIỆN ĐẠO VĂN <")
    else:
        result_label.config(text=result_label.cget("text") + "\nĐộ trùng lặp thuộc mức AN TOÀN !!!")
        result_label.config(text=result_label.cget("text") + "\n\n> VĂN BẢN ĐƯỢC CHẤP NHẬN <")

    # Hiển thị phần văn bản được phát hiện giống nhau ở Textbox mới
    matching_textbox.delete(1.0, tk.END)
    matching_textbox.insert(tk.END, matching_text)

def browse_file():
    comparison_mode = comparison_var.get()

    if comparison_mode == "Nhập văn bản":
        messagebox.showwarning("Cảnh báo", "Vui lòng chuyển sang chế độ 'So sánh với file văn bản' để chọn file.")
        return

    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    file_path_var.set(file_path)

def clear_fields():
    text_input.delete("1.0", tk.END)
    plagiarism_input.delete("1.0", tk.END)
    file_path_var.set("")
    browse_button.config(state='normal')
    result_label.config(text="")
    matching_textbox.delete(1.0, tk.END)
    

################################ GIAO DIỆN ################################
root = tk.Tk()
root.title("Kiểm tra đạo văn")

# Cố định kích thước cửa sổ
window_width = 1170
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

comparison_var = tk.StringVar(root)
comparison_var.set("Nhập văn bản")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccC")

text_label = tk.Label(root, text="Chọn chế độ so sánh:")
text_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

comparison_menu = ttk.Combobox(root, textvariable=comparison_var, values=["Nhập văn bản", "So sánh với file văn bản"], state="readonly")
comparison_menu.grid(row=1, column=0, padx=10, pady=5, sticky="w")
comparison_menu.bind("<<ComboboxSelected>>", toggle_plagiarism_input_state)

text_input_label = tk.Label(root, text="Nhập đoạn văn bản cần kiểm tra:")
text_input_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

text_input = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, bg="#f0f0f0")
text_input.grid(row=3, column=0, padx=10, pady=5, sticky="w")

plagiarism_label = tk.Label(root, text="Nhập văn bản mẫu:")
plagiarism_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

plagiarism_input = scrolledtext.ScrolledText(root, width=80, height=5, wrap=tk.WORD, bg="#f0f0f0")
plagiarism_input.grid(row=5, column=0, padx=10, pady=5, sticky="w")

file_path_label = tk.Label(root, text="Chọn file văn bản mẫu:")
file_path_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

file_path_var = tk.StringVar(root)
file_path_entry = tk.Entry(root, textvariable=file_path_var, state='readonly', width=100)
file_path_entry.grid(row=7, column=0, padx=10, pady=5, sticky="w")

browse_button = tk.Button(root, text="Chọn file", command=browse_file, state='normal', bg="#4caf50", fg="white")
browse_button.grid(row=7, column=2, pady=10)

check_button = tk.Button(root, text="Kiểm tra", command=check_plagiarism, bg="#2196f3", fg="white")
check_button.grid(row=5, column=3, pady=10)

clear_button = tk.Button(root, text="Làm mới", command=clear_fields, bg="#e74c3c", fg="white")
clear_button.grid(row=5, column=2, pady=10)

result_label = tk.Label(root, text="", bg="#f0f0f0", font=("Arial", 18))
result_label.grid(row=3, column=1, padx=10, pady=5, sticky="we", columnspan=2)

matching_textbox = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD, bg="#f0f0f0")
matching_textbox.grid(row=10, column=0, padx=10, pady=5, sticky="w", columnspan=2)

root.mainloop()
