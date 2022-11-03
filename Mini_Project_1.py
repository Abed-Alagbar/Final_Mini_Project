# add some product names
# CREATE products list
product_list = {1: 'Egg Sandwich', 2: 'Chicken Sandwich', 3: 'Fish Sandwich', 4: 'Cheese Sandwich',
                5: 'Vegetable Sandwich', 6: 'Cream Sandwich', 7: 'Ball Sandwich', 8: 'Nutella Sandwich',
                9: 'Beef Sandwich', 10: 'Salmon Sandwich', 11: 'milk', 12: 'coffee', 13: 'tea', 14: 'coca cola',
                15: 'water', 16: 'milkshake'}

# function to print the items in the menu
def product():
    print('Product in the Menu:', '\n', '----------------')
    for key, value in product_list.items():
        print("Number : {} , Item Name :{}".format(key, value))


    # we can use * when we are not sure about the number of arguments
    # that can be passed to a function.
    #print(*product_list.values(), sep="\n")
    #def intro(**data):
    #    for key, value in product_list.items():
    #        print("No.{} {}".format(key, value))
    #intro()

# exit function
def exit():
    main_page()

# make order function
def make_order():
    print('\n', '            **** Add item to your Order ****',
          '\n', '                 ***********************')
    product()
    order()

#confirm order function
def confirm_item():
    print('Enter 1 to Confirm 2 to delete an item')
    confirm_item = input()
    confirm_item = int(confirm_item)
    if confirm_item == 1:
        print('Your Order on the way :)')
    elif confirm_item == 2:
        print('Enter name of item you would like to delete')
        delete_item = input()
        delete_item = str(delete_item)
        customer_order = customer_order.remove(delete_item)
        print('Your Order: ', '\n', ', '.join(customer_order))
    else:
        print("That is not a valid entry.")

    main_page()

# add & delet item function
def add_item():
    # creat list for customer to make order
    customer_order = []
    # while loop to add items to the list 
    # until finish will inter 0 to break the while loop
    while 1:
        print('Enter the number of the item you would like to add or 0 to stop')
        user_input = input()
        user_input = int(user_input)
        if user_input == 0:
            break
        # add item to the list
        customer_order.append(product_list[user_input])
        #','.join(lst)
        print(', '.join(customer_order))
    print('\n', 'Your odrer:', ', '.join(customer_order), '\n')
    # confirm order
    print('Enter 1 to Confirm 2 to delete an item')
    confirm_item = input()
    confirm_item = int(confirm_item)
    if confirm_item == 1:
        print('\n','**** Your Order on the way :) ****','\n')
    # delete items from the list    
    elif confirm_item == 2:
        # while loop to delet items from the list
        # when finish enter stop
        while 1:
          print('Enter name of item you would like to delete or stop to finish')
          delete_item = input()
          # make the enter from user string
          delete_item = str(delete_item)
          # make the enter from the user lower case
          delete_item = delete_item.lower()
          # if the user enter stop the loop will break
          if delete_item == 'stop':
            break
          customer_order.remove(delete_item)
          print('Your Order: ', '\n', ', '.join(customer_order))
          print('\n', 'Your odrer:', ', '.join(customer_order), '\n')
        #Confirm the order
        print('\n', 'Your Order: ', ', '.join(customer_order), '\n', '\n',
              'Enter 1 to Confirm 2 to go to the main page')
        confirm_item = input()
        confirm_item = int(confirm_item)
        if confirm_item == 1:
            print('\n','**** Your Order on the way :) ****','\n')
        else:
            main_page()
    else:
        print("That is not a valid entry.")
        main_page()

# make order function
def order():
    print('\n', 'Would you like to make order:',
          '\n', 'If yes Enter 1', 'If No Enter 2')
    order = input()
    order = int(order)
    if order == 1:
        add_item()
        
    else:
        main_page()

# main page function
def main_page():
    print("Inter Number of the page", '\n',
          "******* 1    Main Page  ", '\n',
          "******* 2    Product    ", '\n',
          "******* 3    Couriers   ", '\n',
          "******* 4    Make an Order ", '\n',
          "******* 5    Exit      ")
    x = input('Enter Number: ')
    x = int(x)
    if x == 1:
        print('main')
        main_page()
        pass
    elif x == 2:
        product()
    elif x == 3:
        print('couriers')
    elif x == 4:
        make_order()
    elif x == 5:
        print('Exit See you later')
    else:
        print('Choose the number of item you would like to       add to your order.')
        main_page()


# call main page function
main_page()
