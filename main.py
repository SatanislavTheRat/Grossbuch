import customtkinter as tk
from datetime import date
from PIL import Image
from tkcalendar import DateEntry
from tkinter import ttk
import tksheet

from grossbuch import Grossbuch
from database import Database
from styles import *

DATABASE_FILE = "grossbuch.db"
BACKUP_PATH = "backups"

db = Database(DATABASE_FILE)
grossbuch=Grossbuch(db)

def lock_entry(entry):
    entry.configure(**ENTRY_DISABLED_STYLE)
    entry.configure(state="disabled")
def unlock_entry(entry):
    entry.configure(state="normal")
    entry.configure(**ENTRY_STYLE)

def validate_amount():
    text = amount_entry.get()
    if not text:
        amount_error_label.configure(text="")
        return False
    try:
        float(amount_entry.get())
        amount_error_label.configure(text="")
        return True
    except ValueError:
        amount_error_label.configure(text="*Amount must be a number!")
        return False

def check_fields(event=None):
    if (
            validate_amount()
            and amount_entry.get()
            and description_entry.get().strip()
            and category_entry.get().strip()
            and category_entry.get().strip().capitalize() in grossbuch.categories):
        add_operation_button.configure(state="normal")
    else:
        add_operation_button.configure(state="disabled")

def add_operation():
    tabs.set("Grossbuch")
    operation_date = date.today()

    amount = int(amount_entry.get())
    if operation_type.get() == "expense":
        amount = -amount

    description = description_entry.get().strip().capitalize()
    category = category_entry.get().strip().capitalize()

    grossbuch.add_operation(amount, description, category, operation_date)

    amount_entry.delete(0, "end")
    description_entry.delete(0, "end")
    category_entry.delete(0, "end")
    unlock_entry(category_search_entry)
    category_search_entry.delete(0, "end")
    add_operation_button.configure(state="disabled")
    show_grossbuch()
    balance_label.configure(text=f"Balance = {grossbuch.balance} UAH")
    update_categories()



def show_category(category):
    if grossbuch.is_used(category):
        button = tk.CTkButton(categories_frame, text=category,**LIST_BUTTON_STYLE,
                            command=lambda c=category: choose_category(c) )
    else:
        button = tk.CTkButton(categories_frame, text=category, **UNUSED_LIST_BUTTON_STYLE,
                              command=lambda c=category: choose_category(c))
    button.grid()

def update_categories(event=None):
    categories_frame_clear_up()
    text = category_search_entry.get().capitalize()
    if not text:
        add_category_button.configure(state="disabled")
    elif text in grossbuch.categories:
        add_category_button.configure(state="disabled")
    else:
        add_category_button.configure(state="normal")
    for widget in categories_frame.winfo_children():
        widget.destroy()
    for category in sorted(grossbuch.categories):
        if category.startswith(text):
            show_category(category)
    category_box.configure(values=sorted(grossbuch.categories))
    category_box.set("All categories")

def choose_category(category):
    unlock_entry(category_search_entry)
    category_search_entry.delete(0, "end")
    category_search_entry.insert(0, category)
    category_entry.delete(0, "end")
    category_entry.insert(0, category)
    add_category_button.configure(state="disabled")
    check_fields()
    lock_entry(category_search_entry)

    if grossbuch.is_used(category):
        delete_category_button.configure(state="disabled")
    else:
        delete_category_button.configure(state="normal")

    if not amount_entry.get() and not description_entry.get():
        merge_with_button.configure(state="normal")

    check_rename_button()

def add_category():
    category=category_search_entry.get().capitalize()
    grossbuch.add_category(category)
    category_search_entry.delete(0, "end")
    update_categories()
    categories_frame_clear_up()
    check_fields()

def synchronize_category_search_entry(event):
    tabs.set("Categories")
    text = category_entry.get().capitalize()
    unlock_entry(category_search_entry)
    category_search_entry.delete(0, "end")
    if text.strip():
        category_search_entry.insert(0, text)
        lock_entry(category_search_entry)
    update_categories()

def check_rename_button(event=None):
    if (
        category_search_entry.get().strip()
        and rename_category_entry.get().strip()
        and rename_category_entry.get().strip().capitalize() not in grossbuch.categories
    ):
        rename_category_button.configure(state="normal")
    else:
        rename_category_button.configure(state="disabled")

def rename_category():
    old=category_search_entry.get()
    new=rename_category_entry.get().strip().capitalize()
    grossbuch.rename_category(old,new)
    update_all()

def delete_category():
    category = category_search_entry.get()
    grossbuch.delete_category(category)
    unlock_entry(category_search_entry)
    category_search_entry.delete(0, "end")
    category_entry.delete(0, "end")
    delete_category_button.configure(state="disabled")
    update_categories()
    categories_frame_clear_up()


def categories_frame_clear_up():
    categories_frame.update_idletasks()
    categories_frame._parent_canvas.yview_moveto(0.0)

def merge_mode():
    merged_category = category_search_entry.get()
    for widget in categories_frame.winfo_children():
        widget.destroy()
    label = tk.CTkLabel(categories_frame, text=f"Merge '{merged_category}' into:", font = TEXT_FONT)
    label.grid()
    cancel_button=tk.CTkButton(categories_frame, text="Cancel", **SMALLER_BUTTON_STYLE, command=update_all)
    cancel_button.grid()
    merge_with_button.configure(state="disabled")
    lock_entry(category_entry)
    lock_entry(category_search_entry)
    for category in grossbuch.categories:
        if category == merged_category:
            pass
        else:
            button = tk.CTkButton(categories_frame, text=category, **LIST_BUTTON_STYLE,
                                  command=lambda c=category: merge_into(c))
            button.grid()
    categories_frame.update_idletasks()
    categories_frame._parent_canvas.yview_moveto(0.0)

def refresh_grossbuch_sheet():
    grossbuch_sheet.set_sheet_data(
        grossbuch.text_list(),
        reset_col_positions=False
    )
    grossbuch_sheet.row_height(
        row="all",
        height="text"
    )
    grossbuch_sheet.refresh()

def update_all():
    update_entries()
    update_categories()
    refresh_grossbuch_sheet()


def merge_into(new):
    old = category_search_entry.get()
    grossbuch.merge_categories(old,new)
    update_all()

def update_entries():
    rename_category_entry.delete(0, "end")
    unlock_entry(category_search_entry)
    category_search_entry.delete(0, "end")
    unlock_entry(category_entry)
    category_entry.delete(0, "end")
    categories_frame_clear_up()



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^CATEGORIES^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
############################-----------STATISTICS--------------------#############################

def get_summary():
    operations_list = grossbuch.filter_by_date(from_date_box.get_date(),to_date_box.get_date(),grossbuch.history)
    if category_box.get() != "All categories":
        return grossbuch.calculate_summary (grossbuch.filter_by_category(category_box.get(),operations_list))
    return grossbuch.calculate_summary(operations_list)

def get_top_income():
    if category_box.get() == "All categories":
        operations_list = grossbuch.filter_by_date(from_date_box.get_date(),to_date_box.get_date(),grossbuch.history)
    else:
        operations_list = grossbuch.filter_by_category(category_box.get(),
        (grossbuch.filter_by_date(from_date_box.get_date(), to_date_box.get_date(), grossbuch.history)))

    operations_list = [operation for operation in operations_list if operation.amount > 0]
    return grossbuch.sort_by_amount(operations_list,reverse=True)

def get_top_expenses():
    if category_box.get() == "All categories":
        operations_list = grossbuch.filter_by_date(from_date_box.get_date(), to_date_box.get_date(), grossbuch.history)
    else:
        operations_list = grossbuch.filter_by_category(category_box.get(),
        (grossbuch.filter_by_date(from_date_box.get_date(),to_date_box.get_date(),grossbuch.history)))

    operations_list = [operation for operation in operations_list if operation.amount < 0]
    return grossbuch.sort_by_amount(operations_list)

def get_top_income_by_category():
    result=[]
    for key,value in grossbuch.top_income_by_category(from_date_box.get_date(),to_date_box.get_date()):
        result.append([key,value[0],value[1]])
    return result

def get_top_expenses_by_category():
    result=[]
    for key,value in grossbuch.top_expenses_by_category(from_date_box.get_date(),to_date_box.get_date()):
        result.append([key,value[0],value[1]])
    return result

def show_summary():
    statistics_headers_sheet.set_sheet_data([[f"Summary for {category_box.get().lower()}\n"
                                              f"from {from_date_box.get()} to {to_date_box.get()}"]])
    statistics_headers_sheet.set_column_widths([370])
    statistics_headers_sheet.refresh()
    statistics_headers_sheet.row_height(row="all",height="text")
    statistics_headers_sheet.height_and_width(height=statistics_headers_sheet.get_row_heights(0)[0] + 1)

    statistics_sheet.set_sheet_data([
            ["Income:", f"{get_summary()["income"]:,} ₴".replace(",", " ")],
            ["Expenses:", f"{get_summary()["expenses"]:,} ₴".replace(",", " ")],
            ["Balance:", f"{get_summary()["balance"]:,} ₴".replace(",", " ")],
            ["Records:", f"{get_summary()["records"]}"]
        ],reset_col_positions=False)
    statistics_sheet.set_column_widths([150,100])
    statistics_sheet.refresh()

def show_top_income():
    if statistics_type.get() == "operation":
        statistics_headers_sheet.set_sheet_data([["Date","Operation","Category","Amount"]],reset_col_positions=False)
        statistics_headers_sheet.set_column_widths([82,108,108,70])
        statistics_headers_sheet.refresh()

        content=[]
        for operation in get_top_income():
            content.append([operation.date.strftime('%d.%m.%Y'),
                            operation.description,
                            operation.category,
                            f"{operation.amount:,} ₴".replace(",", " ")])

        statistics_sheet.set_sheet_data(content, reset_col_positions=False)
        statistics_sheet.set_column_widths([82, 108, 108, 70])
        statistics_sheet.row_height(
            row="all",
            height="text" )
        statistics_headers_sheet.height_and_width(height=statistics_headers_sheet.get_row_heights(0)[0] + 1)
        statistics_sheet.refresh()
    else:
        statistics_headers_sheet.set_sheet_data([["Category", "Amount", "Operations"]],
                                                reset_col_positions=False)
        statistics_headers_sheet.set_column_widths([170,108,95])

        statistics_headers_sheet.refresh()
        statistics_sheet.set_sheet_data(get_top_income_by_category(), reset_col_positions=False)
        statistics_sheet.set_column_widths([170,108,95])
        statistics_sheet.row_height(
            row="all",
            height="text")
        statistics_headers_sheet.height_and_width(height=statistics_headers_sheet.get_row_heights(0)[0] + 1)
        statistics_sheet.refresh()


def show_top_expenses():
    if statistics_type.get() == "operation":
        statistics_headers_sheet.set_sheet_data([["Date","Operation","Category","Amount"]],reset_col_positions=False)
        statistics_headers_sheet.set_column_widths([82,108,108,70])
        statistics_headers_sheet.refresh()

        content=[]
        for operation in get_top_expenses():
            content.append([operation.date.strftime('%d.%m.%Y'),
                            operation.description,
                            operation.category,
                            f"{operation.amount:,} ₴".replace(",", " ")])

        statistics_sheet.set_sheet_data(content, reset_col_positions=False)
        statistics_sheet.set_column_widths([82, 108, 108, 70])
        statistics_sheet.row_height(
            row="all",
            height="text" )
        statistics_headers_sheet.height_and_width(height=statistics_headers_sheet.get_row_heights(0)[0] + 1)
        statistics_sheet.refresh()
    else:
        statistics_headers_sheet.set_sheet_data([["Category", "Amount", "Operations"]],
                                                reset_col_positions=False)
        statistics_headers_sheet.set_column_widths([170,108,95])

        statistics_headers_sheet.refresh()
        statistics_sheet.set_sheet_data(get_top_expenses_by_category(), reset_col_positions=False)
        statistics_sheet.set_column_widths([170,108,95])
        statistics_sheet.row_height(
            row="all",
            height="text")
        statistics_headers_sheet.height_and_width(height=statistics_headers_sheet.get_row_heights(0)[0] + 1)
        statistics_sheet.refresh()



def show_grossbuch():
    grossbuch_sheet.set_sheet_data(grossbuch.text_list(), reset_col_positions=False)
    grossbuch_sheet.set_column_widths([383])
    grossbuch_sheet.row_height(row="all", height="text")
    grossbuch_sheet.see(grossbuch_sheet.get_total_rows() - 1, 0)
    grossbuch_sheet.refresh()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^STATISTICS^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def reconcile_entry_check(event=None):
    text = reconcile_entry.get()
    if not text:
        reconcile_error_label.configure(text="")
        reconcile_button.configure(state="disabled")
        return
    try:
        value = int(text)
    except ValueError:
        reconcile_error_label.configure(text="*Please enter a correct number!")
        reconcile_button.configure(state="disabled")
        return
    reconcile_error_label.configure(text="")
    if value != grossbuch.balance:
        reconcile_button.configure(state="normal")
    else:
        reconcile_button.configure(state="disabled")

def reconcile():
    correction=int(reconcile_entry.get()) - grossbuch.balance
    if correction>0:
        operation_type.set("income")
        description_entry.delete(0, "end")
        description_entry.insert(0, "Balance adjustment (+)")
    else:
        operation_type.set("expense")
        description_entry.delete(0, "end")
        description_entry.insert(0, "Balance adjustment (-)")
    amount_entry.delete(0, "end")
    amount_entry.insert(0, abs(correction))
    category_entry.delete(0, "end")
    category_entry.insert(0, "Reconciliation")
    category_search_entry.delete(0, "end")
    category_search_entry.insert(0, "Reconciliation")
    update_categories()
    add_operation_button.configure(state="normal")
    reconcile_entry.delete(0, "end")


#####################################################################################################
######################################################################################################
#####################################################################################################


grossbuch_window = tk.CTk()
grossbuch_window.iconbitmap("icon.ico")

grossbuch_window.geometry("850x770")
grossbuch_window.title("Grossbuch")
grossbuch_window.resizable(False, False)

logo = tk.CTkImage(light_image=Image.open("logo.png"),size=(850, 225))
logo_label = tk.CTkLabel(grossbuch_window,text="",image=logo)
logo_label.grid(row=0,column=0, columnspan = 2, sticky="EW",)



main_frame = tk.CTkFrame(grossbuch_window,**PANEL_STYLE)
main_frame.grid(row=1,column=0,columnspan=2,padx=8,pady=15,sticky="ew")
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
#############################----LEFT PANEL-----###################################


left_frame = tk.CTkFrame(main_frame, width=400, height=490,**PANEL_STYLE)
left_frame.grid(row=0,column=0,padx=(0, 10),sticky="EW")
left_frame.grid_propagate(False)


title_label = tk.CTkLabel(left_frame,text="New record", font=TITLE_FONT)
title_label.grid(row=0,columnspan=2, pady=(15,10), padx = 150)


operation_type = tk.StringVar(value="expense")
income_radio = tk.CTkRadioButton(left_frame,text="Income", variable=operation_type,value="income",
                                 **RADIO_STYLE)
expense_radio = tk.CTkRadioButton(left_frame,text="Expense",variable=operation_type,value="expense",
                                  **RADIO_STYLE)
income_radio.grid(row=1, column=0, padx=(30,15), pady=(15,5))
expense_radio.grid(row=1, column=1, padx=(20,15), pady=(15,5))


amount_error_label = tk.CTkLabel(left_frame,text = "", text_color=ERROR_COLOR, font=SMALL_FONT)
amount_error_label.grid(row=2,column=1, pady = (0,0), padx = (0,0))

date_word_label=tk.CTkLabel(left_frame,text="Date:",font=TEXT_FONT)
date_word_label.grid(row=3,column=0, sticky = "EW")

amount_label = tk.CTkLabel(left_frame,text = "Amount:",font=TEXT_FONT)
amount_label.grid(row=3,column=1)


date_label=tk.CTkLabel(left_frame,text=date.today().strftime("%d.%m.%Y, %A"), font=TEXT_FONT)
date_label.grid(row=4,column = 0)

amount_entry = tk.CTkEntry(left_frame, **ENTRY_STYLE)
amount_entry.grid(row=4,column=1)
amount_entry.bind("<KeyRelease>", check_fields)


description_label = tk.CTkLabel(left_frame,text="Description:",font=TEXT_FONT)
description_label.grid(row=5,column=0,pady=(15,0))

category_label = tk.CTkLabel(left_frame,text="Category:",font=TEXT_FONT)
category_label.grid(row=5,column=1,pady=(15,0))


description_entry = tk.CTkEntry(left_frame,**ENTRY_STYLE)
description_entry.grid(row=6,column=0)
description_entry.bind("<KeyRelease>", check_fields)

category_entry = tk.CTkEntry(left_frame,**ENTRY_STYLE)
category_entry.grid(row=6,column=1)
category_entry.bind("<KeyRelease>", check_fields)
category_entry.bind("<KeyRelease>", update_categories)
category_entry.bind("<KeyRelease>", synchronize_category_search_entry)


add_operation_button = tk.CTkButton(left_frame,text="Add to Grossbuch", **BUTTON_STYLE,
                                    state="disabled", command=add_operation)
add_operation_button.grid(row=7,columnspan=2,pady = (30,40))

balance_label=tk.CTkLabel(left_frame,text=f"Balance = {grossbuch.balance} ₴",font=TITLE_FONT)
balance_label.grid(row=8, columnspan = 2,pady = (15,15))

reconcile_button=tk.CTkButton(left_frame, text="Reconcile", **BUTTON_STYLE, state="disabled", command=reconcile)
reconcile_button.grid(row=9,column=0)
reconcile_entry = tk.CTkEntry(left_frame, **ENTRY_STYLE)
reconcile_entry.grid(row=9,column=1)
reconcile_entry.bind("<KeyRelease>", reconcile_entry_check)
reconcile_error_label=tk.CTkLabel(left_frame,text="",font=SMALL_FONT, text_color=ERROR_COLOR)
reconcile_error_label.grid(row=10, columnspan=2)

#############################----RIGHT PANEL-----###################################


right_frame = tk.CTkFrame(main_frame, width=400, height=490, **PANEL_STYLE)
right_frame.grid(row=0,column=1,padx=(10, 0), sticky="EW")
right_frame.grid_propagate(False)

tabs = tk.CTkTabview(right_frame, **TAB_STYLE)
tabs.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

tabs.add("Categories")
tabs.add("Statistics")
tabs.add("Grossbuch")
tabs.set("Grossbuch")


##########################################----CATEGORIES------####################################

categories_tab = tabs.tab("Categories")

category_search_entry = tk.CTkEntry(categories_tab,**ENTRY_STYLE,state="normal")
category_search_entry.grid(row=0,column=0,padx=(0,10),pady=5)
category_search_entry.bind("<KeyRelease>", update_categories)


add_category_button = tk.CTkButton(categories_tab,text="Add new", **BUTTON_STYLE, state="disabled",
                                   command=add_category)
add_category_button.grid(row=0,column=1,padx=(15,30), pady=5, sticky="nsew")

categories_tab.grid_columnconfigure(0, weight=1)
categories_tab.grid_columnconfigure(1, weight=0)
categories_tab.grid_rowconfigure(1, weight=1)
categories_frame=tk.CTkScrollableFrame(categories_tab, **SCROLLABLE_FRAME_STYLE)
categories_frame.grid(row=1,column=0,columnspan=2,sticky="NSEW")


##                                DELETE MERGE RENAME                                        ##

rename_category_button=tk.CTkButton(categories_tab, text = "Rename to...", **BUTTON_STYLE, state="disabled",
                                    command=rename_category)
rename_category_button.grid(row=2,column=0, pady=(0,0))


rename_category_entry = tk.CTkEntry(categories_tab, **ENTRY_STYLE, placeholder_text = "Add new name first")
rename_category_entry.grid(row=2,column=1, pady=5)
rename_category_entry.bind("<KeyRelease>", check_rename_button)

delete_category_button=tk.CTkButton(categories_tab,text="Delete", **BUTTON_STYLE, state="disabled",
                                    command=delete_category)
delete_category_button.grid(row=3,column=0, pady=(5,0))


merge_with_button=tk.CTkButton(categories_tab,text="Merge into...", **BUTTON_STYLE,state="disabled",
                                   command=merge_mode)
merge_with_button.grid(row=3,column=1, pady=(5,0))

##########################################-----------STATISTICS TAB-----------------#####################
statistics_tab = tabs.tab("Statistics")

statistics_tab.grid_rowconfigure(1, weight=1)
statistics_tab.grid_columnconfigure(0, weight=1)

# ==========================
# Upper panel
# ==========================
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Grossbuch.DateEntry",
    **DATE_ENTRY_STYLE
)

style.map(
    "Grossbuch.DateEntry",
    **DATE_ENTRY_MAP
)

top_frame = tk.CTkFrame(statistics_tab, fg_color="transparent")
top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

top_frame.grid_columnconfigure(0, weight=0)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)

# Category
category_label = tk.CTkLabel(
    top_frame,
    text="Category:",
    font=TEXT_FONT
)
category_label.grid(
    row=0,
    column=0,
    padx=(3, 5),
    pady=(0, 5),
    sticky="w"
)

categories = ["All categories"] + sorted(grossbuch.categories)

category_box = tk.CTkComboBox(
    top_frame,
    values=categories,
    **COMBOBOX_STYLE
)
category_box.grid(
    row=0,
    column=1,
    columnspan=2,
    padx=(0, 3),
    pady=(0, 5),
    sticky="ew"
)
category_box.set("All categories")


# Dates
from_date_label = tk.CTkLabel(
    top_frame,
    text="From:",
    font=TEXT_FONT
)
from_date_label.grid(
    row=1,
    column=0,
    padx=3,
    pady=(0, 5),
    sticky="e"
)

from_date_box = DateEntry(
    top_frame,
    mindate=grossbuch.first_date(),
    maxdate=date.today(),
    date_pattern="dd.mm.yyyy",
    style="Grossbuch.DateEntry",
    width=20
)
from_date_box.set_date(grossbuch.first_date())
from_date_box.grid(
    row=1,
    column=1,
    padx=3,
    pady=(0, 5),
    sticky="ew"
)

to_date_label = tk.CTkLabel(
    top_frame,
    text="To:",
    font=TEXT_FONT
)
to_date_label.grid(
    row=1,
    column=2,
    padx=3,
    pady=(0, 5),
    sticky="w"
)

to_date_box = DateEntry(
    top_frame,
    mindate=grossbuch.first_date(),
    maxdate=date.today(),
    date_pattern="dd.mm.yyyy",
    style="Grossbuch.DateEntry",
    width=20
)
to_date_box.set_date(date.today())
to_date_box.grid(
    row=1,
    column=2,
    padx=(35, 3),
    pady=(0, 5),
    sticky="e"
)

statistics_type = tk.StringVar(value="category")
category_radio = tk.CTkRadioButton(top_frame,text="Category", variable=statistics_type,value="category",
                                 **RADIO_STYLE)
operation_radio = tk.CTkRadioButton(top_frame,text="Operation",variable=statistics_type,value="operation",
                                  **RADIO_STYLE)
category_radio.grid(row=2, column=0, padx=(30,15), pady=2)
operation_radio.grid(row=2, column=1, columnspan = 2, padx=(20,15), pady=2)


###################################################################################################################
######################################################## Central panel         #######################################
#################################################################################################################
center_frame = tk.CTkFrame(
    statistics_tab,
    fg_color="transparent"
)

center_frame.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=5
)


center_frame.grid_columnconfigure(0, weight=1)


statistics_headers_sheet = tksheet.Sheet(
    center_frame,
    show_row_index=False,
    show_header=False,
    show_y_scrollbar=False,
    show_x_scrollbar=False,
    **TABLE_HEADER_STYLE)

statistics_headers_sheet.grid(
    row=0,
    column=0,
    sticky="ew"
)

statistics_sheet = tksheet.Sheet(
    center_frame,
    show_row_index=False,
    show_header=False,
    show_y_scrollbar=True,
    show_x_scrollbar=False,
    **TABLE_STYLE)

statistics_sheet.grid(row=1,column=0)

# ==========================
# Lower panel
# ==========================

bottom_frame = tk.CTkFrame(
    statistics_tab,
    fg_color="transparent"
)
bottom_frame.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=5,
    pady=5
)

bottom_frame.grid_columnconfigure(
    (0, 1, 2),
    weight=1
)

summary_button = tk.CTkButton(
    bottom_frame,
    text="Summary",
    **SMALLER_BUTTON_STYLE,
    command=show_summary
)
summary_button.grid(
    row=0,
    column=0,
    padx=3,
    sticky="ew"
)

top_expenses_button = tk.CTkButton(
    bottom_frame,
    text="Top Expenses",
    **SMALLER_BUTTON_STYLE,
    command=show_top_expenses
)
top_expenses_button.grid(
    row=0,
    column=1,
    padx=3,
    sticky="ew"
)

top_income_button = tk.CTkButton(
    bottom_frame,
    text="Top Income",
    **SMALLER_BUTTON_STYLE,
    command=show_top_income
)
top_income_button.grid(
    row=0,
    column=2,
    padx=3,
    sticky="ew"
)

############################------------GROSSBUCH------------##########################################
grossbuch_tab = tabs.tab("Grossbuch")
grossbuch_tab.grid_rowconfigure(0, weight=1)
grossbuch_tab.grid_columnconfigure(0, weight=1)

grossbuch_sheet = tksheet.Sheet(
    grossbuch_tab,
    show_row_index=False,
    show_header=False,
    show_y_scrollbar=False,
    show_x_scrollbar=False,
    **TABLE_HEADER_STYLE)

grossbuch_sheet.grid(row=0, column=0, sticky="nsew")

#################################################################################
update_categories()
show_grossbuch()
grossbuch_window.mainloop()