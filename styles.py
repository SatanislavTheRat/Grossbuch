font = "Georgia"

TITLE_FONT = (font, 18, "bold")

TEXT_FONT = (font, 14, "normal")

SMALL_FONT = (font, 11, "normal")

TABLE_FONT = (font, 10, "normal")

MONO_FONT = ("Courier New", 14, "bold")

ERROR_COLOR="#C35A5A"

ENTRY_STYLE = {
    "width": 135,
    "height": 32,
    "font": TEXT_FONT,
    "corner_radius": 8,
    "fg_color": "#2B2B2B",
    "border_width": 1,
    "border_color": "#5C6670",
    "text_color": "#F5F1E8",
}

ENTRY_DISABLED_STYLE = {
    "fg_color": "#2E2E2E",
    "border_width": 0,
    "text_color": "#E4DED2",
    "font": TEXT_FONT
}

SEARCH_ENTRY_STYLE = {
    "width": 200,
    "font": TEXT_FONT,
    "corner_radius": 8
}

BUTTON_STYLE = {
    "fg_color": "#7A2F1D",
    "hover_color": "#A13B22",
    "font": (font, 14, "bold"),
    "corner_radius": 8,
    "height": 34
}

SMALLER_BUTTON_STYLE = {
    "fg_color": "#7A2F1D",
    "hover_color": "#A13B22",
    "font": (font, 11),
    "corner_radius": 8,
    "height": 28,
    "width": 100
}

LIST_BUTTON_STYLE = {
    "fg_color": "transparent",
    "hover_color": "#50302A",
    "text_color": "#F5F1E8",
    "anchor": "w",
    "corner_radius": 6,
    "font": TEXT_FONT,
    "height": 28}

UNUSED_LIST_BUTTON_STYLE = {
    "fg_color": "transparent",
    "hover_color": "#4F3E37",
    "text_color": "#9A8E84",
    "font": (font, 14),
    "anchor": "w",
    "corner_radius": 6,
    "height": 28
}

RADIO_STYLE = {
    "fg_color": "#7A2F1D",
    "hover_color": "#A13B22",
    "font": (font, 15)
}

COMBOBOX_STYLE = {
    "width": 150,
    "height": 32,
    "font": TEXT_FONT,
    "corner_radius": 8,

    "border_color": "#4A3A28",

    "button_color": "#7A2F1D",
    "button_hover_color": "#A13B22",

    "dropdown_fg_color": "#2B2B2B",
    "dropdown_hover_color": "#50302A",

    "dropdown_text_color": "#F5F1E8",

    "text_color": "#F5F1E8"
}
###################################################################################################
DATE_ENTRY_STYLE = {
    "font": TEXT_FONT,
    "fieldbackground": "#2B2B2B",
    "foreground": "#F5F1E8",

    "background": "#7A2F1D",
    "arrowcolor": "#F5F1E8",

    "bordercolor": "#4A3A28",
    "lightcolor": "#4A3A28",
    "darkcolor": "#4A3A28",

    "padding": 4,
}

DATE_ENTRY_MAP = {
    "background": [
        ("active", "#7A2F1D"),
        ("pressed", "#7A2F1D"),
    ],
    "bordercolor": [
        ("active", "#4A3A28"),
        ("pressed", "#4A3A28"),
    ],
    "lightcolor": [
        ("active", "#7A2F1D"),
        ("pressed", "#7A2F1D"),
    ],
    "darkcolor": [
        ("active", "#7A2F1D"),
        ("pressed", "#7A2F1D"),
    ],
    "arrowcolor": [
        ("active", "#F5F1E8"),
        ("pressed", "#F5F1E8"),
    ],
}
####################################################################################################

PANEL_STYLE = {
    "corner_radius": 12,
    "border_width": 1,
    "border_color": "#4A3A28"
}

TAB_STYLE = {
    "segmented_button_fg_color": "#2B2B2B",
    "segmented_button_selected_color": "#8B3A22",
    "segmented_button_selected_hover_color": "#A54728",
    "segmented_button_unselected_color": "#3A3A3A",
    "segmented_button_unselected_hover_color": "#505050",
    "text_color": "#F5F1E8",
}

SCROLLABLE_FRAME_STYLE = {
    "corner_radius": 10,
    "border_width": 1,
    "border_color": "#4A3A28"
}

TABLE_STYLE = {
    "font": TABLE_FONT,
    "header_font": SMALL_FONT,

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
    "outline_color": "#4A3A28",

    "table_wrap": "w",

    "scrollbar_show_arrows": False,
    "vertical_scroll_background": "#2B2B2B",
    "horizontal_scroll_background": "#2B2B2B",
    "vertical_scroll_troughcolor": "#2B2B2B",
    "horizontal_scroll_troughcolor": "#2B2B2B",
    "vertical_scroll_not_active_bg": "#4A3A28",
    "horizontal_scroll_not_active_bg": "#4A3A28",
    "vertical_scroll_active_bg": "#7A2F1D",
    "horizontal_scroll_active_bg": "#7A2F1D",
    "vertical_scroll_pressed_bg": "#A13B22",
    "horizontal_scroll_pressed_bg": "#A13B22",
    "vertical_scroll_borderwidth": 0,
    "horizontal_scroll_borderwidth": 0,
    "vertical_scroll_relief": "flat",
    "horizontal_scroll_relief": "flat",
}

TABLE_HEADER_STYLE = {
    "font": SMALL_FONT,
    "header_font": SMALL_FONT,

    "table_bg": "#2B2B2B",
    "table_fg": "#F5F1E8",
    "table_grid_fg": "#A13B22",

    "align": "center",

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

