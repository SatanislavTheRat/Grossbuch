import customtkinter as tk
from datetime import date
from PIL import Image
from Grossbuch import Grossbuch
from styles import *

HISTORY_FILE = "history.json"
CATEGORIES_FILE = "categories.json"

grossbuch=Grossbuch(HISTORY_FILE,CATEGORIES_FILE)

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
    tabs.set("Statistics")
    operation_date = date.today()

    amount = int(amount_entry.get())
    if operation_type.get() == "expense":
        amount = -amount

    description = description_entry.get()
    category = category_entry.get()

    grossbuch.add_operation(operation_date, amount, description, category)

    amount_entry.delete(0, "end")
    description_entry.delete(0, "end")
    category_entry.delete(0, "end")
    category_search_entry.configure(state="normal")
    category_search_entry.delete(0, "end")
    add_operation_button.configure(state="disabled")
    history_box.delete("1.0", "end")
    history_box.insert("1.0", grossbuch.text())
    history_box.see("end")
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
    for category in grossbuch.categories:
        if category.startswith(text):
            show_category(category)

def choose_category(category):
    category_search_entry.configure(state="normal")
    category_search_entry.delete(0, "end")
    category_search_entry.insert(0, category)
    category_entry.delete(0, "end")
    category_entry.insert(0, category)
    add_category_button.configure(state="disabled")
    check_fields()
    category_search_entry.configure(state="disabled")

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
    grossbuch_window.update_idletasks()
    categories_frame._parent_canvas.yview_moveto(1.0)

def synchronize_category_search_entry(event):
    tabs.set("Categories")
    text = category_entry.get()
    category_search_entry.configure(state="normal")
    category_search_entry.delete(0, "end")
    if text.strip():
        category_search_entry.insert(0, text)
        category_search_entry.configure(state="disabled")
    update_categories()

def check_rename_button(event=None):
    if (
        category_search_entry.get().strip()
        and rename_category_entry.get().strip()
    ):
        rename_category_button.configure(state="normal")
    else:
        rename_category_button.configure(state="disabled")

def rename_category():
    old=category_search_entry.get()
    new=rename_category_entry.get()
    grossbuch.rename_category(old,new)
    update_all()

def delete_category():
    category = category_search_entry.get()
    grossbuch.delete_category(category)
    category_search_entry.configure(state="normal")
    category_search_entry.delete(0, "end")
    category_entry.delete(0, "end")
    delete_category_button.configure(state="disabled")
    update_categories()
    categories_frame.update_idletasks()
    categories_frame._parent_canvas.yview_moveto(0)

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
    category_entry.configure(state="disabled")
    category_search_entry.configure(state="disabled")
    for category in grossbuch.categories:
        if category == merged_category:
            pass
        else:
            button = tk.CTkButton(categories_frame, text=category, **LIST_BUTTON_STYLE,
                                  command=lambda c=category: merge_into(c))
            button.grid()
    categories_frame.update_idletasks()
    categories_frame._parent_canvas.yview_moveto(0.0)

def update_all():
    update_entries()
    update_categories()

def merge_into(new):
    old = category_search_entry.get()
    grossbuch.merge_categories(old,new)
    update_all()



def update_entries():
    rename_category_entry.delete(0, "end")
    category_search_entry.configure(state="normal")
    category_search_entry.delete(0, "end")
    category_entry.configure(state="normal")
    category_entry.delete(0, "end")
    history_box.delete("1.0", "end")
    history_box.insert("1.0", grossbuch.text())
    categories_frame_clear_up()



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^CATEGORIES^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

grossbuch_window.geometry("700x750")
grossbuch_window.title("Grossbuch")
grossbuch_window.resizable(False, False)

logo = tk.CTkImage(light_image=Image.open("logo.png"),size=(700, 196))
logo_label = tk.CTkLabel(grossbuch_window,text="",image=logo)
logo_label.grid(row=0,column=0, columnspan = 2, sticky="EW",)

date_label=tk.CTkLabel(grossbuch_window,text=date.today().strftime("%d.%m.%Y, %A"), font=TEXT_FONT)
date_label.grid(row=1,columnspan = 2,padx=50,pady=(10,5),sticky="WE")

main_frame = tk.CTkFrame(grossbuch_window,**PANEL_STYLE)
main_frame.grid(row=2,column=0,columnspan=2,padx=15,pady=10,sticky="ew")

#############################----LEFT PANEL-----###################################

main_frame.grid_columnconfigure(0, weight=1)
left_frame = tk.CTkFrame(main_frame, width=250, height=400,**PANEL_STYLE)
left_frame.grid(row=0,column=0,padx=(0, 10),sticky="EW")
left_frame.grid_propagate(False)

title_label = tk.CTkLabel(left_frame,text="New record", font=TITLE_FONT)
title_label.grid(row=0,columnspan=2, pady=(25,10))


operation_type = tk.StringVar(value="expense")
income_radio = tk.CTkRadioButton(left_frame,text="Income", variable=operation_type,value="income",
                                 **RADIO_STYLE)
expense_radio = tk.CTkRadioButton(left_frame,text="Expense",variable=operation_type,value="expense",
                                  **RADIO_STYLE)
income_radio.grid(row=1, column=0, padx=(40,15), pady=10)
expense_radio.grid(row=1, column=1, padx=40, pady=10)


amount_error_label = tk.CTkLabel(left_frame,text = "", text_color="red", font=SMALL_FONT)
amount_error_label.grid(row=2,columnspan=2, pady = (0,0))


amount_label = tk.CTkLabel(left_frame,text = "Amount:",font=TEXT_FONT)
amount_label.grid(row=3,column=0)
amount_entry = tk.CTkEntry(left_frame, **ENTRY_STYLE)
amount_entry.grid(row=3,column=1, pady=(0,15),sticky="w")
amount_entry.bind("<KeyRelease>", check_fields)


description_label = tk.CTkLabel(left_frame,text="Description:",font=TEXT_FONT)
description_label.grid(row=4,column=0)
description_entry = tk.CTkEntry(left_frame,**ENTRY_STYLE)
description_entry.grid(row=4,column=1, pady=15, sticky="w")
description_entry.bind("<KeyRelease>", check_fields)


category_label = tk.CTkLabel(left_frame,text="Category:",font=TEXT_FONT)
category_label.grid(row=5,column=0)
category_entry = tk.CTkEntry(left_frame,**ENTRY_STYLE)
category_entry.grid(row=5,column=1, pady=15, sticky="w")
category_entry.bind("<KeyRelease>", check_fields)
category_entry.bind("<KeyRelease>", update_categories)
category_entry.bind("<KeyRelease>", synchronize_category_search_entry)

add_operation_button = tk.CTkButton(left_frame,text="Add to Grossbuch", **BUTTON_STYLE,
                                    state="disabled", command=add_operation)
add_operation_button.grid(row=6,columnspan=2,pady = (30,15))

#############################----RIGHT PANEL-----###################################

main_frame.grid_columnconfigure(1, weight=1)
right_frame = tk.CTkFrame(main_frame, width=250, height=400, **PANEL_STYLE)
right_frame.grid(row=0,column=1,padx=(10, 0), sticky="EW")
right_frame.grid_propagate(False)

tabs = tk.CTkTabview(right_frame, **TAB_STYLE)
tabs.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

tabs.add("Categories")
tabs.add("Statistics")

##########################################----CATEGORIES------####################################

categories_tab = tabs.tab("Categories")

category_search_entry = tk.CTkEntry(categories_tab,**ENTRY_STYLE,state="normal")
category_search_entry.grid(row=0,column=0,padx=(10,5),pady=5)
category_search_entry.bind("<KeyRelease>", update_categories)


add_category_button = tk.CTkButton(categories_tab,text="Add", **BUTTON_STYLE, state="disabled",
                                   command=add_category)
add_category_button.grid(row=0,column=1,padx=(5,10), pady=5, sticky="nsew")

categories_tab.grid_columnconfigure(0, weight=1)
categories_tab.grid_columnconfigure(1, weight=0)
categories_tab.grid_rowconfigure(1, weight=1)
categories_frame=tk.CTkScrollableFrame(categories_tab, **SCROLLABLE_FRAME_STYLE)
categories_frame.grid(row=1,column=0,columnspan=2,sticky="NSEW")
update_categories()

##################################     DELETE MERGE RENAME     ################################################

rename_category_button=tk.CTkButton(categories_tab, text = "Rename:", **BUTTON_STYLE, state="disabled",
                                    command=rename_category)
rename_category_button.grid(row=2,column=0, pady=(5,5))


rename_category_entry = tk.CTkEntry(categories_tab, **ENTRY_STYLE)
rename_category_entry.grid(row=2,column=1, pady=(5,5))
rename_category_entry.bind("<KeyRelease>", check_rename_button)

delete_category_button=tk.CTkButton(categories_tab,text="Delete", **BUTTON_STYLE, state="disabled",
                                    command=delete_category)
delete_category_button.grid(row=3,column=0, pady=(5,0))


merge_with_button=tk.CTkButton(categories_tab,text="Merge into...", **BUTTON_STYLE,state="disabled",
                                   command=merge_mode)
merge_with_button.grid(row=3,column=1, pady=(5,0))

##########################################-----------STATISTICS-----------------#####################

statistics_tab = tabs.tab("Statistics")
statistics_tab.grid_columnconfigure(0, weight=1)
statistics_tab.grid_rowconfigure(0, weight=1)
history_box = tk.CTkTextbox(statistics_tab, font=TEXT_FONT, **PANEL_STYLE)
history_box.grid(row=0,column=0, sticky="nsew")
history_box.insert("end", grossbuch.text())

#################################################################################

balance_label=tk.CTkLabel(grossbuch_window,text=f"Balance = {grossbuch.balance} UAH",font=TITLE_FONT)
balance_label.grid(row=3, sticky="N", columnspan = 2)

reconcile_button=tk.CTkButton(grossbuch_window, text="Reconcile", **BUTTON_STYLE, state="disabled", command=reconcile)
reconcile_button.grid(row=4,column=0, padx=(160,5), pady=(5,0), sticky = "e")
reconcile_entry = tk.CTkEntry(grossbuch_window, **ENTRY_STYLE)
reconcile_entry.grid(row=4,column=1, padx=(5,160), pady=(5,0), sticky="w")
reconcile_entry.bind("<KeyRelease>", reconcile_entry_check)
reconcile_error_label=tk.CTkLabel(grossbuch_window,text="",font=SMALL_FONT, text_color="red")
reconcile_error_label.grid(row=5, column=1, padx=(5,100), sticky="W")

grossbuch_window.mainloop()