# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:02:03 2021

@author: AVITA
"""


from re import L
import tkinter as tk                # python 3
from tkinter import BooleanVar, PhotoImage, Toplevel, font as tkfont 
from tkinter import ttk# python 3
from tkinter import Tk
from tkinter import Button
from tkinter import Label
from tkinter import LabelFrame
from tkinter.constants import TRUE
from typing import Text
from tkcalendar import Calendar
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame 
from tkinter import Checkbutton
from tkinter import Scrollbar
import pandas as pd
import pandasql as ps
import datetime
import csv

class SampleApp(Tk):
    #----------------------------------Introduction Page--------------------------------#

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Welcome to PEM")
        self.resizable(False,False)
        self.root_current_state = ""
        
        self.configure(bg= "#9803fc",padx = 100)


        self.label = tk.Label(text="Add new products, analyse expenses and more\n Shall we begin..?\n", bg = "#9803fc", font=('Helvatical bold',15) )
        self.label.pack(side="top", fill="x", pady=10)

        self.proceed = tk.Button(self, text="Next",bg = "#b942f5",fg = "#45f542",command = self.OpenMain)
        self.proceed.pack()

    #----------------------------------------------------------------------------------#

    #----------------------------------Main Work Window--------------------------------#   
    def OpenMain(self):
        self.tab_window = tk.Toplevel(self)
        self.tab_window.geometry("700x600")
        self.tab_window.resizable(False,False)
        self.tab_window.title("Personal Expenses Manager")
        self.customed_style = ttk.Style()
        self.customed_style.configure('Custom.TNotebook.Tab', padding=[0, 0], font=('Helvetica', 10), background="green3")
        self.settings = {
            "TNotebook.Tab": {
            "configure": {
                 "padding": [96,20],"background": "#808080", "font":("Helvetica",10)}, 
                    "map": {
                        "background": [("selected", "#00FF00"), ("active", "#32CD32")], 
                        "foreground": [("selected", "#000000"), ("active", "#000000")] } } }
        self.customed_style.theme_create("tab_theme",parent="alt", settings = self.settings)
        self.customed_style.theme_use("tab_theme")
        self.display_dataframe = pd.read_csv('product_details.csv', header=None)
        self.display_dataframe.columns = ['Product Name', 'Product Category', 'Purchase Date', 'Product Price']
        self.display_dataframe.to_csv('custom_details.csv', index = False)

        #----------------------------------Creating Tabs--------------------------------#

        self.tabs = ttk.Notebook(self.tab_window, style = 'Custom.TNotebook')
        self.new_product_tab = ttk.Frame(self.tabs)
        self.plot_tab = ttk.Frame(self.tabs)
        self.settings_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.new_product_tab, text='New(+)')
        self.tabs.add(self.plot_tab, text='Plot')
        self.tabs.add(self.settings_tab, text='Settings')
        self.tabs.pack(expand= True, fill ="both")

        #----------------------------------------------------------------------------------#

        #------------------------------Initial Graph Data----------------------------------#

        self.data_value_list = []
        self.check_variable = False
        self.sample_data = {'Week Days': ['Day 1','Day 2','Day 3','Day 4','Day 5','Day 6', 'Day 7'],
         'Groceries': [0,0,0,0,0,0,0],
         'Luxury': [0,0,0,0,0,0,0],
         'Other': [0,0,0,0,0,0,0]
        }

        #----------------------------------------------------------------------------------#

        #-------------------------!!!!!-Plot Tab Begins Here-!!!!!-------------------------#

        #-------------------------------Analysis Frame (Plot Tab)--------------------------#

        self.analysis_legend_frame = LabelFrame(self.plot_tab, text = "Analysis")
        self.analysis_legend_frame.grid(row = 1, column = 0, sticky = tk.NSEW, ipadx = 250)
        
        #-------------------------------Here you will get to see if there was a budget overflow/cross
        self.groceries_crossed_label = Label(self.analysis_legend_frame, text = "    Crossed Groceries Limit: ", font = ('Helvetica', 10))
        self.groceries_crossed_label.grid(row = 0, column = 0)
        self.groceries_crossed_status = Label(self.analysis_legend_frame, text = "No", font = ('Helvetica', 10))
        self.groceries_crossed_status.grid(row = 0, column = 1)

        self.luxury_crossed_label = Label(self.analysis_legend_frame, text = "Crossed Luxury Limit: ", font = ('Helvetica', 10))
        self.luxury_crossed_label.grid(row = 1, column = 0)
        self.luxury_crossed_status = Label(self.analysis_legend_frame, text = "No", font = ('Helvetica', 10))
        self.luxury_crossed_status.grid(row = 1, column = 1)

        self.other_crossed_label = Label(self.analysis_legend_frame, text = " Crossed Other/s Limit: ", font = ('Helvetica', 10))
        self.other_crossed_label.grid(row = 2, column = 0)
        self.other_crossed_status = Label(self.analysis_legend_frame, text = "No", font = ('Helvetica', 10))
        self.other_crossed_status.grid(row = 2, column = 1)

        #----------------------------------------------------------------------------------#

        #----------------------------------Graph Frame (Plot Tab)--------------------------#

        self.graph_legend_frame = LabelFrame(self.plot_tab,text='Graph View',padx=20, pady=30)
        self.graph_legend_frame.grid(columnspan=2,ipadx = 250,ipady=100)

        #----------------------------------Graph area (canvas) is shown here
        self.sample_dataframe = DataFrame(self.sample_data,columns=['Week Days','Groceries','Luxury','Other'])
        self.data_graph = Figure(figsize=(3,3), dpi = 50)
        self.a = self.data_graph.add_subplot(111)
        self.sample_dataframe = self.sample_dataframe[['Week Days','Groceries','Luxury','Other']].groupby('Week Days').sum()
        self.sample_dataframe.plot(kind='bar', legend=True, ax=self.a)
        
        self.canvas = FigureCanvasTkAgg(self.data_graph, self.graph_legend_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

        self.select_week_button = Button(self.graph_legend_frame,text = "Select Week",bg = "#00ff08",fg = "#ff3700",command =self.select_week)
        self.select_week_button.pack(fill=tk.BOTH)

        #-----------------------------<<<<<<<< Plot Tab ends >>>>>>>>>-------------------------#

        #-------------------------!!!!!!- New(+) Tab begins here-!!!!!!------------------------#

        #-------------------------Product Description Frame (Entry area)-------------------#

        #--------------------------Product name entry textbox
        self.legend_frame = LabelFrame(self.new_product_tab,text='Description')
        self.legend_frame.grid(columnspan=2,ipadx = 250,ipady = 60)
        self.product_name_label = Label(self.legend_frame,text = "Product Name: ", font = ('Helvetica', 10))
        self.product_name_label.grid(column=0, row=0, ipadx=0, ipady=10)
        self.product_name_text = tk.Text(self.legend_frame,height = 2,width = 60)
        self.product_name_text.grid(column=1, row=0)
        
        #--------------------------Product type entry combobox(optionbox)
        self.product_type_label = Label(self.legend_frame,text = "Product Type: ", font = ('Helvetica', 10))
        self.product_type_label.grid(column=0, row=1, ipadx=0, ipady=10)
        self.product_type_selection = ttk.Combobox(self.legend_frame,values=["Groceries (Starts at 1₹)","Luxury (Starts at 1000₹)","Other (Starts at 500₹)"], font = ('Helvetica', 10))
        self.product_type_selection.grid(column=1,row =1,ipadx=165,ipady=7)
        self.product_type_selection.current(0)

        #--------------------------Date of purchase label (Calendar selection)
        self.date_of_purchase_label = Label(self.legend_frame,text = "Date of Purchase: ", font = ('Helvetica', 10))
        self.date_of_purchase_label.grid(column=0, row=2, ipadx=0, ipady=10)
        self.date_show_label = Label(self.legend_frame, text = "dd/mm/yyyy", font = ('Helvetica', 10),  relief="sunken")
        self.date_show_label.grid(column =1, row = 2, ipadx= 203, ipady = 7)
        self.calendar_button_image = PhotoImage(file = 'calendar.png')
        self.calendar_button_image.subsample(6)
        self.calendar_label= Label(image=self.calendar_button_image)
        self.calendar_button = Button(self.legend_frame,image=self.calendar_button_image, borderwidth=0, command = self.select_date)
        self.calendar_button.grid(column=2,row=2)
        self.price_of_product_label = Label(self.legend_frame,text = "Price of Product: ₹", font = ('Helvetica', 10))
        self.price_of_product_label.grid(column=0, row=3, ipadx=0, ipady=10)
        self.price_of_product_text = tk.Text(self.legend_frame,height = 2,width = 60)
        self.price_of_product_text.grid(column=1, row=3)
        
        self.add_product_button = Button(self.legend_frame, text = "Add", borderwidth=2, bg = "#00ff08",fg = "#ff3700", command=self.add_product)
        self.add_product_button.grid(column = 1, row=4, ipadx=20,ipady=7)

        #----------------------------------------------------------------------------------#

        #--------------------------------<<<<<< New (+) Tab ends >>>>>---------------------#

        #--------------------------!!!!!-Settings tabs begins here-!!!!!-------------------#

        #---------------------Creating two frames for two types of Settings----------------#
        self.special_settings_legend_frame = LabelFrame(self.settings_tab, text = "Special" )
        self.special_settings_legend_frame.grid(row = 1, column = 0, ipadx = 200, ipady = 120, columnspan= 2, sticky= tk.NSEW)

        self.general_settings_legend_frame = LabelFrame(self.settings_tab,text = "General")
        self.general_settings_legend_frame.grid(row = 0, column = 0, ipadx = 200, ipady = 10)
        self.set_warranty_warning_label = Label(self.general_settings_legend_frame, text = "Set Warranty Warning: ", font = ('Helvetica', 10))
        self.set_warranty_warning_label.grid(row = 0, column = 0)
        self.warranty_selection_variable = BooleanVar()
        self.warranty_selection = Checkbutton(self.general_settings_legend_frame, text = "No", var = self.warranty_selection_variable, command =self.check_warranty_set_status, font = ('Helvetica', 10))
        self.warranty_selection.grid(row= 0, column= 1)
        
        #----------------------------Add your desired budget limits here
        self.groceries_budget_limit_label = Label(self.general_settings_legend_frame,text = "Set Groceries Budget: ₹", font = ('Helvetica', 10))
        self.groceries_budget_limit_label.grid(row = 1  , column = 0,  ipadx=0, ipady=10)
        self.groceries_budget_limit_text = tk.Text(self.general_settings_legend_frame,height = 2,width = 60)
        self.groceries_budget_limit_text.grid(row = 1, column = 1)

        self.luxury_budget_limit_label = Label(self.general_settings_legend_frame,text = "Set Luxury Budget: ₹", font = ('Helvetica', 10))
        self.luxury_budget_limit_label.grid(row = 2  , column = 0,  ipadx=0, ipady=10)
        self.luxury_budget_limit_text = tk.Text(self.general_settings_legend_frame,height = 2,width = 60)
        self.luxury_budget_limit_text.grid(row = 2, column = 1)

        self.other_budget_limit_label = Label(self.general_settings_legend_frame,text = "Set Other/s Budget: ₹", font = ('Helvetica', 10))
        self.other_budget_limit_label.grid(row = 3  , column = 0,  ipadx=0, ipady=10)
        self.other_budget_limit_text = tk.Text(self.general_settings_legend_frame,height = 2,width = 60)
        self.other_budget_limit_text.grid(row = 3, column = 1)

        #------------------------------Save Button to save your settings in csv file
        self.save_general_settings_button = Button(self.general_settings_legend_frame, text = "Save", command = self.save_general_settings, bg = "#00ff08",fg = "#ff3700")
        self.save_general_settings_button.grid(row = 4, column = 1, ipadx= 63, ipady= 7, padx= 10, pady = 12)

        self.view_data_button = Button(self.general_settings_legend_frame, text ="View Data", command = self.view_data, bg = "#00ff08",fg = "#ff3700")
        self.view_data_button.grid(row = 5, column = 1,ipadx = 50, ipady = 7, padx= 10, pady = 12)

        self.fill_initial_settings()

        #------------------------<<<<< Settings tab ends >>>>>>>-----------------------------#


        self.withdraw()
        self.tab_window.deiconify()
        self.tab_window.protocol("WM_DELETE_WINDOW",self.close_all)

    #----------------------------<<<<<< Main Work Window ends >>>>>>---------------------------#

    #-----------------------------Function to View the CSV data in a tkinter table

    def view_data(self):
        self.data_window = Toplevel(self.tab_window, height = 100, width = 250)
        self.data_window.resizable(False,False)
        self.data_window.title("Product Data")
        self.data_window_scrollbarx = Scrollbar(self.data_window, orient=tk.HORIZONTAL)
        self.data_window_scrollbary = Scrollbar(self.data_window, orient=tk.VERTICAL)
        self.data_tree = ttk.Treeview(self.data_window, columns=("Product Name", "Product Category", "Purchase Date", "Product Price"), height=20, selectmode="extended", yscrollcommand=self.data_window_scrollbary.set, xscrollcommand=self.data_window_scrollbarx.set)
        self.data_window_scrollbary.config(command=self.data_tree.yview)
        self.data_window_scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        self.data_window_scrollbarx.config(command=self.data_tree.xview)
        self.data_window_scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        self.data_tree.heading('Product Name', text="Product Name", anchor=tk.W)
        self.data_tree.heading('Product Category', text="Product Category", anchor=tk.W)
        self.data_tree.heading('Purchase Date', text="Purchase Date", anchor=tk.W)
        self.data_tree.heading('Product Price', text="Product Price", anchor=tk.W)
        self.data_tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.data_tree.column('#1', stretch=tk.NO, minwidth=0, width=120)
        self.data_tree.column('#2', stretch=tk.NO, minwidth=0, width=120)
        self.data_tree.column('#3', stretch=tk.NO, minwidth=0, width=120)
        self.data_tree.column('#4', stretch=tk.NO, minwidth=0, width=120)
        self.data_tree.pack()

        with open('custom_details.csv') as readfile:
            self.data_reader = csv.DictReader(readfile, delimiter=',')
            for row in self.data_reader:
                self.pname = row['Product Name']
                self.ptype = row['Product Category']
                self.pdate = row['Purchase Date']
                self.pprice = row['Product Price']
                self.data_tree.insert("", 0, values=(self.pname, self.ptype, self.pdate, self.pprice))

    #------------------ This will fill in the settings for Settings tab if it exists in CSV file

    def fill_initial_settings(self):
        self.fill_general_settings_reader_file = open('general_settings.csv')
        self.fill_general_settings_reader = csv.reader(self.fill_general_settings_reader_file)
        self.fill_general_settings_list_rows = []
        for row in self.fill_general_settings_reader:
            self.fill_general_settings_list_rows.append(row)
        self.tofill_warranty_status = self.fill_general_settings_list_rows[0][0]
        self.tofill_groceries_budget_value = int(self.fill_general_settings_list_rows[0][1])
        self.tofill_luxury_budget_value = int(self.fill_general_settings_list_rows[0][2])
        self.tofill_other_budget_value = int(self.fill_general_settings_list_rows[0][3])
        if (self.tofill_warranty_status == "Yes"):
            self.warranty_selection.select()
            self.check_warranty_set_status()
        self.groceries_budget_limit_text.insert(tk.END, self.tofill_groceries_budget_value)
        self.luxury_budget_limit_text.insert(tk.END, self.tofill_luxury_budget_value)
        self.other_budget_limit_text.insert(tk.END, self.tofill_other_budget_value)

    #-----------------------Save the entered settings into the CSV file
    def save_general_settings(self):
        if(self.check_variable == True):
            self.warranty_status_text = "Yes"
        else:
            self.warranty_status_text = "No"         
        self.groceries_limit_text =  self.groceries_budget_limit_text.get("1.0",'end-1c')
        self.luxury_limit_text = self.luxury_budget_limit_text.get("1.0",'end-1c')
        self.other_limit_text = self.other_budget_limit_text.get("1.0",'end-1c')
        if (self.groceries_limit_text == ""):
            self.groceries_limit_text = "0"
        if (self.luxury_limit_text == ""):
            self.luxury_limit_text = "0"
        if (self.other_limit_text == ""):
            self.other_limit_text = "0"  
        self.general_settings_list = [self.warranty_status_text, self.groceries_limit_text, self.luxury_limit_text, self.other_limit_text]
        with open('general_settings.csv', 'w', newline= '') as self.gsfile:
            self.write_general_settings_details = csv.writer(self.gsfile)
            self.write_general_settings_details.writerow(self.general_settings_list)   
        self.gsfile.close()                   
        print(self.warranty_status_text,self.groceries_limit_text,self.luxury_limit_text, self.other_limit_text, sep = "\n")

    #----------------------- Checks if the warranty warning setting is activated
    def check_warranty_set_status(self):
        self.check_variable = self.warranty_selection_variable.get()
        if(self.check_variable == True):
            self.warranty_selection.config(text="Yes")
        else:
            self.warranty_selection.config(text="No")
    
    #------------------------ Adds the product details given by user into products CSV file 
    def add_product(self):
        self.string_sep = " "
        self.product_name_show = self.product_name_text.get("1.0",'end-1c')
        self.product_type_show = self.product_type_selection.get()
        self.modified_product_type_text = self.product_type_show.split(self.string_sep, 1)[0]
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
            self.product_details = [self.product_name_show, self.modified_product_type_text, self.date_of_purchase_show, self.product_price_show]
            with open('product_details.csv', 'a', newline= '') as self.file:
                self.write_details = csv.writer(self.file)
                self.write_details.writerow(self.product_details)
                self.display_dataframe = pd.read_csv('product_details.csv', header=None)
                self.display_dataframe.columns = ['Product Name', 'Product Category', 'Purchase Date', 'Product Price']
                self.display_dataframe.to_csv('custom_details.csv', index = False)

    #----------------------------- Allows selection of date of purchase for product
    def select_date(self):
        self.calendar_window = tk.Toplevel(self.tab_window)
        self.calendar = Calendar(self.calendar_window,selectmode="day",year= 2021, month=1, day=1, date_pattern = 'dd/mm/y')
        self.calendar.pack(fill = tk.BOTH, expand =True)
        self.select_date_button = Button(self.calendar_window, text ="Select Date", command = self.get_calendar_date)
        self.select_date_button.pack(ipady = 8)

    #----------------------------- Helps user select the start date of a particular week for analysis
    def select_week(self):
        self.graph_calendar_window = tk.Toplevel(self.tab_window)
        self.graph_calendar = Calendar(self.graph_calendar_window, selectmode="day",year= 2021, month=1, day=1, date_pattern = 'dd/mm/y')
        self.graph_calendar.pack(fill = tk.BOTH, expand =True)
        self.select_week_date_button = Button(self.graph_calendar_window, text ="Select Week Start", command = self.get_graph_calendar_date)
        self.select_week_date_button.pack(ipady = 8)

    #----------------------------- Gets calendar date from user choice for product date.
    def get_calendar_date(self):
        self.date_text = self.calendar.get_date()
        self.date_show_label.configure(text = self.date_text)
        self.calendar_window.destroy()

    #----------------------------- Gets week start date, calculates product category price values...
    #----------------------------- ... and displays the same in a graph canvas
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
        self.data_graph = Figure(figsize=(3,3), dpi = 50)
        self.a = self.data_graph.add_subplot(111)
        self.extracted_dataframe = self.extracted_dataframe[['Week Days','Groceries','Luxury','Other']].groupby('Week Days').sum()
        self.extracted_dataframe.plot(kind='bar', legend=True, ax=self.a)
        
        self.canvas = FigureCanvasTkAgg(self.data_graph, self.graph_legend_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

        self.groceries_budget_label = Label(self.plot_tab, text = "Groceries Budget Exceeded? ", font = ('Helvetica', 10))
        self.luxuries_budget_label = Label(self.plot_tab, text = "Luxuries Budget Exceeded? ", font = ('Helvetica', 10))
        self.other_budget_label = Label(self.plot_tab, text = "Other Budget Exceeded? ", font = ('Helvetica', 10))
        self.groceries_budget_value_label = Label(self.plot_tab, text = "No", font = ('Helvetica', 10))
        self.luxuries_budget_value_label = Label(self.plot_tab, text = "No ", font = ('Helvetica', 10))
        self.other_budget_value_label = Label(self.plot_tab, text = "No ", font = ('Helvetica', 10))

        self.select_week_button = Button(self.graph_legend_frame,text = "Select Week",bg = "#00ff08",fg = "#ff3700",command =self.select_week)
        self.select_week_button.pack(fill=tk.BOTH)

        self.general_settings_reader_file = open('general_settings.csv')
        self.general_settings_reader = csv.reader(self.general_settings_reader_file)
        self.settings_list_rows = []
        for row in self.general_settings_reader:
            self.settings_list_rows.append(row)
        self.groceries_budget_value = int(self.settings_list_rows[0][1])
        self.luxury_budget_value = int(self.settings_list_rows[0][2])
        self.other_budget_value = int(self.settings_list_rows[0][3])
        if (sum(self.data_value_list[0]) > self.groceries_budget_value):
            self.groceries_crossed_status.config(text ="Yes")
        else:
            self.groceries_crossed_status.config(text ="No")
        if (sum(self.data_value_list[1]) > self.luxury_budget_value):
            self.luxury_crossed_status.config(text ="Yes")
        else:
            self.luxury_crossed_status.config(text ="No")
        if (sum(self.data_value_list[2]) > self.other_budget_value):
            self.other_crossed_status.config(text ="Yes")
        else:
            self.other_crossed_status.config(text ="No")
        self.graph_calendar_window.destroy()

    # ------------------------------- Extracts the data from CSV file, It uses SQL query to filter required data.
    #-------------------------------- This data will then be used for graph plotting.
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

    #---------------------------- Closes the Work Window and the Introduction Window 
    def close_all(self):
        self.deiconify()
        self.root_current_state = self.state()
        if(self.root_current_state == "normal"):
            self.tab_window.destroy()
            self.destroy()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()