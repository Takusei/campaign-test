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

        for idx, key in enumerate(self.placeholders):
            tk.Label(root, text=key).grid(row=idx, column=0, sticky=tk.W, padx=5, pady=2)
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

        # Insert JS from 2nd HTML into head
        for script_tag in second_soup.find_all("script"):
            template_soup.head.append(script_tag)

        # Replace form action/name
        second_form = second_soup.find("form")
        form_action = second_form.get("action", "") if second_form else ""
        form_name = second_form.get("name", "") if second_form else ""

        html_str = str(template_soup)
        for key, entry in self.entries.items():
            html_str = html_str.replace(f"【REPLACE: {key}】", entry.get())
        html_str = html_str.replace("form[ACTION]", form_action).replace("form[NAME]", form_name)
        template_soup = BeautifulSoup(html_str, "html.parser")

        form = template_soup.find("form", {"class": "userSurvey__form"})

        # Replace radio button info (keep template style)
        second_radios = second_soup.find_all("input", {"type": "radio"})
        second_labels = second_soup.find_all("label")

        template_radios = form.find_all("input", {"type": "radio"})
        template_labels = form.find_all("label", {"class": "userSurvey__form-list-label01"})

        for new_input, new_label, old_input, old_label in zip(second_radios, second_labels, template_radios, template_labels):
            old_input["id"] = new_input.get("id", "")
            old_input["name"] = new_input.get("name", "")
            old_input["value"] = new_input.get("value", "")
            old_label["for"] = new_input.get("id", "")
            old_label.string = new_label.text.strip()

        # Replace textarea "name" using <input type="text"> from 2nd HTML
        second_text_input = second_soup.find("input", {"type": "text"})
        if second_text_input:
            textarea = form.find("textarea", {"class": "big"})
            if textarea:
                textarea["name"] = second_text_input.get("name", "")

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output_{now}.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(template_soup.prettify())

        messagebox.showinfo("Success", f"Generated: {output_file}")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLGeneratorApp(root)
    root.mainloop()
