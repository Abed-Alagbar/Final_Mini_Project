# Import libraries
import csv
import time
from datetime import datetime
import pandas as pd
import pymysql
import os
from dotenv import load_dotenv


calculate_list = []
global total_price

orders = {}
order_number = 0
# creat list for customer to make order
customer_order = []
#couriers_list = ['uber', 'deliveroo', 'just eat']


#function to print the items in the menu
def print_products():
    #print the product list from the database
    insert_product_into_db()
    # Execute SQL query
    cursor.execute(
        'SELECT product_list_id, product_name, product_price FROM product_list')
    # Gets all rows from the result
    rows = cursor.fetchall()
    for row in rows:
        print(f'product id: {(row[0])}\n product name: {row[1]} \
                \n product price: £{row[2]}')
        print('-------------------------')

# function edite the product
def product():
    #print the products
    print_products()

    print('Enter 1 to add a product','\n','2 to delete','\n', '0 to retuen to Main page')
    u_input = input()
    u_input = int(u_input)
    if u_input == 1:
        print('Please Enter Product Name')
        new_product_Name = input()
        new_product_Name = str(new_product_Name)
        print('Please Enter product Price')
        new_product_Price = input()
        new_product_Price = float(new_product_Price)

        insert_product_into_db()
        sql = "INSERT INTO product_list (product_name,product_price) VALUES (%s, %s)"
        val = (new_product_Name, new_product_Price)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()

        print('The new product is added successfully')
        #print the product list from the database
        insert_product_into_db()
        # Execute SQL query
        cursor.execute('SELECT * FROM product_list WHERE product_list_id = \
                (SELECT max(product_list_id) FROM product_list)')
        # Gets all rows from the result
        last_entery = cursor.fetchall()
        for row in last_entery:
            print(f'product id: {(row[0])}\n product name: {row[1]} \
                \n product price: £{row[2]}')
        print('-------------------------------------')
    elif u_input == 2:
        print_products()
        print('Enter id number of the product you wolud like to DELETE')
        delete_product = input()
        delete_product = int(delete_product)
        sql = ('DELETE FROM product_list WHERE product_list_id = %s')
        cursor.execute(sql, delete_product)
        connection.commit()
        print('\n','Number of rows deleted', cursor.rowcount)
        cursor.close()
        connection.close()
    elif u_input == 0:
        main_page()
    else:
        print('Please Enter 1 to add or 0 to main page')


#exit function to end the program
def exit():
    string = 'See you later :)  '
    for i in string:
        # printing each character of the message
        # In Python, files are automatically flushed while closing them.
        # However, a programmer can flush a file before closing it by using the flush() method.
        print(i, end='', flush=True)
        # adding time delay of half second to print each character
        time.sleep(0.3)
    quit()


#make order function
def make_order():
    global order_number
    print("Enter Customer's Name")
    global customer_name
    customer_name = input()
    print('Enter Address')
    customer_address = input()
    print('Enter your phone number')
    customer_phone = input()
    order_number = order_number+1
    orders[order_number] = [customer_name,
                            customer_address, customer_phone]
    print('\n', '            **** Add item to your Order ****',
          '\n', '                 ***********************')

    #insert data to the database
    insert_product_into_db()
    sql = "INSERT INTO customers(Customer_Name,Customer_Address,Customer_PhoneNo)VALUES (%s,%s,%s)"
    val = (customer_name, customer_address, customer_phone)
    cursor.execute(sql, val)
    connection.commit()
    global last_customer_id
    last_customer_id = cursor.lastrowid
    cursor.close()
    connection.close()

    #print product list
    print('Product in the Menu:', '\n', '----------------')
    #print the products
    print_products()
    #call order function
    order()


#add & delet item function
def add_delet_status_item():
    # while loop to add items to the list
    # until finish will inter 0 to break the while loop
    while 1:
        print('\n', 'Enter the number of the item you would like to add',
              '\n', 'Or 0 to stop')
        #user enter product number
        global p_id
        p_id = input()
        p_id = int(p_id)
        
        insert_product_into_db()
        # Execute SQL query
        cursor.execute('SELECT product_list_id FROM product_list')
        # Gets all rows from the result
        row = list(cursor.fetchall())
        #creat a list to put the id from database inside it 
        #and check if the id and the product is exist
        product_id_list = []
        for each in row:
            for field in each:
                product_id_list.append(field)
        #print(product_id_list)
        
        #add item to the list if it is exist
        if p_id in product_id_list:
            # user enter the quantity
            print('Enter quantity')
            p_quantity = input()
            p_quantity = int(p_quantity)
            #insert data to the database
            insert_product_into_db()
            sql = "INSERT INTO order_item(product_list_id,customer_id,quantity)\
            VALUES(%s,%s,%s)"
            val = (p_id,last_customer_id,p_quantity)
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
            connection.close()

            #calculate the total price for all products added
            insert_product_into_db()
            # Execute SQL query
            sql1 = "SELECT product_price FROM product_list WHERE product_list_id = %s"
            cursor.execute(sql1,p_id)
            connection.commit()
            cursor.close()
            connection.close()

            #Gets all rows from the result
            new_row = list(cursor.fetchall())
            #creat a list to put the product price from database inside it
            global total_price
            total_price = 0.0
            for each in new_row:
                for field in each:
                    calculate_list.append(field)
            print(calculate_list)
            for i in calculate_list:
                print('£', i)
                total_price = i+total_price
            print('Total Price: £', total_price)


        #if user enter 0 break and go out of the add product
        elif p_id == 0:
            break
        else:
            print('\n', 'Please Enter valid item number', '\n')
            continue

    print('Final Total Price: £', total_price)

    #confirm order
    print('\n', 'Enter 1 to Confirm 2 to delete an items')
    confirm_item = input()
    confirm_item = int(confirm_item)
    if confirm_item == 1:
        # add the time of the order
        now = datetime.now()
        global order_time
        order_time = now.strftime("%H:%M")
        order_time = str(order_time)
        global order_day
        order_day = now.strftime("%d:%m:%y")
        order_day = str(order_day)
        confirm_order_status()
        couriers()

        #insert data to the database
        insert_product_into_db()
        sql_2 = "INSERT INTO `order`(customer_id,total,order_status,order_courier,order_date,order_time)\
            VALUES(%s,%s,%s,%s,%s,%s)"
        val_2 = (last_customer_id, total_price,status_now,courier_name,order_day, order_time)
        cursor.execute(sql_2, val_2)
        connection.commit()
        cursor.close()
        connection.close()
        print('\n----------------Make a new order------------------\n')
    #delete items from the list
    elif confirm_item == 2:
        # while loop to delet items from the list
        # when finish enter stop
        while 1:
            print('\n', 'Enter name of item you would like to delete',
                  '\n', 'Or STOP to finish')
            delete_item = input()
            # make the enter from user string
            delete_item = str(delete_item)
            # make the enter from the user lower case
            delete_item = delete_item.lower()
            # if the user enter stop the loop will break
            if delete_item == 'stop':
                break
            elif delete_item in customer_order:
                print(' ')


            else:
                print('\n', 'Please Enter STOP to finish Your Order', '\n',
                      'Or Make sure to enter the name of the item you would like to DELETE')
                continue
        #Confirm the order
        print('\n', 'Your Order: ', ', '.join(customer_order), '\n', '\n',
              'Enter 1 to Confirm 2 to go to the main page')
        confirm_item = input()
        confirm_item = int(confirm_item)
        if confirm_item == 1:
            confirm_order_status()
            couriers()
        else:
            main_page()


#make order function
def order():
    print('\n', 'Would you like to make order:',
          '\n', 'If yes Enter 1', 'If No Enter 2')
    order = input()
    order = int(order)
    if order == 1:
        add_delet_status_item()
    else:
        main_page()

# confirm order status
def confirm_order_status():
    while True:
        order_status = {1: "Preparing", 2: "Awaiting Pickup",
                        3: "Out-for-Delivery", 4: "Delivered"}
        print('Enter the number of order status:', '\n', '----------------')
        for key, value in order_status.items():
            print("Number: {} , Status:{}".format(key, value))
        order_status_now = input()
        order_status_now = int(order_status_now)

        if order_status_now in order_status.keys():
            print('Status ',order_status[order_status_now], ' added to the order')
            global status_now 
            status_now = str(order_status[order_status_now])
            print(status_now)
            break
        else:
            print("Please Enter valid status Number from (1 to 4)")
            continue

# order_status (to edit and change order status)
def edit_order_status():
    while True:
        print('Please Enter Order Number: ')
        ord_number = input()
        ord_number = int(ord_number)
        if ord_number in orders.keys():
            print('', 'Order Details:', '\n', orders[ord_number])
            print('TO CHANGE ORDER STATUS ENTER 1')
            ord_change = input()
            ord_change = int(ord_change)
            if ord_change == 1:
                print('Enter the number of order status:',
                      '\n', '----------------')
                order_status = {1: "Preparing", 2: "Awaiting Pickup",
                                3: "Out-for-Delivery", 4: "Delivered"}
                for key, value in order_status.items():
                    print("Number : {} , Item Name :{}".format(key, value))
                order_status_now = input()
                order_status_now = int(order_status_now)
                orders[ord_number][5] = order_status[order_status_now]
                print('\n', 'New Order Details:', '\n', orders[ord_number])
            else:
                main_page()
        else:
            print('This order number in not exist')
            continue



def print_courier():
    insert_product_into_db()
    # Execute SQL query
    cursor.execute('SELECT * FROM courier')
    # Gets all rows from the result
    result = cursor.fetchall()
    global couriers_list
    couriers_list = []
    for row in result:
        print(f'courier id: {(row[0])}\n courier name: {row[1]}')
        print('-------------------------------------')
        couriers_list.append(row[1])
    connection.commit()
    cursor.close()
    connection.close()


# couriers
def couriers():
    while True:
        print('Couriers Available:', '\n', '----------------')
        #print the courier list from the database
        print_courier()
            
        print('Enter 1 to add a courier to your order', '\n',
                '2 to ADD new courier to the database','\n',
                '3 to DELETE courier from the database', '\n',
                '0 to retuen to Main page','\n')
        courier_input = input()
        courier_input = int(courier_input)
        if courier_input == 1:
            print('\n', 'Enter the name of the couriers:')
            global courier_name
            courier_name = str(input())
            courier_name = courier_name.lower()
            if courier_name in couriers_list:
                print(f'Courier {courier_name} added to the order')
                break
            else:
                print('Please Enter Courier name From Couriers List')
                #couriers()

        elif courier_input == 2:
            print('Please courier Name')
            new_courier_Name = input()
            new_courier_Name = str(new_courier_Name)
            print('Please Enter product Price')
            # insert to the database
            insert_product_into_db()
            sql = "INSERT INTO courier (courier_name) VALUES ( %s)"
            val = (new_courier_Name)
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
            connection.close()
            print_courier()
        
        elif courier_input == 3:
            print_courier()
            print('Enter courier number would you like to DELETE')
            delete_courier = input()
            delete_courier = int(delete_courier)
            sql = ('DELETE FROM courier WHERE courier_name = %s')
            cursor.execute(sql, delete_courier)
            connection.commit()
            print('\n','Number of rows deleted', cursor.rowcount)
            cursor.close()
            connection.close()

        elif courier_input == 0:
            main_page()

        else:
            print("Please Enter valid status Number from (1 to 4)")
            continue


#read funcation
def read_file():

    #df = pd.read_csv('G:\Generation\mini_project\order_file.csv')
    #print(df.to_string())
    # opening the CSV file
    with open('G:\Generation\mini_project\order_file.csv', mode='r')as file:
        #reading the CSV file
        csvFile = csv.reader(file)
    #displaying the contents of the CSV file
        for lines in csvFile:
            print(lines)

# main page function
def main_page():
    while True:
        print('\n')
        print("Inter Number of the page", '\n',
              "******* 1    Main Page  ", '\n',
              "******* 2    Product    ", '\n',
              "******* 3    Couriers   ", '\n',
              "******* 4    Make an Order ", '\n',
              "******* 5    Order Status ", '\n',
              "******* 6    Exit", '\n',
              "******* 7    Read the Data")
        x = input('Enter Number: ')
        x = int(x)
        if x == 1:
            print('main')
            main_page()
            break
        elif x == 2:
            product()

        elif x == 3:
            print('couriers')
            break
        elif x == 4:
            make_order()
            break
        elif x == 5:
            edit_order_status()
            break
        elif x == 6:
            exit()
            break
        elif x == 7:
            read_file()
            break
        else:
            print(
                '\n', 'Please Enter Valid number of the page you would like to access', '\n')
            continue


#fubnction to insert data to the data base
def insert_product_into_db():
       #Load environment variables from .env file
    load_dotenv()
    host = os.environ.get("mysql_host")
    user = os.environ.get("mysql_user")
    password = os.environ.get("mysql_pass")
    database = os.environ.get("mysql_db")

    # Establish a database connection
    global connection
    connection = pymysql.connect(
    host,
    user,
    password,
    database
    )
    #A cursor is an object that represents a DB cursor,
    #which is used to manage the context of a fetch operation.
    global cursor
    cursor = connection.cursor()


#call main page function
while 1:
    #welcome message
    string = "Welcome to CAFE \n I hope you have a nice day"
    for i in string:
        # printing each character of the message
        # In Python, files are automatically flushed while closing them.
        # However, a programmer can flush a file before closing it by using the flush() method.
        print(i, end='', flush=True)
        # adding time delay of half second to print each character
        time.sleep(0.2)
    main_page()
