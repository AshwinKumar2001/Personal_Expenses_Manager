# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:02:03 2021

@author: AVITA
"""


import tkinter as tk                # python 3
from tkinter import PhotoImage, font as tkfont 
from tkinter import ttk# python 3
from tkinter import Tk
from tkinter import Button
from tkinter import Label
from tkinter import LabelFrame
from tkinter.constants import TRUE
from tkcalendar import Calendar
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame 
import pandas as pd
import pandasql as ps
import datetime
import csv
from tkinter import Scrollbar

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
        self.tab_window.geometry("800x600")
        self.tab_window.resizable(True,True)
        self.tab_window.title("Personal Expenses Manager")
        self.customed_style = ttk.Style()
        self.customed_style.configure('Custom.TNotebook.Tab', padding=[0, 0], font=('Helvetica', 10), background="green3")
        self.settings = {
            "TNotebook.Tab": {
            "configure": {
                 "padding": [112,20],"background": "#808080", "font":("Helvetica",10)}, 
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
        self.data_value_list = []
        self.sample_data = {'Week Days': ['Day 1','Day 2','Day 3','Day 4','Day 5','Day 6', 'Day 7'],
         'Groceries': [0,0,0,0,0,0,0],
         'Luxury': [0,0,0,0,0,0,0],
         'Other': [0,0,0,0,0,0,0]
        }

        self.graph_legend_frame = LabelFrame(self.plot_tab,text='Graph View',padx=20, pady=30)
        self.graph_legend_frame.grid(columnspan=2,ipadx = 250,ipady=100)
        self.vertical_graph_view = Scrollbar(self.graph_legend_frame)
        self.vertical_graph_view.pack(side =tk.RIGHT, fill = tk.Y)

        self.sample_dataframe = DataFrame(self.sample_data,columns=['Week Days','Groceries','Luxury','Other'])
        self.data_graph = Figure(figsize=(5,5), dpi = 50)
        self.a = self.data_graph.add_subplot(111)
        self.sample_dataframe = self.sample_dataframe[['Week Days','Groceries','Luxury','Other']].groupby('Week Days').sum()
        self.sample_dataframe.plot(kind='bar', legend=True, ax=self.a)
        
        self.canvas = FigureCanvasTkAgg(self.data_graph, self.graph_legend_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

        self.select_week_button = Button(self.graph_legend_frame,text = "Select Week",bg = "#00ff08",fg = "#ff3700",command =self.select_week)
        self.select_week_button.pack(fill=tk.BOTH)


        self.legend_frame = LabelFrame(self.new_product_tab,text='Description')
        self.legend_frame.grid(columnspan=2,ipadx = 250,ipady = 60)
        self.product_name_label = Label(self.legend_frame,text = "Product Name: ", font = ('Helvetica', 10))
        self.product_name_label.grid(column=0, row=0, ipadx=0, ipady=10)
        self.product_name_text = tk.Text(self.legend_frame,height = 2,width = 70)
        self.product_name_text.grid(column=1, row=0)
        
        self.product_type_label = Label(self.legend_frame,text = "Product Type: ", font = ('Helvetica', 10))
        self.product_type_label.grid(column=0, row=1, ipadx=0, ipady=10)
        self.product_type_selection = ttk.Combobox(self.legend_frame,values=["Groceries","Luxury","Other"], font = ('Helvetica', 10))
        self.product_type_selection.grid(column=1,row =1,ipadx=200,ipady=7)
        self.product_type_selection.current(0)

        self.date_of_purchase_label = Label(self.legend_frame,text = "Date of Purchase: ", font = ('Helvetica', 10))
        self.date_of_purchase_label.grid(column=0, row=2, ipadx=0, ipady=10)
        self.date_show_label = Label(self.legend_frame, text = "dd/mm/yyyy", font = ('Helvetica', 10),  relief="sunken")
        self.date_show_label.grid(column =1, row = 2, ipadx= 240, ipady = 7)
        self.calendar_button_image = PhotoImage(file = 'calendar.png')
        self.calendar_button_image.subsample(6)
        self.calendar_label= Label(image=self.calendar_button_image)
        self.calendar_button = Button(self.legend_frame,image=self.calendar_button_image, borderwidth=0, command = self.select_date)
        self.calendar_button.grid(column=2,row=2)
        self.price_of_product_label = Label(self.legend_frame,text = "Price of Product: ₹", font = ('Helvetica', 10))
        self.price_of_product_label.grid(column=0, row=3, ipadx=0, ipady=10)
        self.price_of_product_text = tk.Text(self.legend_frame,height = 2,width = 70)
        self.price_of_product_text.grid(column=1, row=3)
        
        self.add_product_button = Button(self.legend_frame, text = "Add", borderwidth=2, bg = "#00ff08",fg = "#ff3700", command=self.add_product)
        self.add_product_button.grid(column = 1, row=4, ipadx=20,ipady=7)
        
        self.withdraw()
        self.tab_window.protocol("WM_DELETE_WINDOW",self.open_root)

    def add_product(self):
        self.product_name_show = self.product_name_text.get("1.0",'end-1c')
        self.product_type_show = self.product_type_selection.get()
        self.date_of_purchase_show = self.date_show_label.cget("text")
        self.product_price_show = self.price_of_product_text.get("1.0",'end-1c')
        if(len(self.product_name_show)==0):
            messagebox.showerror("Product Name Error","Please Enter the Product Name!")
        elif(self.date_of_purchase_show == 'dd/mm/yyyy'):
            messagebox.showerror("Product Date Error","Please Enter the Date of Purchase!")
        elif(len(self.product_price_show) == 0):
            messagebox.showerror("Product Price Error","Please Enter the Price of the Product!")
        else:
            messagebox.showinfo(title = 'Product Info', message = 'Product Name: '+ self.product_name_show + '\nProduct Type: ' + self.product_type_show + '\nDate of Purchase: ' + self.date_of_purchase_show + '\nProduct Price: ' + self.product_price_show + ' ₹')
            self.product_details = [self.product_name_show, self.product_type_show, self.date_of_purchase_show, self.product_price_show]
            with open('product_details.csv', 'a', newline= '') as self.file:
                self.write_details = csv.writer(self.file)
                self.write_details.writerow(self.product_details)

    def select_date(self):
        self.calendar_window = tk.Toplevel(self.tab_window)
        self.calendar = Calendar(self.calendar_window,selectmode="day",year= 2021, month=1, day=1, date_pattern = 'dd/mm/y')
        self.calendar.pack(fill = tk.BOTH, expand =True)
        self.select_date_button = Button(self.calendar_window, text ="Select Date", command = self.get_calendar_date)
        self.select_date_button.pack(ipady = 8)

    def select_week(self):
        self.graph_calendar_window = tk.Toplevel(self.tab_window)
        self.graph_calendar = Calendar(self.graph_calendar_window, selectmode="day",year= 2021, month=1, day=1, date_pattern = 'dd/mm/y')
        self.graph_calendar.pack(fill = tk.BOTH, expand =True)
        self.select_week_date_button = Button(self.graph_calendar_window, text ="Select Week Start", command = self.get_graph_calendar_date)
        self.select_week_date_button.pack(ipady = 8)

    
    def get_calendar_date(self):
        self.date_text = self.calendar.get_date()
        self.date_show_label.configure(text = self.date_text)
        self.calendar_window.destroy()

    def get_graph_calendar_date(self):
        self.graph_date_text = self.graph_calendar.get_date()
        messagebox.showinfo(title = 'Product Info', message = 'Start Date: ' + self.graph_date_text)
        self.data_value_list = self.data_extract()
        messagebox.showinfo(title = 'Product Info', message = 'Data List: ' + str(self.data_value_list))
        self.extracted_data = {'Week Days': ['Day 1','Day 2','Day 3','Day 4','Day 5','Day 6', 'Day 7'],
         'Groceries': self.data_value_list[0],
         'Luxury': self.data_value_list[1],
         'Other': self.data_value_list[2]
        }
        self.graph_legend_frame.destroy()

        self.graph_legend_frame = LabelFrame(self.plot_tab,text='Graph View',padx=20, pady=30)
        self.graph_legend_frame.grid(columnspan=2,ipadx = 250,ipady=100)

        self.extracted_dataframe = DataFrame(self.extracted_data,columns=['Week Days','Groceries','Luxury','Other'])
        self.data_graph = Figure(figsize=(5,5), dpi = 50)
        self.a = self.data_graph.add_subplot(111)
        self.extracted_dataframe = self.extracted_dataframe[['Week Days','Groceries','Luxury','Other']].groupby('Week Days').sum()
        self.extracted_dataframe.plot(kind='bar', legend=True, ax=self.a)
        
        self.canvas = FigureCanvasTkAgg(self.data_graph, self.graph_legend_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

        self.select_week_button = Button(self.graph_legend_frame,text = "Select Week",bg = "#00ff08",fg = "#ff3700",command =self.select_week)
        self.select_week_button.pack(fill=tk.BOTH)
        self.graph_calendar_window.destroy()

    def data_extract(self):
        self.power_list = []
        self.groceries = []
        self.luxury = []
        self.other = []
        for data_row in range(7):
            self.custom_dataframe = pd.read_csv('product_details.csv', header=None)
            self.custom_dataframe.columns = ['Product_Name', 'Product_Category', 'Purchase_Date', 'Product_Price']
            self.proper_df = self.custom_dataframe.iloc[:,1:]
            print(self.proper_df,end="\n\n")
            grouped_df_by_date = self.proper_df[['Product_Category','Purchase_Date','Product_Price']].groupby(['Purchase_Date','Product_Category'], as_index= False).sum('Product_Price')
            self.date_start_date = datetime.datetime.strptime(self.graph_date_text, "%d/%m/%Y").date()
            self.date_query = "select * from grouped_df_by_date where Purchase_Date = '"+self.graph_date_text+"'"
            self.temporary_day_values = ps.sqldf(self.date_query, locals())
            if(len(self.temporary_day_values)!=0):
                for data_row in range(len(self.temporary_day_values)):
                    if self.temporary_day_values['Product_Category'][data_row] == 'Groceries':
                        self.groceries.append(self.temporary_day_values['Product_Price'][data_row])
                    elif self.temporary_day_values['Product_Category'][data_row] == 'Luxury':
                        self.luxury.append(self.temporary_day_values['Product_Price'][data_row])
                    elif self.temporary_day_values['Product_Category'][data_row] == 'Other':
                        self.other.append(self.temporary_day_values['Product_Price'][data_row])
                    
                self.temporary_max_value = max(len(self.groceries),len(self.luxury),len(self.other))
                if len(self.groceries) != self.temporary_max_value:
                    self.groceries.append(0)
                if len(self.luxury) != self.temporary_max_value:
                    self.luxury.append(0)
                if len(self.other) != self.temporary_max_value:
                    self.other.append(0)
                
            else:
                self.groceries.append(0)
                self.luxury.append(0)
                self.other.append(0)   
                
            self.date_next = self.date_start_date + datetime.timedelta(1)
            self.graph_date_text = self.date_next.strftime("%d/%m/%Y")
        
        self.power_list.append(self.groceries)
        self.power_list.append(self.luxury)
        self.power_list.append(self.other)
        
        return (self.power_list)

    def open_root(self):
        self.deiconify()
        self.root_current_state = self.state()
        if(self.root_current_state == "normal"):
            self.tab_window.destroy()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()