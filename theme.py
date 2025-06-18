import tkinter as tk
from tkinter import ttk

def apply_theme(root, theme):
    
    if theme == "d":  
        bg_color = "#7F7F7F"
        fg_color = "#ffffff"
        entry_bg = "#3d3d3d"
        button_bg = "#4d4d4d"
        frame_bg = "#7F7F7F"
        combobox_bg = "#3d3d3d"
        combobox_fg = "#ffffff"
        combobox_field_bg = "#3d3d3d"
        combobox_arrow_color = "#ffffff"
        heading_bg = "#3d3d3d"
        heading_fg = "#ffffff"
        tree_bg = "#3d3d3d"
        tree_fg = "#ffffff"
        tree_selected_bg = "#5d5d5d"
        highlight_color = "#cccccc"
    else:  
        bg_color = "#f0f0f0"
        fg_color = "#000000"
        entry_bg = "#ffffff"
        button_bg = "#e0e0e0"
        frame_bg = "#e0e0e0"
        combobox_bg = "#ffffff"
        combobox_fg = "#000000"
        combobox_field_bg = "#ffffff"
        combobox_arrow_color = "#000000"
        heading_bg = "#e0e0e0"
        heading_fg = "#000000"
        tree_bg = "#ffffff"
        tree_fg = "#000000"
        tree_selected_bg = "#d0d0d0"
        highlight_color = "#cccccc"

    style = ttk.Style()
    
    style.theme_use('default') 
    
    style.configure('.', 
                   background=frame_bg,
                   foreground=fg_color,
                   fieldbackground=entry_bg,
                   selectbackground=highlight_color,
                   selectforeground=fg_color)
    
    style.configure('TFrame', background=frame_bg)
    style.configure('TLabel', background=frame_bg, foreground=fg_color)
    style.configure('TButton', 
                   background=button_bg, 
                   foreground=fg_color,
                   bordercolor=highlight_color,
                   focuscolor=highlight_color)
    style.configure('TEntry', 
                   fieldbackground=entry_bg,
                   foreground=fg_color,
                   insertcolor=fg_color)
    style.configure('TCombobox',
                   fieldbackground=combobox_field_bg,
                   background=combobox_bg,
                   foreground=combobox_fg,
                   arrowcolor=combobox_arrow_color)
    style.configure('Treeview',
                   background=tree_bg,
                   foreground=tree_fg,
                   fieldbackground=tree_bg)
    style.map('Treeview',
             background=[('selected', tree_selected_bg)])
    style.configure('Treeview.Heading',
                   background=heading_bg,
                   foreground=heading_fg)
    style.configure('Horizontal.TScrollbar',
                   background=button_bg,
                   troughcolor=frame_bg)
    style.configure('Vertical.TScrollbar',
                   background=button_bg,
                   troughcolor=frame_bg)

    root.config(bg=bg_color)
    
    def apply_to_widget(widget):
        try:
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.LabelFrame)):
                widget.config(bg=frame_bg if isinstance(widget, (tk.Label, tk.LabelFrame)) else entry_bg,
                            fg=fg_color)
                if isinstance(widget, tk.Button):
                    widget.config(activebackground=button_bg,
                                highlightbackground=highlight_color)
                if isinstance(widget, tk.Entry):
                    widget.config(insertbackground=fg_color,
                                selectbackground=highlight_color,
                                selectforeground=fg_color)
            
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=frame_bg)
            
            for child in widget.winfo_children():
                apply_to_widget(child)
                
        except Exception as e:
            print(f"Не удалось применить тему к виджету {widget}: {e}")
    
    apply_to_widget(root)