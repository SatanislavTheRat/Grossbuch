import customtkinter as tk
import tksheet


TABLE_STYLE = {
    "font": ("Georgia", 14, "normal"),
    "header_font": ("Georgia", 18, "bold"),

    "table_bg": "#2B2B2B",
    "table_fg": "#F5F1E8",
    "table_grid_fg": "#4A3A28",

    "header_bg": "#7A2F1D",
    "header_fg": "#F5F1E8",
    "header_border_fg": "#4A3A28",
    "header_grid_fg": "#4A3A28",

    "table_selected_cells_bg": "#50302A",
    "table_selected_cells_fg": "#F5F1E8",
    "table_selected_cells_border_fg": "#A13B22",

    "frame_bg": "#2B2B2B",
    "outline_color": "#4A3A28"
}


window = tk.CTk()
window.geometry("500x400")


center_frame = tk.CTkFrame(
    window,
    fg_color="transparent"
)

center_frame.grid(
    row=0,
    column=0,
    sticky="nsew"
)


# У center_frame:
# row 0 — label
# row 1 — таблиця заголовків
# row 2 — основна таблиця

center_frame.grid_rowconfigure(2, weight=1)
center_frame.grid_columnconfigure(0, weight=1)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


# Label

statistics_label = tk.CTkLabel(
    center_frame,
    text="Top Income for All categories:",
    font=("Georgia", 14)
)

statistics_label.grid(
    row=0,
    column=0,
    sticky="w"
)


# Таблиця заголовків

statistics_headers_sheet = tksheet.Sheet(
    center_frame,
    data=[
        ["Amount", "Description", "Category", "Date"]
    ],
    show_row_index=False,
    show_header=False,
    **TABLE_STYLE
)

statistics_headers_sheet.set_column_widths([
    80,
    180,
    120,
    100
])

statistics_headers_sheet.grid(
    row=1,
    column=0,
    sticky="ew"
)


# Основна таблиця

statistics_sheet = tksheet.Sheet(
    center_frame,
    data=[
        ["-50 €", "Snap button installation series", "Personal Access", "07.07.2026"],
        ["+5 120 €", "Financial support", "Family", "06.08.2026"],
        ["+2 560 €", "Financial support", "Family", "12.07.2026"],
        ["+2 560 €", "Financial support", "Family", "22.07.2026"]
    ],
    show_row_index=False,
    show_header=False,
    **TABLE_STYLE
)

statistics_sheet.set_column_widths([
    80,
    180,
    120,
    100
])

statistics_sheet.grid(
    row=2,
    column=0,
    sticky="nsew"
)


window.mainloop()