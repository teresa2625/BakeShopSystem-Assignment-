from Model import *
from View import *
import csv
import tkinter as tk
import datetime
from dateutil.relativedelta import *


class BakeShopSystemController:
    def __init__(self):
        # specify category of item
        self.coffee = ["ice coffee","espresso","cappuccino","ice latte" ]
        self.food = ["white bread","cucumber Sandwich","plain pancake","barros Luco Sandwich","texas brisket sandwich","broodje kroket sandwich","multigrain bread","chicken burger","toast skagen","red velvet cake","lamb burger","charcoal bread","fries burger","gatsby sandwich","vanilla cake","bocadillo de atun sandwich","banana pancake","yakisoba pan","potato pancake","rye break","dinner role","raspberry cake","crumb apple muffins","veggie burger","fish burger","chocolate chip pancake","runza sandwich","fat sandwich","lemon crumb muffins","tiramisu cake","banana blueberry muffins","spicy chicken burger","rainbow cake","blueberry muffins","panbazo sandwich","nutella cake","blueberry pancake","double fish fillet burger","chocolate cake"]
        self.drinks = ["lemonade","fanta","coke","water","pepsi"]
        self.coffee_bean = ["roast coffee beans"]
        # load account info and create users
        
        self.user_collection = self.create_user()
        # load store info
        self.store_collection = self.create_store()
        # load item info
        self.item_collection = self.create_item()
        # load inventory info
        self.create_inventory()
        # load order info
        self.create_order()
        self.current_store = 4
        self.current_user = None
        # load login page
        self.root = tk.Tk()
        self.view = LoginScreen(self.root, self)
        self.root.geometry("1200x800")
        self.root.title("Please Login")
        self.root.mainloop()
    ######################################## Load Info From Data Files ####################################

    def create_store(self):
        f = open("./data/store_info.csv", "r")
        reader = csv.reader(f)
        store_info = []
        for row in reader:
            store_info.append(row)
        f.close()
        del store_info[0]
        store_collection = []
        for store in store_info:
            temp = Store(int(store[0]),store[1],store[2],store[3],store[5],store[4])
            store_collection.append(temp)
        return store_collection


    def create_user(self):
        f = open("./data/account_info.csv", "r")
        reader = csv.reader(f)
        user_info = []
        for row in reader:
            user_info.append(row)
        f.close()
        del user_info[0]
        user_collection = []
        for user in user_info:
            if user[4] == "Manager":
                temp = Manager(user[12], user[3], user[11], user[1], user[10], user[2], user[4],
                 user[5], user[6], user[9], user[8], user[7], user[0])
                user_collection.append(temp)
            elif user[4] == "Staff":
                temp = Staff(user[12], user[3], user[11], user[1], user[10], user[2], user[4],
                 user[5], user[6], user[9], user[8], user[7], user[0])
                user_collection.append(temp)
            elif user[4] == "Owner":
                temp = Owner(user[12], user[3], user[11], user[1], user[10], user[2], user,
                 user[0])
                user_collection.append(temp)
        return user_collection
    

    def create_item(self):
        f = open("./data/item_info.csv", "r")
        reader = csv.reader(f)
        item_info = []
        for row in reader:
            item_info.append(row)
        f.close()
        del item_info[0]
        item_collection = []
        for item in item_info:
            temp = Item(item[1],item[0],item[2])
            item_collection.append(temp)
        return item_collection


    def create_inventory(self):
        f = open("./data/inventory_info.csv", "r")
        reader = csv.reader(f)
        inventory_info = []
        for row in reader:
            inventory_info.append(row)
        f.close()
        del inventory_info[0]
        for inventory in inventory_info:
            temp_store_list = inventory[0].split("|")
            temp = Inventory(inventory[1],inventory[2],inventory[3],inventory[4])
            for store_id in temp_store_list:
                self.add_inventory(temp, store_id)
    

    def add_inventory(self, inventory, store_id):
        for store in self.store_collection:
            if store.get_store_id() == int(store_id):
                store.add_inventory(inventory)


    def create_order(self):
        f = open("./data/order_info.csv", "r")
        reader = csv.reader(f)
        order_info = []
        for row in reader:
            order_info.append(row)
        f.close()
        del order_info[0]
        for order in order_info:
            temp = Order(order[0],order[1],order[2],order[3].split(","),order[4].split(","),order[5].split("|"),[order[7],order[8]],order[9], order[10])
            self.add_order(temp, order[0])
            
    
    def add_order(self, order, store_id):
        for store in self.store_collection:
            if store.get_store_id() == int(store_id):
                store.add_order(order)


    # verify login inforation
    def verify_user(self, user_name, password):
        # search user name from registered user
        for user in self.user_collection:
            # verify password according to user name
            if user.get_user_name() == user_name:
                if user.get_user_password() == password:
                    return (True, user)
                else:
                    return (False, "unmatched username or password")
        return (False, "username do not exist")
    
    ####################################### Login ########################################

    def login(self, user_name, password):
        status = self.verify_user(user_name, password)
        if status[0] == True:
            self.root.destroy()
            self.current_user = status[1]
            self.root = tk.Tk()
            self.view = MainScreen(self.root, self)
            self.root.geometry("1200x800")
            self.root.title("Welcome To The Bake Shop System")
            self.root.mainloop()
        else:
            return False
    
    def get_current_user(self):
        return self.current_user
    ####################################### Create New Order ###########################################

    def current_product_info(self):
        product_info = [[], [], []]
        current_store = self.get_store_by_id(self.current_store)
        for item in self.item_collection:
            inventory = current_store.search_inventory_by_name(item.get_item_name())
            product_info[0].append(item.get_item_name())
            product_info[1].append(item.get_item_price())
            if inventory != False:
                product_info[2].append(inventory.get_quantity())
            else:
                product_info[2].append(0)
        return product_info


    def generate_order_id(self):
        f = open("./data/order_info.csv", "r")
        reader = csv.reader(f)
        order_info = []
        for row in reader:
            order_info.append(row)
        f.close()
        # delete the first line of csv file
        del(order_info[0])
        # get the greatest order id
        current = 0
        for order in order_info:
            if current < int(order[1]):
                current = int(order[1])
        new_id = current + 1
        return new_id
    
    def get_current_datetime(self):
        current = str(datetime.date.today())
        current = current.split("-")
        current.reverse()
        temp = str(int(current[0]))
        current[0] = str(int(current[1]))
        current[1] = temp
        date = "/".join(current)
        current = str(datetime.datetime.today().time())
        current = current.split(":")
        del(current[-1])
        time = ":".join(current)
        return [date, time]

    def create_new_order(self, ordered_item, item_qty, price, customer_name):
        temp = [str(item) for item in item_qty[:]]
        item_qty_str = temp
        temp = [str(item) for item in price[:]]
        price_str = temp
        # change later depend on what type of
        new_order = Order(self.current_store,self.generate_order_id(),self.current_user.get_id(),ordered_item,item_qty_str,price_str,self.get_current_datetime(),customer_name,"Preparing")
        # add new order to store
        self.add_order(new_order, self.current_store)
        self.update_order_data()
        # reduce quantity of item in inventory
        current_store = self.get_store_by_id(self.current_store)
        for i in range (len(ordered_item)):
            inventory_item = current_store.search_inventory_by_name(ordered_item[i])
            temp_qty = inventory_item.get_quantity()
            current_qty = temp_qty - item_qty[i]
            inventory_item.set_quantity(current_qty)
        self.update_inventory_data()
        return new_order
    
    ################################### Report Part#################################

    def get_all_store_name(self):
        store_name_list = []
        for store in self.store_collection:
            store_name = "Store" + str(store.get_store_id()) + ": " + store.get_store_street_address() + ", " + store.get_store_city()
            store_name_list.append([store_name, store.get_store_id()])
        return store_name_list
    
    def get_all_store_info(self):
        store_info_list = []
        for store in self.store_collection:
            temp = []
            temp.append(store.get_store_id())
            temp.append(store.get_store_street_address())
            temp.append(store.get_store_city())
            temp.append(store.get_store_suburb())
            temp.append(store.get_store_postal())
            store_info_list.append([temp, store.get_store_id()])
        return store_info_list
    
    def find_item_quantity_sold(self, item_name):
        quantity_list = []
        last_month = datetime.datetime.today() - relativedelta(months=1)
        for store in self.store_collection:
            count = 0
            for order in store.get_order_list():
                if item_name in order.get_order_item() and order.get_order_time() >= last_month:
                    count += order.get_quantity_of_items()[order.get_order_item().index(item_name)]
            quantity_list.append([count, store.get_store_id()])
        return quantity_list
    
    # take make of category (coffee/food/drinks/coffee bean)
    def total_item_sold_by_category(self, category_name):
        item_qty_list = []
        item_count = []
        temp = []
        if category_name == "coffee":
            item_count = self.coffee
        elif category_name == "foods":
            item_count = self.food
        elif category_name == "drinks":
            item_count = self.drinks
        elif category_name == "coffee bean":
            item_count = self.coffee_bean
        for item in item_count:
            temp.append(self.find_item_quantity_sold(item))
        item_qty_list = temp[0][:]
        for i in range (1, len(temp)):
            for idx in range (len(item_qty_list)):
                item_qty_list[idx][0] += temp[i][idx][0]
        # add food to complete the list
        for store in item_qty_list:
            store[0] = [category_name, store[0]]
        return item_qty_list
    
    # take make of category (coffee/food/drinks/coffee bean)
    def type_of_item_sold_by_category(self, category_name):
        item_qty_list = []
        item_count = []
        temp = []
        if category_name == "coffee":
            item_count = self.coffee
        elif category_name == "foods":
            item_count = self.food
        elif category_name == "drinks":
            item_count = self.drinks
        elif category_name == "coffee bean":
            item_count = self.coffee_bean
        for item in item_count:
            temp.append(self.find_item_quantity_sold(item))
        item_qty_list = temp[0][:]            
        for idx in range (len(item_qty_list)):
            item_qty_list[idx][0] = [item_qty_list[idx][0]]
            for i in range (1, len(temp)):
                item_qty_list[idx][0].append(temp[i][idx][0])
        
        for idx in range (len(item_qty_list)):
            if max(item_qty_list[idx][0]) != 0:
                item_qty_list[idx][0] = [category_name, item_count[item_qty_list[idx][0].index(max(item_qty_list[idx][0]))], max(item_qty_list[idx][0])]
            else:
                item_qty_list[idx][0] = [category_name, "No order last week", 0]
        return item_qty_list
    
    def day_made_most_sale(self, end_date):
        day_made_most_sale_list = []
        current = end_date
        day_list = []
        for i in range (8):
            day_list.append(current - relativedelta(days=i))
        for store in self.store_collection:
            temp = []
            for i in range (len(day_list) - 1):
                sale = 0
                for order in store.get_order_list():
                    if order.get_order_time() < day_list[i] and order.get_order_time() >= day_list[i + 1]:
                        sale += order.get_order_total()
                temp.append(sale)
            sorted_temp = temp[:]
            sorted_temp.sort()
            if sorted_temp[-1] > 0:
                temp_day = day_list[temp.index(sorted_temp[-1])] - relativedelta(days=1)
                temp_day = str(temp_day.date())
                day_made_most_sale_list.append([[temp_day, sorted_temp[-1]], store.get_store_id()])
            else:
                day_made_most_sale_list.append([["No order for the week", sorted_temp[-1]], store.get_store_id()])
        return day_made_most_sale_list
    
    def day_of_week_of_last_month_made_most_sale(self):
        temp_collection = []
        current = datetime.datetime.today()
        for i in range (4):
            temp = self.day_made_most_sale(current)
            temp_collection.append(temp)
            current -= relativedelta(days=7)
        return_data = temp_collection[0]
        for idx in range (len(return_data)):
            return_data[idx][0] = [temp_collection[0][idx][0], temp_collection[1][idx][0], temp_collection[2][idx][0], temp_collection[3][idx][0]]
        return return_data
        

    def total_sale_last_month(self):
        total_sale_list = []
        last_month = datetime.datetime.today() - relativedelta(months=1)
        for store in self.store_collection:
            total_sale = 0
            for order in store.get_order_list():
                if order.get_order_time() >= last_month:
                    total_sale += order.get_order_total()
            total_sale_list.append([total_sale, store.get_store_id()])
        return total_sale_list
    ################################## inventory #######################################

    def get_store_by_id(self, store_id):
        for store in self.store_collection:
            if store.get_store_id() == store_id:
                return store
        return False

    # take the amount if less than the amount, considered as low inventory
    def get_low_inventory(self, amount):
        low_inventory_collection = []
        for store in self.store_collection:
            temp = []
            for item in store.get_low_inventory_item(amount):
                temp.append([item.get_inventory_item_id(), item.get_name_of_item(), item.get_quantity(), item.get_date_inventory_added()])
            low_inventory_collection.append([temp, store.get_store_id()])
            # low_inventory_collection.append([store.get_low_inventory_item(amount), store.get_store_id()])
        return low_inventory_collection

    def get_all_inventory(self):
        inventory_list = []
        for store in self.store_collection:
            inventory_collection = store.get_inventory_list()
            output = []
            for item in inventory_collection:
                temp = []
                temp.append(item.get_inventory_item_id())
                temp.append(item.get_name_of_item())
                temp.append(item.get_quantity())
                temp.append(item.get_date_inventory_added())
                output.append(temp)
            inventory_list.append([output, store.get_store_id() ])
        return inventory_list
    
    def edit_inventory_qty(self, store_id, inventory_id, qty):
        print(qty)
        current_store = self.get_store_by_id(store_id)
        current_inventory = current_store.search_inventory_by_id(inventory_id)
        current_inventory.set_quantity(qty)
        current_inventory.set_date_inventory_added(self.get_current_datetime()[0])
        self.update_inventory_data()
    

    ########################### save object info to csv file #################################
    def update_inventory_data(self):
        data = [["store id", "item id", "name of item", "quantity", "date inventory added"]]
        for store in self.store_collection:
            for inventory in store.get_inventory_list():
                temp = []
                temp.append(store.get_store_id())
                temp.append(inventory.get_inventory_item_id())
                temp.append(inventory.get_name_of_item())
                temp.append(inventory.get_quantity())
                temp.append(inventory.get_date_inventory_added())
                data.append(temp)
        with open('./data/inventory_info.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        return data

    
    def update_order_data(self):
        data = [["store id", "order id", "staff id", "name of item", "quantity", "price", "total amount", "date", "time", "customer name", "order status", "customer phone number"]]
        for store in self.store_collection:
            for order in store.get_order_list():
                temp = []
                temp.append(order.get_store_id())
                temp.append(order.get_order_id())
                temp.append(order.get_staff_id())
                temp.append(order.get_order_item_data_format())
                temp.append(order.get_quantity_of_items_data_format())
                temp.append(order.get_price_data_format())
                temp.append(str(order.get_order_total()))
                temp.append(order.get_order_date_data_format())
                temp.append(order.get_order_time_data_format())
                temp.append(order.get_customer_name())
                temp.append(order.get_order_status())
                temp.append("")
                data.append(temp)
        with open('./data/order_info.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        return data


if __name__ == "__main__":
    # just for testing
    controller = BakeShopSystemController()
    # print(controller.store_collection[0].order_list[0].order_time)
    #print(controller.day_made_most_sale(datetime.datetime.today()))
    # order = controller.create_new_order(["ice coffee", "coke"], [1,2], [3.5, 4.8], "Adam Liang")
    #print(order.get_order_id())