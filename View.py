from tkinter import *
from tkinter import Tk, Label, Button, messagebox, font, Frame, Entry, ttk
from PIL import ImageTk
from Model import *


class LoginScreen(Frame):

    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller

        # Creating labels such as username and password

        self.user = Label(root, text="Username *", bg="white")
        self.user.place(relx=0.285, rely=0.298, height=20, width=80)
        self.passwd = Label(root, text="Password *", bg="white")
        self.passwd.place(relx=0.285, rely=0.468, height=20, width=80)

        # Creating Buttons for login and exit

        self.login_button = Button(root, text="Login")
        self.login_button.place(relx=0.440, rely=0.638, height=30, width=60)
        self.login_button.configure(command=self.login_user)

        self.exit_button = Button(root, text="Exit")
        self.exit_button.place(relx=0.614, rely=0.638, height=30, width=60)
        self.exit_button.configure(command=self.exit_login)

        # Creating entry boxes for input

        self.username_box = Entry(root)
        self.username_box.place(relx=0.440, rely=0.298, height=20, relwidth=0.35)
        self.password_box = Entry(root)
        self.password_box.place(relx=0.440, rely=0.468, height=20, relwidth=0.35)
        self.password_box.configure(show="*")
        self.password_box.configure(background="white")

    def event_X(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            exit()

    # Giving function to login process

    def login_user(self):
        name = self.username_box.get()
        password = self.password_box.get()
        status = self.controller.login(name, password)
        if status == False:
            messagebox.showwarning("Acess Denied", "Username or Password incorrect!")
            # messagebox showing warning for wrong inputs

    def exit_login(self):
        msg = messagebox.askyesno("Exit login page", "Do you really want to exit?")
        if (msg):
            exit()


class MainScreen:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # top buttons
        self.top_bottom_frame = Frame(self.root)
        self.top_bottom_frame.pack(side=TOP, fill=X)
        print(type(self.controller.get_current_user()) is Manager)
        Button(self.top_bottom_frame, text="Log out").pack(side="right")
        Button(self.top_bottom_frame, text="Account").pack(side="right")
        Button(self.top_bottom_frame, text="New Order", command=lambda: self.switch_frame(CreateOrderScreen)).pack(
            side="left")

        # bottom buttons
        self.bottom_frame = Frame(root)
        self.bottom_frame.pack(side=BOTTOM)
        Button(self.bottom_frame, text="Order", command=lambda: self.switch_frame(OrderScreen)).pack(side="left")
        Button(self.bottom_frame, text="Inventory", command=lambda: self.switch_frame(InventoryScreen)).pack(
            side="left")
        if type(self.controller.get_current_user()) is Owner:
            Button(self.bottom_frame, text="Report", command=lambda: self.switch_frame(ReportScreen)).pack(side="left")
        if type(self.controller.get_current_user()) is Manager or type(self.controller.get_current_user()) is Owner:
            Button(self.bottom_frame, text="Staff Information").pack(side="bottom")

        self._frame = None
        self.switch_frame(OrderScreen)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self.root, self.controller)
        if self._frame is not None:
            # Destroys current frame and replaces with new one
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class OrderScreen(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        root.title("Order")


class ReportScreen(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        root.title("Report")
        self.controller = controller
        # load report info for all store
        self.store_name = self.controller.get_all_store_name()
        self.store_info = self.controller.get_all_store_info()
        self.day_made_most_sale = self.controller.day_of_week_of_last_month_made_most_sale()
        self.total_sale_last_month = self.controller.total_sale_last_month()
        self.total_coffee_sold = self.controller.total_item_sold_by_category("coffee")
        self.total_food_sold = self.controller.total_item_sold_by_category("foods")
        self.total_drinks_sold = self.controller.total_item_sold_by_category("drinks")
        self.total_coffee_bean_sold = self.controller.total_item_sold_by_category("coffee bean")
        self.popular_item_sold = self.controller.type_of_item_sold_by_category("coffee")
        # Select Store
        option_list = ["Please chose the store you would like to view "]
        for store in self.store_name:
            option_list.append(store[0])
        self.variable = StringVar(self)
        self.variable.set(option_list[0])

        opt = OptionMenu(self, self.variable, *option_list)
        opt.config(width=90, font=('Helvetica', 12))
        opt.pack()
        self.variable.trace("w", self.callback)
        # init tab
        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')
        self.tab_control = ttk.Notebook(self, style='lefttab.TNotebook')
        self.create_tab(None)

    def create_tab(self, store_id):

        self.tab_control.destroy()
        if store_id != None:
            # tab
            style = ttk.Style(self)
            style.configure('lefttab.TNotebook', tabposition='wn')
            self.tab_control = ttk.Notebook(self, style='lefttab.TNotebook')
            # tab1
            store_heading = ["Store ID", "Address", "Suburb", "State", "Postal Code"]
            # get store info for current store
            info_list = self.get_by_store_id(self.store_info, store_id)
            tab1 = Frame(self.tab_control)
            tab1.pack(fill="both")
            # adding table
            for row in range(2):
                for column in range(len(store_heading)):
                    if row == 0:
                        label = Label(tab1, text=store_heading[column], bg="#E0E0E0", fg="black", padx=3, pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        tab1.grid_columnconfigure(column, weight=1)
                    else:
                        label = Label(tab1, text=info_list[column], bg="#F0F0F0", fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)

            self.tab_control.add(tab1, text="Store information  ")

            # tab2
            revenue_heading = ["Revenue Last Month"]
            tab2 = Frame(self.tab_control)
            tab2.pack(fill="both")
            # calculate revenue
            info_list = [self.get_by_store_id(self.total_sale_last_month, store_id)]
            # adding table
            for row in range(2):
                for column in range(len(revenue_heading)):
                    revenue = '$' + str(info_list[column])
                    if row == 0:
                        label = Label(tab2, text=revenue_heading[column], bg="#E0E0E0", fg="black", padx=3, pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        tab2.grid_columnconfigure(column, weight=1)

                    else:
                        label = Label(tab2, text=revenue, bg="#F0F0F0", fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)

            self.tab_control.add(tab2, text='Revenue                ')

            # tab3
            revenue_heading = [["Day made most sales 1 Week ago", "Total made"],
                               ["Day made most sales 2 Week ago", "Total made"],
                               ["Day made most sales 3 Week ago", "Total made"],
                               ["Day made most sales 4 Week ago", "Total made"]]
            tab3 = Frame(self.tab_control)
            tab3.pack(fill="both")
            info_list = self.get_by_store_id(self.day_made_most_sale, store_id)
            for i in range(len(info_list)):
                info_list[i][1] = "$" + str(info_list[i][1])
            row_count = 0
            for i in range(4):

                # calculate revenue
                # adding table
                for row in range(2):
                    for column in range(len(revenue_heading[i])):
                        if row == 0:
                            label = Label(tab3, text=revenue_heading[i][column], bg="#E0E0E0", fg="black", padx=3,
                                          pady=3)
                            label.grid(row=row_count, column=column, sticky="nsew", padx=1, pady=1)
                            tab3.grid_columnconfigure(column, weight=1)
                        else:
                            label = Label(tab3, text=info_list[i][column], bg="#F0F0F0", fg="black")
                            label.grid(row=row_count, column=column, sticky="nsew", padx=1, pady=1)
                            label.grid_columnconfigure(column, weight=1)
                    row_count += 1

            self.tab_control.add(tab3, text='Day Made Most Sales')

            # tab4
            total_heading = ["Item category", "Quantity sold"]
            tab4 = Frame(self.tab_control)
            tab4.pack(fill="both")
            # calculate total sale by item category
            info_list = []
            info_list.append(self.get_by_store_id(self.total_coffee_sold, store_id))
            info_list.append(self.get_by_store_id(self.total_food_sold, store_id))
            info_list.append(self.get_by_store_id(self.total_drinks_sold, store_id))
            info_list.append(self.get_by_store_id(self.total_coffee_bean_sold, store_id))
            # adding table
            for row in range(len(info_list) + 1):
                for column in range(len(total_heading)):
                    if row == 0:
                        label = Label(tab4, text=total_heading[column], bg="#E0E0E0", fg="black", padx=3, pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        tab4.grid_columnconfigure(column, weight=1)
                    else:
                        label = Label(tab4, text=info_list[row - 1][column], bg="#F0F0F0", fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)

            self.tab_control.add(tab4, text='Total item sold      ')

            # tab5
            popular_heading = ["Item Category", "Item name", "Quantity sold"]
            tab5 = Frame(self.tab_control)
            tab5.pack(fill="both")
            # calculate total sale by item category
            info_list = self.get_by_store_id(self.popular_item_sold, store_id)
            # adding table
            for row in range(2):
                for column in range(len(popular_heading)):
                    if row == 0:
                        label = Label(tab5, text=popular_heading[column], bg="#E0E0E0", fg="black", padx=3, pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        tab5.grid_columnconfigure(column, weight=1)
                    else:
                        label = Label(tab5, text=info_list[column], bg="#F0F0F0", fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)

            self.tab_control.add(tab5, text='Popular items sold')
            self.tab_control.pack(fill="both")

    def callback(self, *args):
        store_id = None
        for name in self.controller.get_all_store_name():
            if name[0] == self.variable.get():
                store_id = name[1]
                break
        self.create_tab(store_id)

    def get_by_store_id(self, data, store_id):
        for store in data:
            if store[1] == store_id:
                return store[0]


class InventoryScreen(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        root.title("Inventory")
        self.controller = controller

        self.store_name = self.controller.get_all_store_name()
        self.store_info = self.controller.get_all_store_info()
        self.current_inventory = self.controller.get_all_inventory()
        self.low_inventory = self.controller.get_low_inventory(40)

        # Select Store
        option_list = ["Please chose the store you would like to view "]
        for store in self.store_name:
            option_list.append(store[0])
        self.variable = StringVar(self)
        self.variable.set(option_list[0])

        opt = OptionMenu(self, self.variable, *option_list)
        opt.config(width=90, font=('Helvetica', 12))
        opt.pack()
        self.variable.trace("w", self.callback)
        # init tab
        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')
        self.tab_control = ttk.Notebook(self, style='lefttab.TNotebook')
        self.tab_1 = Frame(self.tab_control)
        self.tab_control.add(self.tab_1, text="Store information         ")
        self.tab_2 = Frame(self.tab_control)
        self.tab_control.add(self.tab_2, text="View current inventory")
        self.tab_3 = Frame(self.tab_control)
        self.tab_control.add(self.tab_3, text="Low inventory items    ")
        self.tab_4 = Frame(self.tab_control)
        self.tab_control.add(self.tab_4, text="Manage inventory        ")
        self.create_tab(None)

    def create_tab(self, store_id):
        self.tab_control.pack_forget()
        if store_id != None:
            # tab
            '''
            style = ttk.Style(self)
            style.configure('lefttab.TNotebook', tabposition='wn')
            self.tab_control = ttk.Notebook(self, style='lefttab.TNotebook')
'''
            # self.tab_1
            store_inventory_heading = ["Store ID", "Address", "Suburb", "State", "Postal Code"]
            # get store info for current store
            info_list = self.get_by_store_id(self.store_info, store_id)
            self.tab_1.forget()
            for row in range(2):
                for column in range(len(store_inventory_heading)):
                    if row == 0:
                        label = Label(self.tab_1, text=store_inventory_heading[column], bg="#E0E0E0", fg="black",
                                      padx=3,
                                      pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        self.tab_1.grid_columnconfigure(column, weight=1)
                    else:
                        label = Label(self.tab_1, text=info_list[column], bg="#F0F0F0", fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)

            # self.tab_2
            inventory_heading = ["Item ID", "Item Name", "Quantity", "Date Inventory Added"]
            self.tab_2.forget()
            # get inventory item info
            info_list = self.get_by_store_id(self.current_inventory, store_id)
            # adding table
            for row in range(len(info_list) + 1):
                for column in range(len(inventory_heading)):
                    if row == 0:
                        label = Label(self.tab_2, text=inventory_heading[column], bg="#E0E0E0", fg="black", padx=3,
                                      pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        self.tab_2.grid_columnconfigure(column, weight=1)
                    else:
                        label = Label(self.tab_2, text=info_list[row - 1][column], bg="#F0F0F0",
                                      fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)

            # self.tab_3
            self.tab_3.forget()
            # load low inventory info
            info_list = self.get_by_store_id(self.low_inventory, store_id)
            # adding table
            for row in range(len(info_list) + 1):
                for column in range(len(inventory_heading)):
                    if row == 0:
                        label = Label(self.tab_3, text=inventory_heading[column], bg="#E0E0E0", fg="black", padx=3,
                                      pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        self.tab_3.grid_columnconfigure(column, weight=1)
                    else:
                        label = Label(self.tab_3, text=info_list[row - 1][column], bg="#F0F0F0",
                                      fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)

            # self.tab_4
            self.tab_4.forget()
            # get inventory item info
            info_list = self.get_by_store_id(self.current_inventory, store_id)
            # adding table
            # self.add_button = [[0 for x in range(10)] for y in range(10)]
            for row in range(len(info_list) + 1):
                for column in range(len(inventory_heading)):
                    if row == 0:
                        label = Label(self.tab_4, text=inventory_heading[column], bg="#E0E0E0", fg="black", padx=3,
                                      pady=3)
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        self.tab_4.grid_columnconfigure(column, weight=1)
                    elif column == 2:
                        label = Label(self.tab_4, text=info_list[row - 1][column], bg="#F0F0F0",
                                      fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=15, pady=1)
                        label.grid_columnconfigure(column, weight=20)
                        quantity = label.cget("text")
                        item_id = info_list[row - 1][0]
                        add_button = Button(self.tab_4, text="+", command=lambda q=quantity, s=store_id,
                                                                                 i=item_id,
                                                                                 t=self.tab_4: self.edit_quantity(0, q,
                                                                                                                  s, i,
                                                                                                                  t))
                        add_button.grid(row=row, column=2, sticky='e')
                        minus_button = Button(self.tab_4, text="-", command=lambda q=quantity, s=store_id,
                                                                                   i=item_id,
                                                                                   t=self.tab_4: self.edit_quantity(1,
                                                                                                                    q,
                                                                                                                    s,
                                                                                                                    i,
                                                                                                                    t))
                        minus_button.grid(row=row, column=2, sticky='w')
                    else:
                        label = Label(self.tab_4, text=info_list[row - 1][column], bg="#F0F0F0",
                                      fg="black")
                        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                        label.grid_columnconfigure(column, weight=1)
            self.tab_control.pack(fill="both")

    def callback(self, *args):
        store_id = None
        for name in self.controller.get_all_store_name():
            if name[0] == self.variable.get():
                store_id = name[1]
                break
        self.create_tab(store_id)

    def get_by_store_id(self, data, store_id):
        for store in data:
            if store[1] == store_id:
                return store[0]

        # edit the quantity

    def edit_quantity(self, button_num, quantity, store_id, item_id, tab):
        button_num = int(button_num)
        quantity = int(quantity)
        if button_num == 0:
            quantity += 1
        else:
            quantity -= 1
        self.controller.edit_inventory_qty(store_id, item_id, quantity)
        self.update_quantity(store_id)

    # update the quantity in an order
    def update_quantity(self, store_id):
        self.current_inventory = self.controller.get_all_inventory()
        self.low_inventory = self.controller.get_low_inventory(40)
        self.create_tab(store_id)


class CreateOrderScreen(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.root = root
        self.controller = controller
        self.root.title("Create Order")

        self.current_inventory = self.controller.get_all_inventory()
        self.item_info = self.controller.current_product_info()
        # get inventory item info
        store_id = 4
        self.inventory_list = self.get_by_store_id(self.current_inventory, store_id)
        self.price_list = self.item_info[1]
        self.quantity_list = self.item_info[2]
        self.item_list = self.item_info[0]
        self.order_name_detail = []
        self.order_quantity_detail = []
        self.order_price = []
        self.order_total_price = []
        self.order_detail = []
        self.new_order_detail = []
        self.index_j = 0
        self.create_frames()

    def create_frames(self):
        self.index_j = 0
        # Creating paned window allows to resize these widgets, by moving the separators in between them
        self.panedwindow = PanedWindow(self, orient=HORIZONTAL)
        self.panedwindow.pack(fill=BOTH, expand=True)

        self.panedwindow.grid_rowconfigure(0, weight=1)
        self.panedwindow.grid_columnconfigure(0, weight=1)

        self._frame = self.panedwindow

        # self.frame1 = ttk.Frame(self.panedwindow, width=700, height=800, relief=SUNKEN)
        self.frame1 = ttk.Frame(self.panedwindow, relief=SUNKEN)
        self.frame1.pack()


        # self.frame2 = ttk.Frame(self.panedwindow, width=900, height=800, relief=SUNKEN)
        self.frame2 = ttk.Frame(self.panedwindow, relief=SUNKEN)
        self.frame2.pack()

        self.create_frame1(None)

        # create labels for item name, price, stock quantity, customer name in frame2.
        item_name_label = Label(self.frame2
                                , text='Item Name')
        item_name_label.place(relx=0.20, rely=0.33, height=20, width=90)
        self.text_name = StringVar()
        self.text_name.set("")
        item_name_value = Label(self.frame2
                                , textvariable=self.text_name)
        item_name_value.place(relx=0.20, rely=0.38, height=20, width=110)

        item_price_label = Label(self.frame2
                                 , text='Price')
        item_price_label.place(relx=0.43, rely=0.33, height=20, width=90)
        self.text_price = IntVar()
        self.text_price.set("")
        item_price_value = Label(self.frame2
                                 , textvariable=self.text_price)
        item_price_value.place(relx=0.48, rely=0.38, height=20, width=70)

        item_stock_label = Label(self.frame2
                                 , text='Stock Quantity')
        item_stock_label.place(relx=0.66, rely=0.33, height=20, width=90)
        self.text_stock = StringVar()
        self.text_stock.set(0)
        item_stock_value = Label(self.frame2
                                 , textvariable=self.text_stock)
        item_stock_value.place(relx=0.66, rely=0.38, height=20, width=90)

        item_qnt_label = Label(self.frame2
                               , text='Quantity')
        item_qnt_label.place(relx=0.85, rely=0.33, height=20, width=90)
        self.ws = IntVar()
        # for increase or decrease the quantity value
        self.w = Spinbox(self.frame2
                         , from_=0, to=1000, textvariable=self.ws).place(relx=0.85, rely=0.38, height=20,
                                                                         width=80)

        customer_name_label = Label(self.frame2
                                    , text='Customer Name')
        customer_name_label.place(relx=0.01, rely=0.60, height=20, width=100)
        self.customer_name_value = Entry(self.frame2
                                         , textvariable="")
        self.customer_name_value.place(relx=0.01, rely=0.65, height=20, width=120)

        # buttons for submit an order or cancel the order.
        Button(self.frame2
               , text='Submit', command=self.submit_order
               ).place(relx=0.66, rely=0.88, height=20, width=50)

        Button(self.frame2
               , text='Cancel', command=self.frame2
               .quit).place(relx=0.80, rely=0.88, height=20, width=50)

        # for searching particular item
        Label(self.frame2
              , text=' Search an item: ').place(relx=0.1, rely=0.05, height=20, width=100)

        # Selecting the particular item and add it to the list.
        Button(self.frame2
               , text='Add Item', command=self.item_details).place(relx=0.7, rely=0.04, height=20, width=80)

        # creating text box
        self.e = Entry(self.frame2
                       )
        h = Label(self.frame2
                  )
        h.grid(row=8, column=3, padx=8, pady=8)

        h.pack()
        self.e.pack()
        self.e.bind('<KeyRelease>', self.check_key)

        # creating list box
        self.lb = Listbox(self.frame2, width=20, height=5)
        self.lb.bind('<<ListboxSelect>>', self.current_select)
        self.lb.pack()
        # update(l)


        self.panedwindow.add(self.frame1)
        self.panedwindow.add(self.frame2)

        self.frame1.grid(row=0, column=1)
        self.frame2.grid(row=0, column=0)

        self.panedwindow.paneconfig(self.frame1, width=630, height=800, sticky=E + W + S + N)
        self.panedwindow.paneconfig(self.frame2, width=570, height=800, sticky=E + W + S + N)

        # self.panedwindow.paneconfig(self.frame2, width=700)


    def create_frame1(self, order_list):

        # create labels for item name, quantity, price per item, total amount in frame1.
        item_name_label2 = Label(self.frame1, text='Item Name')
        item_name_label2.place(relx=0.01, rely=0.06, height=20, width=100)

        item_quantity_label = Label(self.frame1, text='Quantity')
        item_quantity_label.place(relx=0.20, rely=0.06, height=20, width=100)

        item_per_label = Label(self.frame1, text='Price per item')
        item_per_label.place(relx=0.38, rely=0.06, height=20, width=100)

        item_total_label = Label(self.frame1, text='Total')
        item_total_label.place(relx=0.58, rely=0.06, height=20, width=100)

        Total_bill_label = Label(self.frame1, text='Total Amount')
        Total_bill_label.place(relx=0.01, rely=0.60, height=20, width=100)
        self.tot_amt = IntVar()
        self.tot_amt.set(0)
        Total_bill_value = Label(self.frame1, textvariable=self.tot_amt)
        Total_bill_value.place(relx=0.58, rely=0.60, height=20, width=50)

        if order_list is not None and len(order_list) > 0:
            self.count_name = 1
            self.count_quantity = 1
            self.count_price = 1
            self.count_total = 1
            self.total_amount = 0
            # For deleting the particular item or order.
            for name_index in order_list[0]:
                self.index_j = 0.05 * self.count_name
                self.name_label = Label(self.frame1, text=name_index)
                self.name_label.place(relx=0.03, rely=self.index_j + 0.06, height=15, width=70)
                self.delete_button = Button(self.frame1, text='Delete',
                                            command=lambda n=self.name_label.cget("text"): self.delete_order(n))
                self.delete_button.place(relx=0.89, rely=self.index_j + 0.06, height=15, width=50)
                self.add_button = Button(self.frame1, text='+',
                                         command=lambda n=self.name_label.cget("text"),
                                                        b=0: self.edit_order(n,
                                                                             b))
                self.add_button.place(relx=0.31, rely=self.index_j + 0.06, height=15, width=15)

                self.minus_button = Button(self.frame1, text='-',
                                           command=lambda n=self.name_label.cget("text"),
                                                          b=1: self.edit_order(n,
                                                                               b))
                self.minus_button.place(relx=0.19, rely=self.index_j + 0.06, height=15, width=15)
                self.count_name += 1
            # Evaluting quantity, price and Total
            for quantity_index in order_list[1]:
                self.index_j = 0.05 * self.count_quantity
                self.quantity_label = Label(self.frame1, text=quantity_index)
                self.quantity_label.place(relx=0.21, rely=self.index_j + 0.06, height=15, width=70)
                self.count_quantity += 1

            for price_index in order_list[2]:
                self.index_j = 0.05 * self.count_price
                self.price_label = Label(self.frame1, text=price_index)
                self.price_label.place(relx=0.39, rely=self.index_j + 0.06, height=15, width=70)
                self.count_price += 1

            for total_index in order_list[3]:
                self.total_amount += float(total_index)
                self.index_j = 0.05 * self.count_total
                self.total_label = Label(self.frame1, text=total_index)
                self.total_label.place(relx=0.59, rely=self.index_j + 0.06, height=15, width=70)
                self.count_total += 1
            # getting total amount
            self.tot_amt.set(self.total_amount)

    def get_by_store_id(self, data, store_id):
        for store in data:
            if store[1] == store_id:
                return store[0]

    def current_select(self, evt):
        w = evt.widget
        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])
            value = w.get(index)
            # print(value2)
            self.e.delete(0, END)
            self.e.insert(0, value)
            item_index = self.item_info[0].index(value)
            try:
                self.price = self.price_list[item_index]
                self.quantity = self.quantity_list[item_index]
            except IndexError:
                self.price = 0
                self.quantity = 0

            self.text_name.set(value)
            self.text_price.set(int(self.price))
            self.text_stock.set(self.quantity)

    def check_key(self, event):
        value = event.widget.get()
        data = []
        # get data from l
        if value == '':
            data = self.item_list
        else:
            for item in self.item_list:
                if value.lower() in item.lower():
                    data.append(item)
        # update data in listbox
        self.update(data)

    def update(self, data):

        # clear previous data
        self.lb.delete(0, 'end')

        # put new data
        for item in data:
            self.lb.insert('end', item)

    def item_details(self):
        value = str((self.lb.get(ACTIVE)))
        item_index = self.item_info[0].index(value)
        self.price = self.price_list[item_index]
        self.quantity = self.quantity_list[item_index]

        if self.text_name.get() not in self.order_name_detail:
            if self.ws.get() > self.quantity:
                messagebox.showinfo("Exceed Inventory", "Insufficient inventory")
                # messagebox showing warning if there is insufficient inventory
                return
            # fetch details of an item if it is still in the inventory
            else:
                self.order_name_detail.append(self.text_name.get())
                self.order_quantity_detail.append(self.ws.get())
                self.order_price.append(self.text_price.get())
                self.order_total_price.append(str(int(self.text_price.get()) * self.ws.get()) + ".0")
                self.order_detail.append(self.order_name_detail)
                self.order_detail.append(self.order_quantity_detail)
                self.order_detail.append(self.order_price)
                self.order_detail.append(self.order_total_price)
                self.create_frame1(self.order_detail)
        else:
            self.exist_item_index = self.order_name_detail.index(self.text_name.get())
            self.order_detail[1][self.exist_item_index] += self.ws.get()
            self.order_detail[3][self.exist_item_index] = (
                        str(int(self.text_price.get()) * self.order_detail[1][self.exist_item_index]) + ".0")
            self.frame1.destroy()
            self.frame2.destroy()
            self.create_frames()
            self.create_frame1(self.order_detail)

    def submit_order(self):
        self.controller.create_new_order(self.order_name_detail, self.order_quantity_detail,
                                         self.order_total_price, self.customer_name_value.get())
        self.switch_frame(OrderScreen)

    def edit_order(self, name, button):
        self.frame1.destroy()
        self.frame2.destroy()

        # modify an order
        self.modify_quantity = 0
        if button == 0:
            self.modify_quantity = 1
        else:
            self.modify_quantity = -1

        if name:
            self.create_frames()
            self.item_index = self.order_name_detail.index(name)
            self.order_quantity_detail[self.item_index] += self.modify_quantity
            self.order_total_price[self.item_index] = str(
                self.order_quantity_detail[self.item_index] * self.order_price[self.item_index]) + ".0"
            self.new_order_detail.append(self.order_name_detail)
            self.new_order_detail.append(self.order_quantity_detail)
            self.new_order_detail.append(self.order_price)
            self.new_order_detail.append(self.order_total_price)
            self.create_frame1(self.new_order_detail)

    def delete_order(self, name):
        self.frame1.destroy()
        self.frame2.destroy()
        # removing details from the order and creating new one
        if name:
            self.create_frames()
            self.remove_item_index = self.order_name_detail.index(name)
            self.order_name_detail.remove(name)

            self.remove_quantity = self.order_quantity_detail[self.remove_item_index]
            self.order_quantity_detail.remove(self.remove_quantity)

            self.remove_price = self.order_price[self.remove_item_index]
            self.order_price.remove(self.remove_price)

            self.remove_total = self.order_total_price[self.remove_item_index]
            self.order_total_price.remove(self.remove_total)

            self.new_order_detail.append(self.order_name_detail)
            self.new_order_detail.append(self.order_quantity_detail)
            self.new_order_detail.append(self.order_price)
            self.new_order_detail.append(self.order_total_price)
            self.create_frame1(self.new_order_detail)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self.root, self.controller)
        if self._frame is not None:
            # Destroys current frame and replaces with new one
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
