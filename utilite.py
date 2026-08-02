import customtkinter as tk
from datetime import date

from Grossbuch import Grossbuch

HISTORY_FILE = "history.json"
CATEGORIES_FILE = "categories.json"

grossbuch = Grossbuch(HISTORY_FILE, CATEGORIES_FILE)


def add_operation():
    operation_date = date(2026, 7, int(day_entry.get()))

    amount = int(amount_entry.get())
    description = description_entry.get()
    category = category_entry.get()

    grossbuch.add_operation(
        operation_date,
        amount,
        description,
        category
    )

    day_entry.delete(0, "end")
    amount_entry.delete(0, "end")
    description_entry.delete(0, "end")
    category_entry.delete(0, "end")

    history_box.delete("1.0", "end")
    history_box.insert("end", grossbuch.text())
    history_box.see("end")

    day_entry.focus()


window = tk.CTk()
window.geometry("600x650")
window.title("Grossbuch Import")

tk.CTkLabel(window, text="Day").pack(pady=(10, 0))
day_entry = tk.CTkEntry(window)
day_entry.pack()

tk.CTkLabel(window, text="Amount").pack(pady=(10, 0))
amount_entry = tk.CTkEntry(window)
amount_entry.pack()

tk.CTkLabel(window, text="Description").pack(pady=(10, 0))
description_entry = tk.CTkEntry(window)
description_entry.pack()

tk.CTkLabel(window, text="Category").pack(pady=(10, 0))
category_entry = tk.CTkEntry(window)
category_entry.pack()

add_button = tk.CTkButton(
    window,
    text="Add operation",
    command=add_operation
)
add_button.pack(pady=20)

history_box = tk.CTkTextbox(window, width=550, height=300)
history_box.pack(fill="both", expand=True, padx=10, pady=10)

history_box.insert("end", grossbuch.text())
history_box.see("end")

window.bind("<Return>", lambda event: add_operation())

day_entry.focus()

window.mainloop()