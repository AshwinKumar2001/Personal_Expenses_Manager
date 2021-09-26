# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:02:03 2021

@author: AVITA
"""


import tkinter as tk                # python 3
from tkinter import font as tkfont 
from tkinter import ttk# python 3
from tkinter import Tk
from tkinter import Label
from tkinter import LabelFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 


class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Welcome to PEM")
        self.resizable(False,False)
        self.root_current_state = ""
        

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.configure(bg= "#9803fc",padx = 100)


        self.label = tk.Label(text="Add new products, analyse expenses and more\n Shall we begin..?\n", bg = "#9803fc", font=('Helvatical bold',15) )
        self.label.pack(side="top", fill="x", pady=10)

        self.proceed = tk.Button(self, text="Next",bg = "#b942f5",fg = "#45f542",command = self.OpenMain)
        self.proceed.pack()
        
    def OpenMain(self):
        self.tab_window = tk.Toplevel(self)
        self.tab_window.geometry("600x500")
        self.tab_window.resizable(False,False)
        self.tab_window.title("Personal Expenses Manager")
        self.customed_style = ttk.Style()
        self.customed_style.configure('Custom.TNotebook.Tab', padding=[60, 12], font=('Helvetica', 10), background="green3")
        self.settings = {"TNotebook.Tab": {
            "configure": {
                 "padding": [79,12],"background": "#808080", "font":("Helvetica",10) }, 
                    "map": {
                        "background": [("selected", "#00FF00"), ("active", "#32CD32")], 
                        "foreground": [("selected", "#000000"), ("active", "#000000")] } } }
        self.customed_style.theme_create("tab_theme",parent="alt", settings = self.settings)
        self.customed_style.theme_use("tab_theme")
        self.tabs = ttk.Notebook(self.tab_window, style = 'Custom.TNotebook')
        self.new_product_tab = ttk.Frame(self.tabs)
        self.plot_tab = ttk.Frame(self.tabs)
        self.settings_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.new_product_tab, text='New(+)')
        self.tabs.add(self.plot_tab, text='Plot')
        self.tabs.add(self.settings_tab, text='Settings')
        self.tabs.pack(expand= True, fill ="both")
        
        self.f = Figure(figsize=(5,5), dpi = 100)
        self.a = self.f.add_subplot(111)
        self.a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        self.canvas = FigureCanvasTkAgg(self.f, self.plot_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        self.legend_frame = LabelFrame(self.new_product_tab,text='Description',padx=250, pady=50)
        self.legend_frame.pack(side = tk.TOP, expand = False)
        self.product_name_label = Label(self.legend_frame,text = "Product Name: ", font = ('Helvetica', 10))
        self.product_name_label.grid(column=0, row=0, padx=0, pady=10)
        self.product_name_text = tk.Text(self.legend_frame,height = 2,width = 50)
        self.product_name_text.grid(column=1, row=0)
        
        _type_label = Label(self.legend_frame,text = "Product Type: ", font = ('Helvetica', 10))
        self.product_type_label.grid(column=0, row=1, padx=0, pady=10)
        self.product_type_text = tk.Text(self.legend_frame,height = 2,width = 50)
        self.product_type_text.grid(column=1, row=1)
        self.date_of_purchase_label = Label(self.legend_frame,text = "Date of Purchase: ", font = ('Helvetica', 10))
        self.date_of_purchase_label.grid(column=0, row=2, padx=0, pady=10)
        self.price_of_product_label = Label(self.legend_frame,text = "Price of Product: ", font = ('Helvetica', 10))
        self.price_of_product_label.grid(column=0, row=3, padx=0, pady=10)
        
        
        #self.product_name_label.place(x =100, y = 100 )
        
        self.withdraw()
        self.tab_window.protocol("WM_DELETE_WINDOW",self.open_root)

        
    def open_root(self):
        self.deiconify()
        self.root_current_state = self.state()
        if(self.root_current_state == "normal"):
            self.tab_window.destroy()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()