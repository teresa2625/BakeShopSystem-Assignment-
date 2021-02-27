import datetime

class RegisteredUser:
    def __init__(self, user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type):
        self.user_name = user_name
        self.user_password = user_password
        self.store_id = store_id
        self.user_fullname = user_fullname
        self.contact_number = contact_number
        self.user_email = user_email
        self.user_type = user_type

    def set_user_name(self, new_user_name):
        self.user_name = new_user_name

    def get_user_name(self):
        return self.user_name

    def set_contact_number(self, new_contact_number):
        self.contact_number = new_contact_number

    def get_contact_number(self):
        return self.contact_number

    def set_user_password(self, new_user_password):
        self.user_password = new_user_password

    def get_user_password(self):
        return self.user_password

    def set_user_fullname(self, new_user_fullname):
        self.user_fullname = new_user_fullname

    def get_user_fullname(self):
        return self.user_fullname

    def set_user_email(self, new_user_email):
        self.user_email = new_user_email

    def get_user_email(self):
        return self.user_email

    def set_user_type(self, new_user_type):
        self.user_type = new_user_type

    def get_user_type(self):
        return self.user_type


class Owner(RegisteredUser):
    def __init__(self, user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type,
                 owner_id):
        super().__init__(user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type)
        self.owner_id = owner_id

    def set_id(self, new_owner_id):
        self.owner_id = new_owner_id

    def get_id(self):
        return self.owner_id


class Employee(RegisteredUser):
    def __init__(self, user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type,
                 tfn, street_address, postal_code, state, city):
        super().__init__(user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type)
        self.tfn = tfn
        self.street_address = street_address
        self.postal_code = postal_code
        self.state = state
        self.city = city

    def set_tfn(self, new_tfn):
        self.tfn = new_tfn

    def get_tfn(self):
        return self.tfn

    def set_street_address(self, new_street_address):
        self.street_address = new_street_address

    def get_street_address(self):
        return self.street_address

    def set_postal_code(self, new_postal_code):
        self.postal_code = new_postal_code

    def get_postal_code(self):
        return self.postal_code

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state

    def set_city(self, new_city):
        self.city = new_city

    def get_city(self):
        return self.city


class Staff(Employee):
    def __init__(self, user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type,
                 tfn, street_address, postal_code, state, city, staff_id):
        super().__init__(user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type, tfn,
                       street_address, postal_code, state, city)
        self.staff_id = staff_id

    def set_id(self, new_staff_id):
        self.staff_id = new_staff_id

    def get_id(self):
        return self.staff_id


class Manager(Employee):
    def __init__(self, user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type,
                 tfn, street_address, postal_code, state, city, manager_id):
        super().__init__(user_name, user_password, store_id, user_fullname, contact_number, user_email, user_type, tfn,
                       street_address, postal_code, state, city)
        self.manager_id = manager_id

    def set_id(self, new_manager_id):
        self.manager_id = new_manager_id

    def get_id(self):
        return self.manager_id



class Store:
    
    def __init__(self,store_id,store_street_address,store_city,store_suburb,store_contact_number,store_postal):
        self.store_id = store_id
        self.store_street_address = store_street_address
        self.store_city = store_city
        self.store_suburb = store_suburb
        self.store_contact_number = store_contact_number
        self.store_postal = store_postal
        self.inventory_list = []
        self.order_list = []

    def get_low_inventory_item(self, amount):
        item_list = []
        for item in self.inventory_list:
            if item.get_quantity() < amount:
                item_list.append(item)
        return item_list


    def set_store_id(self,new_store_id):
        self.store_id = new_store_id

    def get_store_street_address(self):
        return self.store_street_address

    def get_store_id(self):
        return self.store_id

    def get_store_city(self):
        return self.store_city

    def get_store_suburb(self):
        return self.store_suburb

    def get_store_contact_number(self):
        return self.store_contact_number

    def get_store_postal(self):
        return self.store_postal

    def set_store_street_address(self,new_store_street_address):
        self.store_street_address = new_store_street_address

    def set_store_city(self,new_store_city):
        self.store_city = new_store_city

    def set_store_suburb(self,new_store_suburb):
        self.store_suburb = new_store_suburb

    def set_store_contact_number(self,new_store_contact_number):
        self.store_contact_number = new_store_contact_number

    def set_store_postal(self,new_store_postal):
        self.store_postal = new_store_postal

    def get_order_list(self):
        return self.order_list

    def get_inventory_list(self):
        return self.inventory_list

    def set_order_list(self,new_order_list):
        self.order_list = new_order_list

    def set_inventory_list(self,new_inventory_list):
        self.inventory_list = new_inventory_list
    
    def add_inventory(self, inventory):
        self.inventory_list.append(inventory)
    
    def add_order(self, order):
        self.order_list.append(order)

    def search_inventory_by_name(self, new_inventory_item):
        inventory_item = new_inventory_item.strip()
        for i in self.inventory_list:
            if inventory_item == i.get_name_of_item():
                return i
        return False
    
    def search_inventory_by_id(self, inventory_id):
        for i in self.inventory_list:
            if inventory_id == i.get_inventory_item_id():
                return i
        return False


class Inventory:
    def __init__(self,inventory_item_id,name_of_item,quantity,date_inventory_added):
        self.inventory_item_id = inventory_item_id
        self.name_of_item = name_of_item.strip()
        self.quantity = int(quantity)
        self.date_inventory_added = date_inventory_added

    def get_inventory_item_id(self):
        return self.inventory_item_id

    def set_item_id(self,new_item_id):
        self.inventory_item_id = new_item_id

    def get_name_of_item(self):
        return self.name_of_item

    def set_quantity(self,new_quantity):
        self.quantity = new_quantity

    def get_quantity(self):
        return self.quantity

    def set_date_inventory_added(self,new_date_inventory_added):
        self.date_inventory_added = new_date_inventory_added

    def get_date_inventory_added(self):
        return self.date_inventory_added



class Item:
    def __init__(self,item_name,item_id,item_price):
        self.item_name = item_name.strip()
        self.item_id = item_id
        self.item_price = float(item_price)

    def get_item_name(self):
        return self.item_name

    def get_item_id(self):
        return self.item_id

    def get_item_price(self):
        return self.item_price

    def set_item_name(self,new_item_name):
        self.item_name = new_item_name

    def set_item_id(self,new_item_id):
        self.item_id = new_item_id

    def set_item_price(self,new_item_price):
        self.item_price = new_item_price
    

class Order:
    def __init__(self,store_id,order_id,staff_id,order_item,quantity_of_items,price,order_time,customer_name,order_status):
        self.store_id = store_id
        self.order_id = order_id
        self.staff_id = staff_id
        self.order_item = None
        self.set_order_item(order_item)
        self.quantity_of_items = None
        self.set_quantity_of_items(quantity_of_items)
        #calculate it in the class?
        self.price = None
        self.set_price(price)
        self.order_time = None
        self.set_order_time(order_time)
        self.customer_name = customer_name
        self.order_status = order_status
    
    def get_order_total(self):
        return sum(self.price)

    def set_quantity_of_items(self,new_quantity_of_items):
        quantity_list = []
        for i in new_quantity_of_items:
            i.replace(" ","")
            quantity_list.append(int(i))
        self.quantity_of_items = quantity_list

    def get_quantity_of_items(self):
        return self.quantity_of_items
    
    def get_quantity_of_items_data_format(self):
        temp = [str(item) for item in self.quantity_of_items]
        return ",".join(temp)
    
    def set_price(self,new_price):
        item_price_list = []
        for i in new_price:
            i.replace(" ","")
            item_price_list.append(float(i))
        self.price = item_price_list
    
    def get_price(self):
        return self.price

    def get_price_data_format(self):
        temp = [str(item) for item in self.price]
        return "|".join(temp)

    def set_order_item(self,new_order_item):
        item_list = []
        for i in new_order_item:
            item_list.append(i.strip())
        self.order_item = item_list

    def get_order_item(self):
        return self.order_item
    
    def get_order_item_data_format(self):
        return ",".join(self.order_item)

    def get_store_id(self):
        return self.store_id

    def set_store_id(self,new_store_id):
        self.store_id = new_store_id

    def set_order_id(self,new_order_id):
        self.order_id = new_order_id

    def get_order_id(self):
        return self.order_id

    def set_staff_id(self, new_staff_id):
        self.staff_id = new_staff_id
    
    def get_staff_id(self):
        return self.staff_id
        
    #get item from item class?
    def get_item(self):
        return

    def set_customer_name(self,new_customer_name):
        self.customer_name = new_customer_name

    def get_customer_name(self):
        return self.customer_name

    def set_order_time(self,new_order_time):
        order_time_str = new_order_time[0] + " " + new_order_time[1]
        order_date_time = datetime.datetime.strptime(order_time_str, '%m/%d/%Y %H:%M')
        self.order_time = order_date_time

    def get_order_time(self):
        return self.order_time
    
    def get_order_date_data_format(self):
        date = str(self.order_time.date())
        date = date.split("-")
        date.reverse()
        temp = str(int(date[0]))
        date[0] = str(int(date[1]))
        date[1] = temp
        return "/".join(date)
    
    def get_order_time_data_format(self):
        time = str(self.order_time.time())
        time = time.split(":")
        del(time[-1])
        return ":".join(time)

    def set_order_status(self,new_order_status):
        self.order_status = new_order_status

    def get_order_status(self):
        return self.order_status

    #add item to the order
    def add_item(self):
        return

    def update_quantity(self):
        return

    def del_item(self):
        return

    def calc_total_amount(self):
        return

class AdvancedOrder(Order):
    def __init__(self,store_id,order_id,staff_id,order_item,quantity_of_items,price,order_time,customer_name,order_status,pick_up_date,customer_contact_number):
        super().__init__(store_id,order_id,staff_id,order_item,quantity_of_items,price,order_time,customer_name,order_status)
        self.pick_up_date = pick_up_date
        self.customer_contact_number = customer_contact_number

    def set_pick_up_date(self,new_pick_up_date):
        self.pick_up_date = new_pick_up_date

    def set_customer_contact_number(self,new_customer_contact_number):
        self.customer_contact_number = new_customer_contact_number

    def get_pick_up_date(self):
        return self.pick_up_date

    def get_customer_contact_number(self):
        return self.customer_contact_number

    