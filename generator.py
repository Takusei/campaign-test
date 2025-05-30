import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import re
from bs4 import BeautifulSoup

# List of placeholders and GUI labels
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
    ("Second Question", "【REPLACE: Second Question】")
]

entries = {}

def generate_html():
    try:
        template_file = "template.html"
        with open(template_file, "r", encoding="utf-8") as f:
            template_html = f.read()

        # Get replacement values from GUI
        for label, placeholder in REPLACEMENTS:
            widget = entries[label]
            value = widget.get() if isinstance(widget, tk.Entry) else widget.get("1.0", tk.END).strip()
            template_html = template_html.replace(placeholder, value)

        # Ask user for second HTML file
        second_file_path = filedialog.askopenfilename(
            title="Select the 2nd HTML file",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if not second_file_path:
            messagebox.showwarning("キャンセル", "2つ目のHTMLファイルが選択されていません。")
            return

        with open(second_file_path, "r", encoding="utf-8") as f:
            second_html = f.read()

        second_soup = BeautifulSoup(second_html, "html.parser")
        new_body_content = "".join(str(tag) for tag in second_soup.body.contents if tag.name != "script")
        new_script_tags = second_soup.find_all("script")

        # Replace the entire <section id="userSurvey-content">...</section>
        template_soup = BeautifulSoup(template_html, "html.parser")
        old_section = template_soup.find("section", id="userSurvey-content")
        if old_section:
            new_section = BeautifulSoup(new_body_content, "html.parser")
            old_section.replace_with(new_section)

        # Append script tags to body
        for script in new_script_tags:
            template_soup.body.append(script)

        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output_{timestamp}.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(template_soup))

        messagebox.showinfo("成功", f"{output_file} を生成しました。")

    except Exception as e:
        messagebox.showerror("エラー", str(e))

# GUI setup
root = tk.Tk()
root.title("HTMLテンプレート生成ツール")

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

# Create input fields
for label, _ in REPLACEMENTS:
    tk.Label(frame, text=label, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    if "Description" in label or "Question" in label or "Head Line" in label:
        widget = tk.Text(frame, height=3, width=70)
    else:
        widget = tk.Entry(frame, width=70)
    widget.pack(padx=10)
    entries[label] = widget

# Button to generate
tk.Button(frame, text="生成 (Generate HTML)", command=generate_html, bg="lightblue").pack(pady=20)

root.mainloop()
