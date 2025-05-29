import tkinter as tk
from tkinter import messagebox

# Updated replacement keys from your latest template
REPLACEMENTS = [
    ("Page Title", "【REPLACE: Page Title】"),
    ("Meta Description", "【REPLACE: Meta Description】"),
    ("OG Description", "【REPLACE: OG Description】"),
    ("Head Line1", "【REPLACE: Head Line1】"),
    ("Head Line2", "【REPLACE: Head Line2】"),
    ("Head Line3", "【REPLACE: Head Line3】"),
    ("Deadline year", "【REPLACE: Deadline year】"),
    ("Deadline month", "【REPLACE: Deadline month】"),
    ("Deadline day", "【REPLACE: Deadline day】"),
    ("Deadline weekday", "【REPLACE: Deadline weekday】"),
    ("Deliver date", "【REPLACE: Deliver date】"),
    ("Extract year", "【REPLACE: Extract year】"),
    ("Extract month", "【REPLACE: Extract month】"),
    ("Extract day", "【REPLACE: Extract day】"),
    ("Extract weekday", "【REPLACE: Extract weekday】"),
    ("Form Submission URL", "【REPLACE: Form Submission URL】"),
    ("First Question", "【REPLACE: First Question】"),
    ("Option 1", "【REPLACE: Option 1】"),
    ("Option 2", "【REPLACE: Option 2】"),
    ("Second Question", "【REPLACE: Second Question】"),
]

entries = {}

def generate_html():
    try:
        with open("template.html", "r", encoding="utf-8") as f:
            html = f.read()

        for label, placeholder in REPLACEMENTS:
            widget = entries[label]
            value = widget.get() if isinstance(widget, tk.Entry) else widget.get("1.0", tk.END).strip()
            html = html.replace(placeholder, value)

        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html)

        messagebox.showinfo("成功", "output.html が正常に生成されました！")

    except Exception as e:
        messagebox.showerror("エラー", str(e))

# GUI Setup
root = tk.Tk()
root.title("HTMLテンプレート自動生成ツール")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Dynamically create labels and input fields
for label_text, _ in REPLACEMENTS:
    tk.Label(frame, text=label_text, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

    if "Description" in label_text or "Question" in label_text or "Head Line" in label_text:
        widget = tk.Text(frame, height=3, width=70)
    else:
        widget = tk.Entry(frame, width=70)

    widget.pack(padx=10)
    entries[label_text] = widget

tk.Button(frame, text="生成 (Generate HTML)", command=generate_html, bg="lightblue").pack(pady=20)

root.mainloop()
