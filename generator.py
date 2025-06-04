import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import datetime
import os

class HTMLGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Generator")
        self.entries = {}

        self.placeholders = [
            "Page Title", "Canonical URL", "Meta Description", "OG Description",
            "Head Line1", "Head Line2", "Head Line3",
            "Deadline year", "Deadline month", "Deadline day", "Deadline weekday",
            "Deliver date", "Extract year", "Extract month", "Extract day", "Extract weekday"
        ]

        def limit_length(P):
            return len(P) <= 20

        vcmd = (root.register(limit_length), '%P')

        for idx, key in enumerate(self.placeholders):
            tk.Label(root, text=key).grid(row=idx, column=0, sticky=tk.W, padx=5, pady=2)
            if key.startswith("Head Line"):
                entry = tk.Entry(root, width=60, validate="key", validatecommand=vcmd)
            else:
                entry = tk.Entry(root, width=60)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.entries[key] = entry

        tk.Button(root, text="Select 2nd HTML File", command=self.load_second_html).grid(row=len(self.placeholders), column=0, pady=10)
        tk.Button(root, text="Generate HTML", command=self.generate_html).grid(row=len(self.placeholders), column=1, pady=10)

        self.second_html_path = None

    def load_second_html(self):
        self.second_html_path = filedialog.askopenfilename(title="Select second HTML file", filetypes=[("HTML files", "*.html")])
        if self.second_html_path:
            messagebox.showinfo("File Selected", f"Loaded: {os.path.basename(self.second_html_path)}")

    def generate_html(self):
        if not self.second_html_path:
            messagebox.showerror("Error", "You must select the 2nd HTML file.")
            return

        with open("template.html", "r", encoding="utf-8") as f:
            template_soup = BeautifulSoup(f, "html.parser")

        with open(self.second_html_path, "r", encoding="utf-8", errors="ignore") as f:
            second_soup = BeautifulSoup(f, "html.parser")

        # Insert <script> from second HTML
        for script_tag in second_soup.find_all("script"):
            template_soup.head.append(script_tag)

        # Replace placeholders
        html_str = str(template_soup)
        for key, entry in self.entries.items():
            html_str = html_str.replace(f"【REPLACE: {key}】", entry.get())
        template_soup = BeautifulSoup(html_str, "html.parser")

        # Replace form action, name, onSubmit
        src_form = second_soup.find("form")
        target_form = template_soup.find("form")
        if src_form and target_form:
            if src_form.get("action"):
                target_form["action"] = src_form["action"]
            if src_form.get("name"):
                target_form["name"] = src_form["name"]
            if src_form.get("onsubmit"):
                target_form["onsubmit"] = src_form["onsubmit"]

        # Replace radio inputs and labels
        second_radios = second_soup.find_all("input", {"type": "radio"})
        second_labels = second_soup.find_all("label")
        template_radios = target_form.find_all("input", {"type": "radio"})
        template_labels = target_form.find_all("label", {"class": "userSurvey__form-list-label01"})

        for new_input, new_label, old_input, old_label in zip(second_radios, second_labels, template_radios, template_labels):
            old_input["id"] = new_input.get("id", "")
            old_input["name"] = new_input.get("name", "")
            old_input["value"] = new_input.get("value", "")
            old_label["for"] = new_input.get("id", "")
            old_label.string = new_label.get_text(strip=True)

        # Replace textarea attributes with <input type=text> from second.html, but keep tag as <textarea>
        second_text_input = second_soup.find("input", {"type": "text"})
        textarea = target_form.find("textarea")
        if second_text_input and textarea:
            textarea["name"] = second_text_input.get("name", "")

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output_{now}.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(template_soup.prettify()))

        messagebox.showinfo("Success", f"Generated: {output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLGeneratorApp(root)
    root.mainloop()