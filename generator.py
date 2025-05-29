import tkinter as tk
from tkinter import messagebox
import os

def generate_html():
    try:
        with open("template.html", "r", encoding="utf-8") as f:
            html_template = f.read()

        # Create a dictionary of replacements
        replacements = {
            "【REPLACE: Page Title】": entry_title.get(),
            "【REPLACE: Canonical URL】": entry_canonical.get(),
            "【REPLACE: Meta Description】": entry_description.get(),
            "【REPLACE: OG Title】": entry_og_title.get(),
            "【REPLACE: OG Description】": entry_og_description.get(),
            "【REPLACE: OG Image URL】": entry_og_image.get(),
            "【REPLACE: Main Heading】": entry_main_heading.get(),
            "【REPLACE: Main sub text (e.g., instructions, deadline, etc.)】": entry_main_text.get("1.0", tk.END).strip(),
            "【REPLACE or Keep: Notes / Warnings / Terms】": entry_notes.get("1.0", tk.END).strip(),
            "【REPLACE: Form Submission URL】": entry_form_url.get(),
            "【REPLACE: First Question】": entry_q1.get(),
            "【REPLACE: Option 1】": entry_q1_opt1.get(),
            "【REPLACE: Option 2】": entry_q1_opt2.get(),
            "【REPLACE: Second Question】": entry_q2.get()
        }

        # Replace placeholders
        for key, value in replacements.items():
            html_template = html_template.replace(key, value)

        # Write output file
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(html_template)

        messagebox.showinfo("成功", "output.html が生成されました！")

    except Exception as e:
        messagebox.showerror("エラー", str(e))

# GUI
root = tk.Tk()
root.title("HTMLテンプレート生成ツール")

canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")
canvas.create_window((0, 0), window=frame, anchor='nw')

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))
frame.bind('<Configure>', on_configure)

def labeled_entry(parent, label, width=60):
    tk.Label(parent, text=label).pack(anchor="w", pady=(10, 0))
    e = tk.Entry(parent, width=width)
    e.pack()
    return e

def labeled_text(parent, label, height=4, width=60):
    tk.Label(parent, text=label).pack(anchor="w", pady=(10, 0))
    t = tk.Text(parent, height=height, width=width)
    t.pack()
    return t

entry_title = labeled_entry(frame, "Page Title")
entry_canonical = labeled_entry(frame, "Canonical URL")
entry_description = labeled_entry(frame, "Meta Description")
entry_og_title = labeled_entry(frame, "OG Title")
entry_og_description = labeled_entry(frame, "OG Description")
entry_og_image = labeled_entry(frame, "OG Image URL")

entry_main_heading = labeled_entry(frame, "Main Heading")
entry_main_text = labeled_text(frame, "Main Sub Text")
entry_notes = labeled_text(frame, "Notes / Warnings")

entry_form_url = labeled_entry(frame, "Form Submission URL")
entry_q1 = labeled_entry(frame, "First Question (Q1)")
entry_q1_opt1 = labeled_entry(frame, "Option 1")
entry_q1_opt2 = labeled_entry(frame, "Option 2")
entry_q2 = labeled_entry(frame, "Second Question (Q2)")

tk.Button(frame, text="生成 (Generate HTML)", command=generate_html, bg="lightblue").pack(pady=20)

root.mainloop()
