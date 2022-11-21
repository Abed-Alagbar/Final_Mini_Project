# Import libraries
import csv
import time
from datetime import datetime
import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

# CREATE products list as a dictionary
product_list = {1: ('Egg Sandwich', 4.50), 2: ('Chicken Sandwich', 5.90),
                3: ('Fish Sandwich', 5.50), 4: ('Cheese Sandwich', 3.70),
                5: ('Vegetable Sandwich', 4.00), 6: ('Cream Sandwich', 3.40),
                7: ('Ball Sandwich', 6.00), 8: ('Nutella Sandwich', 3.30),
                9: ('Beef Sandwich', 6.20), 10: ('Salmon Sandwich', 6.60),
                11: ('milk', 2.20), 12: ('coffee', 2.50), 13: ('tea', 2.10),
                14: ('coca cola', 1.50), 15: ('water', 1.10), 16: ('milkshake', 3.70)}

orders = {}
order_number = 0
# creat list for customer to make order
customer_order = []
couriers_list = ['uber', 'deliveroo', 'just eat']

# function to print the items in the menu


def product():

    #print the product list from the database
    insert_product_into_db()
    # Execute SQL query
    cursor.execute(
        'SELECT product_list_id, product_name, product_price FROM product_list')
    # Gets all rows from the result
    rows = cursor.fetchall()
    for row in rows:
        print(f'{str(row[0])} {row[1]} £{row[2]}')
    print('-------------------------------------')

    # print product list from python(product list above)
    # print('Product in the Menu:', '\n', '----------------')
    # for key, value in product_list.items():
    #     print(key, value[0], '£', value[1])
        
    print('Enter 1 to add a product and 0 to retuen to Main page')
    u_input = input()
    #try:
    u_input = int(u_input)
    if u_input == 1:
            last_key = list(product_list.keys())[-1]
            last_key = last_key+1
            print('Please Enter Product Name')
            new_product_Name = input()
            new_product_Name = str(new_product_Name)
            print('Please Enter product Price')
            new_product_Price = input()
            new_product_Price = float(new_product_Price)
            product_list[last_key] = [new_product_Name, new_product_Price]

            insert_product_into_db()
            sql = "INSERT INTO product_list (product_name,product_price) VALUES (%s, %s)"
            val = (new_product_Name, new_product_Price)
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
            connection.close()



            print('The new product is added successfully',
                  product_list[last_key])
    elif u_input == 0:
            main_page()
    else:
            print('Please Enter 1 to add or 0 to main page')
    #except:
     #   print('\n', "please just enter a digit", '\n')


#exit function to end the program
def exit():
    string = 'See you later :)  '
    for i in string:
        # printing each character of the message
        # In Python, files are automatically flushed while closing them.
        # However, a programmer can flush a file before closing it by using the flush() method.
        print(i, end='', flush=True)
        # adding time delay of half second to print each character
        time.sleep(0.5)
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
    for key, value in product_list.items():
        print(key, value[0], '£', value[1])
    #call order function    
    order()



#add & delet item function
def add_delet_status_item():
    # while loop to add items to the list
    # until finish will inter 0 to break the while loop
    while 1:
        print('\n', 'Enter the number of the item you would like to add',
              '\n', 'Or 0 to stop')
        user_input = input()

        #use try and except in case the user enter text instead of digit
        #try:
        user_input = int(user_input)
            #add item to the list
        if user_input in product_list.keys():
                customer_order.append(product_list[user_input])
                global total_price
                total_price = 0.0
                print('Your odrer:')
                for i in customer_order:
                    print(i[0], '£', i[1])
                    total_price = i[1]+total_price
                print('Total Price: £', total_price)
                
                #insert data to the database
                insert_product_into_db()
                sql = "INSERT INTO order_item(product_list_id,customer_id,quantity)VALUES(%s,%s,%s)"
                val = (user_input, last_customer_id, 1)
                cursor.execute(sql, val)
                connection.commit()
                cursor.close()
                connection.close()
                
        elif user_input == 0:
                break
        else:
                print('\n', 'Please Enter valid item number', '\n')
                continue
        #error message if the user enter text instead of digit
        #except:
         #   print("please just enter a digit")

    print('Your odrer:')
    for i in customer_order:
        print(i[0], '£', i[1])
        total_price = i[1]+total_price
    print('Total Price: £', total_price)

    #confirm order
    print('\n', 'Enter 1 to Confirm 2 to delete an items')
    confirm_item = input()
    confirm_item = int(confirm_item)
    if confirm_item == 1:
        orders[order_number].append(customer_order)
        orders[order_number].append(total_price)

        confirm_order_status()
        couriers()
        final_order()
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
                customer_order.remove(delete_item)
                print('\n', 'Your Order: ', '\n', ', '.join(customer_order))
                print('\n', 'Your odrer:', ', '.join(customer_order), '\n')
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

            print('\n', '**** Your Order on the way :) ****', '\n')
            for item in (orders.keys()):
                print('Order Number:', item)
                print('Customer name:', orders[item][0], '\n',
                      'Address:', orders[item][1], '\n',
                      'Phone No:', orders[item][2], '\n',
                      'Order Items:', orders[item][3], '\n',
                      'Order Time', orders[item][4], '\n',
                      'Order Status:', orders[item][5], '\n',
                      'Order Courier:', orders[item][6],)
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
            # add the time of the order
            now = datetime.now()
            global order_time
            order_time = now.strftime("%H:%M")
            order_time = str(order_time)
            global order_day
            order_day = now.strftime("%d:%m:%y")
            order_day = str(order_day)
            
            #add the time to the order
            orders[order_number].append(order_time)
            #add status to the order
            orders[order_number].append(order_status[order_status_now])
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

# couriers
def couriers():
    print('Couriers Available:', '\n', '----------------')
    for each in couriers_list:
        print('Courier Number: ', each)

    print('\n', 'Enter the name of the couriers:')
    courier_name = input()
    courier_name = courier_name.lower()
    if courier_name in couriers_list:
        print(courier_name)
        orders[order_number].append(courier_name)
    else:
        print('Please Enter Courier From Couriers List')
        couriers()

# final order
def final_order():
    #write the data to the file
    sourceFile_1 = open('G:\Generation\mini_project\order_file.txt', 'a')
    sourceFile_2 = open('G:\Generation\mini_project\order_file.csv', 'a')
    print(order_number, *orders[order_number], sep="||", file=sourceFile_1)
    print('-----------------------------------------------------------------------------',
          file=sourceFile_1)
    print(order_number, *orders[order_number], sep="||", file=sourceFile_2)
    print('-----------------------------------------------------------------------------',
          file=sourceFile_2)
    sourceFile_1.close()
    sourceFile_2.close()

    #insert data to the database
    insert_product_into_db()
    #sql = "INSERT INTO order_item(product_list_id,customer_id,quantity)VALUES(%s,%s,%s)"
    sql = "INSERT INTO `order`(customer_id,total,order_date,order_time)VALUES(%s,%s,%s,%s)"
    val = (last_customer_id, total_price,order_day,order_time)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()


    print('\n', '**** Your Order on the way :) ****', '\n')
    for item in (orders.keys()):
        print('Order Number:', item)
        print('Customer name:', orders[item][0])
        print('Address:', orders[item][1])
        print('Phone No:', orders[item][2])
        print('Order Items:', *orders[item][3], sep=',')
        print('Total Price:', '£', orders[item][4])
        print('Order Time', orders[item][5])
        print('Order Status:', orders[item][6])
        print('Order Courier:', orders[item][7])

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
