# -*- coding: utf-8 -*-
"""
A La Carte - Food Ordering and Delivery Application
"""

import mysql.connector as sqltor
import time

from datetime import datetime

def _CheckUsernameStringCorrectness(username: str) -> bool:
    """Function to check the correctness of the username."""
    is_correct = True
    if len(username)==0:
        # Username cannot be an empty string.
        print('Username not entered by the user.')
        is_correct = False
    elif len(username)>20:
        # Username cannot have more than 20 characters
        print('Username should not have more than 20 characters')
        is_correct = False
    else:
        for s in username:
            # Username should not have special characters
            if not s.isalnum():
                is_correct = False
                break
    return is_correct

def _CheckPasswordStringCorrectness(password: str) -> bool:
    """Function to check the correctness of the password."""
    is_correct = True
    is_uppercase_present = False
    is_lowercase_present = False
    is_digit_present = False
    is_special_character_present = False
    
    if len(password)<5:
        # Password should have atleast 5 characters
        print('Password should have atleast 5 characters.')
        is_correct =False
    else:
        # Password should have atleast 1 uppercase, 1 lowercase, 1 number and 
        # 1 special character
        for s in password:
            if s.isupper():
                is_uppercase_present = True
            elif s.islower():
                is_lowercase_present = True
            elif s.isdigit():
                is_digit_present = True
            elif not s.isalnum():
                is_special_character_present = True
        if not is_uppercase_present:
            print('Password does not have atleast 1 uppercase character.')
            is_correct = False
        if not is_lowercase_present:
            print('Password does not have atleast 1 lowercase character.')
            is_correct = False
        if not is_digit_present:
            print('Password does not have atleast 1 digit.')
            is_correct = False
        if not is_special_character_present:
            print('Password does not have atleast 1 special character.')
            is_correct = False
    return is_correct
            
def _PrintPageHeader():
    """Function to clear existing screen and print the page header."""
    # Clear the screen
    print("\033[H")
    print("\033[J") 
    time.sleep(0.5)
    print('-----------------------------------')
    print('A La Carte - Your Food Delivery App')
    print('-----------------------------------')
    print()

def _PrintReturnToPreviousMessage():
    """Function to print the message to return to the previous menu."""
    print('Returning to the Previous Menu', end = "")
    time.sleep(1)
    print('.', end = "")
    time.sleep(1)
    print('.', end = "")
    time.sleep(1)
    print('.')

def setup(mycon):
    """Function to create the database and related tables for the application
    if they already don't exist."""
    my_cursor = mycon.cursor()
    my_cursor.execute('CREATE DATABASE IF NOT EXISTS alacarte;')
    my_cursor.execute('USE alacarte;')
    my_cursor.execute(
        'CREATE TABLE IF NOT EXISTS restaurant_login('+
        'username VARCHAR(20),'+
        'password VARCHAR(20),'+
        'PRIMARY KEY(username));'
    )
    my_cursor.execute(
        'CREATE TABLE IF NOT EXISTS restaurant_details('+
        'username VARCHAR(20),'+
        'name     VARCHAR(100),'+
        'city     VARCHAR(50),'+
        'cuisine  VARCHAR(100),'+
        'PRIMARY KEY(username));'
    )
    my_cursor.execute(
        'CREATE TABLE IF NOT EXISTS restaurant_menu('+
        'username           VARCHAR(20),'+
        'dish_category      VARCHAR(100),'+
        'dish_name          VARCHAR(50),'+
        'dish_description   VARCHAR(200),'+
        'dish_price         NUMERIC,'+
        'max_order_quantity INTEGER,'+
        'PRIMARY KEY(username,dish_name));'
    )
    my_cursor.execute(
        'CREATE TABLE IF NOT EXISTS restaurant_customer_orders('+
        'restaurant_username VARCHAR(20),'+
        'customer_username   VARCHAR(20),'+
        'order_amount        NUMERIC,'+
        'date_time           DATETIME,'+
        'mode_of_payment     VARCHAR(50),'+
        'PRIMARY KEY(restaurant_username, customer_username, date_time));'
    )
    my_cursor.execute(
        'CREATE TABLE IF NOT EXISTS restaurant_customer_ratings('+
        'restaurant_username VARCHAR(20),'+
        'customer_username   VARCHAR(20),'+
        'ratings             INTEGER(1),'+
        'PRIMARY KEY(restaurant_username, customer_username));'
    )
    my_cursor.execute(
        'CREATE TABLE IF NOT EXISTS customer_login('+
        'username VARCHAR(20),'+
        'password VARCHAR(20),'+
        'PRIMARY KEY(username));'
    )
    my_cursor.execute(
        'CREATE TABLE IF NOT EXISTS customer_details('+
        'username VARCHAR(20),'
        'first_name VARCHAR(20),'+
        'last_name VARCHAR(20),'+
        'city VARCHAR(50),'+
        'PRIMARY KEY(username));'
    )
    my_cursor.close()

def _CheckUsernameForUniqueness(
        mycon, 
        username: str, 
        restaurant_or_customer: str
    ) -> bool:
    """Function to check if username already exists for any other restaurant or
    customer.
    The argument restaurant_or_customer is used to specify the table name to 
    be used to check whether or not the username is unique.
    """
    is_username_unique = True
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query = (
        "SELECT COUNT(*) "+
        "FROM %s_login " % (restaurant_or_customer)+
        "WHERE username = '%s'" % (username)
    )
    my_cursor.execute(query)
    username_count = my_cursor.fetchone()
    if username_count[0] != 0:
        is_username_unique = False
    my_cursor.close()
    return is_username_unique

def _InsertLoginDetails(
        mycon, 
        restaurant_or_customer: str,
        username: str,
        password: str):
    """Function for inserting restaurant/customer login details (username and 
    password) into the corresponding table.
    """
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    insert_statement = (
        "INSERT INTO %s_login " % (restaurant_or_customer) +
        "VALUES "+
        "('%s','%s')" % (username, password)    
    )
    my_cursor.execute(insert_statement)
    mycon.commit()
    my_cursor.close()

def _CheckLoginDetails(
        mycon,
        restaurant_or_customer: str,
        username: str,
        password: str) -> bool:
    """Function to check whether or not the provided username and password
    are correct by checking if they already exist in the table."""
    is_correct_login_info = True
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query = (
        "SELECT COUNT(*) "+
        "FROM %s_login " % (restaurant_or_customer)+
        "WHERE username = '%s' " % (username)+
        "  AND password = '%s'; " % (password)
    )
    my_cursor.execute(query)
    record_count = my_cursor.fetchone()
    if record_count[0] == 0:
        is_correct_login_info = False
    return is_correct_login_info

def Login(mycon, restaurant_or_customer: str) -> str:
    """Function to handle restaurant/customer login. After 3 unsuccessful login 
    attempts, the control will return to restaurant/customer startup menu.
    """
    is_username_password_correct = False
    username = ""
    password = ""
    attempt_number = 0
    while(not is_username_password_correct):
        _PrintPageHeader()
        print('Login')
        print('*****')
        print()
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        # Function call to check if the login details are correct
        is_username_password_correct = (
            _CheckLoginDetails(mycon,restaurant_or_customer,username,password)
        )
        if not is_username_password_correct:
            print('Username or Password is Incorrect.')
            attempt_number = attempt_number + 1
            if attempt_number == 3:
                break
    if attempt_number == 3:
        # Login Failed for 3 attempts. Return to the previous screen with no
        # username.
        username = ""
    return username
            
        
    
def CreateAccount(mycon,restaurant_or_customer: str):
    """Function handling the the creation of account for restaurants/customers.
    The argument restaurant_or_customer determines whether the account has to
    be created for a restaurant or a customer."""
    username_all_checks_passed = False
    password_all_checks_passed = False
    username = ""
    password = ""
    while(not (username_all_checks_passed and password_all_checks_passed)):
        _PrintPageHeader()
        print('Create Account')
        print('**************')
        print()
        username = input(
            'Enter Username (should not have more than 20 characters):'
        )
        username_string_correctness = _CheckUsernameStringCorrectness(username)
        username_uniqueness = _CheckUsernameForUniqueness(
            mycon,
            username,
            restaurant_or_customer
        )
        username_all_checks_passed = (
            username_string_correctness and username_uniqueness
        )
        
        print('Password should have-')
        print('Atleast 1 Uppercase Letter.')
        print('Atleast 1 Lowercase Letter.')
        print('Atleast 1 Number.')
        print('Atleast 1 Special Character.')
        password = input('Enter Password:')
        password_all_checks_passed = _CheckPasswordStringCorrectness(password)
        if password_all_checks_passed:
            confirm_password = input('Confirm Password: ')
            if password != confirm_password:
                print(
                    'Confirm Password value does not match the Password value.'
                )
                password_all_checks_passed = False
        if not password_all_checks_passed:
            print('Retry Password.')
            time.sleep(2)        
            
    _InsertLoginDetails(mycon, restaurant_or_customer, username, password)
    print(
        'Account for the Restaurant has been created with the username: ',
        username
    )
    _PrintReturnToPreviousMessage()

def AddOrEditRestaurantDetails(mycon, username: str):
    _PrintPageHeader()
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query = (
        "SELECT COUNT(*) "+
        "FROM restaurant_details "+
        "WHERE username = '%s' " % (username)
    )
    my_cursor.execute(query)
    record_count = my_cursor.fetchone()
    if record_count[0] == 0:
        print('Restaurant details not present in the system.')
        print('Our pleasure adding your restaurant to the system.')
        name = input('Enter Restaurant Name: ')
        # To do: Restrict to a number of cities for delivery time computation.
        city = input('Enter the Restaurant City: ')
        cuisine = input('Enter the Kind of Cuisine the Restaurant Serves: ')
        insert_statement = (
            "INSERT INTO restaurant_details "+
            "VALUES ('%s','%s','%s','%s');" % (username,name,city,cuisine)
        )
        my_cursor.execute(insert_statement)
        mycon.commit()
        print('Restaurant Details Successfully Added to the System.')
    else:
        update_choice = 0
        print('Restaurant details found in the system.')
        print('1. Update Restaurant Name.')
        print('2. Update Restaurant City.')
        print('3. Update Restaurant Cuisine.')
        update_choice = int(input('Enter Choice: '))
        update_column = ''
        column_value = ''
        if update_choice == 1:
            update_column = 'name'
            column_value = input('Enter the New Restaurant Name: ')
        elif update_choice == 2:
            update_column = 'city'
            column_value = input('Enter the New Restaurant City: ')
        elif update_choice == 3:
            update_column = 'cuisine'
            column_value = input('Enter the New Restaurant Cuisine: ')
        else:
            print('Incorrect choice entered for update.')
        if update_column != '':
            update_statement = (
                "UPDATE restaurant_details " +
                "SET %s = '%s'" % (update_column, column_value) +
                "WHERE username = '%s'" %(username)
            )
            my_cursor.execute(update_statement)
            mycon.commit()
            print('Restaurant Details are Successfully Updated in the System.')
    my_cursor.close()
    _PrintReturnToPreviousMessage()

def AddItemsToRestaurantMenu(mycon, username: str):
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    choice = 'y'
    while(choice != 'n'):
        _PrintPageHeader()
        print("Enter the details of your delicious delicacy.")
        dish_category = input("Enter the category for this dish: ")
        dish_name = input("Enter the dish name: ")
        dish_description = input("Describe this dish for your customers:")
        dish_price = float(input("Enter the price (in Rupees) of the dish: "))
        max_order_quantity = int(input("Enter the maximum order quantity: "))
        insert_statement = (
            "INSERT INTO restaurant_menu "+
            "VALUES ('%s','%s','%s','%s','%s','%s');" % (
                username, 
                dish_category, 
                dish_name, 
                dish_description, 
                dish_price,
                max_order_quantity
                )
        )
        my_cursor.execute(insert_statement)
        mycon.commit()
        choice = input('Do you want to add another dish(y/n)?')
    my_cursor.close()
    _PrintReturnToPreviousMessage()
        
def DeleteItemsFromRestaurantMenu(mycon, username: str):
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    choice = 'y'
    while(choice != 'n'):
        _PrintPageHeader()
        dish_name = input(
            "Enter the dish name that the customers will miss having :("
        )
        delete_statement = (
            "DELETE FROM restaurant_menu "+
            "WHERE username = '%s' " % (username) +
            "  AND dish_name = '%s';" % (dish_name)
            
        )
        my_cursor.execute(delete_statement)
        mycon.commit()
        choice = input('Do you want to delete another dishes(y/n)?')
    my_cursor.close()
    _PrintReturnToPreviousMessage()
        
def DisplayRestaurantMenu(mycon, restaurant_username) -> dict:
    _PrintPageHeader()
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query = (
        "SELECT * "+
        "FROM restaurant_menu "+
        "WHERE username = '%s' " % (restaurant_username) +
        "ORDER BY dish_category, dish_name"
    )
    my_cursor.execute(query)
    restaurant_menu_items = my_cursor.fetchall()
    # Dictionary of list of lists keyed on item category
    menu_items_by_category = {}
    # Dictionary of lists keyed on the number using which a customer will 
    # select a dish.
    menu_items_by_number = {}
    dish_count = 0
    for restaurant_menu_item in restaurant_menu_items:
        
        if restaurant_menu_item[1] not in menu_items_by_category:
           menu_items_by_category[restaurant_menu_item[1]] = []
        menu_items_by_category[restaurant_menu_item[1]].append([
            restaurant_menu_item[2],
            restaurant_menu_item[3],
            restaurant_menu_item[4],
            restaurant_menu_item[5]
        ])
        dish_count = dish_count + 1
        menu_items_by_number[dish_count] = [
            restaurant_menu_item[2],
            restaurant_menu_item[3],
            restaurant_menu_item[4],
            restaurant_menu_item[5]
        ]
    dish_count = 0
    for category in menu_items_by_category:
        print(category)
        print('#################')
        for menu_items_for_category in menu_items_by_category[category]:
            dish_count = dish_count + 1
            print(dish_count,'.', end = " ")
            print("Dish Name: ", menu_items_for_category[0], end = " | ")
            print("Dish Price: ", menu_items_for_category[2], end = " | ")
            print("Max Order Quantity: ", menu_items_for_category[3])
            print("Description: ", menu_items_for_category[1])
            print('---------------------------------------------------------------------------------------')
    if len(menu_items_by_category) == 0:
        print("No Items in the Restaurant's Menu.")
    my_cursor.close()
    return menu_items_by_number
    
def ViewRestaurantSales(mycon, restaurant_username: str):
    _PrintPageHeader()
    print('Record of Orders from the Restaurant')
    print('------------------------------------------')
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    # To Do: Add options to give selection criteria for displaying orders.
    # To Do: Join with customer table to display customer name.
    query = (
        "SELECT * " +
        "FROM restaurant_customer_orders " +
        "WHERE restaurant_username = '%s'" % (restaurant_username) +
        "ORDER BY date_time DESC"
        
    )
    my_cursor.execute(query)
    restaurant_orders = my_cursor.fetchall()
    for restaurant_order in restaurant_orders:
        # To Do: Print Customer name instead of username
        print('Customer Username: ',restaurant_order[1])
        print('Order Amount: ', restaurant_order[2])
        print('Date and Time: ', restaurant_order[3])
        print('Mode of Payment: ', restaurant_order[4])
        print('---------------------------------------------------------------------------------------')
    if len(restaurant_orders) == 0:
        print('Restaurant Does Not Have Orders.')
    my_cursor.close()
    previous_page = input('Press y and enter to return to the previous page.')
    _PrintReturnToPreviousMessage()
    
def GetAverageRestaurantRatings(mycon, restaurant_username: str) -> float:
    average_rating = 0.0
    num_of_customers = 0
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query = (
        "SELECT AVG(IFNULL(ratings,0)), COUNT(*)"+
        "FROM restaurant_customer_ratings "+
        "WHERE restaurant_username = '%s';" % (restaurant_username)
    )
    my_cursor.execute(query)
    query_result = my_cursor.fetchone()
    average_rating, num_of_customers = query_result[0], query_result[1]
    my_cursor.close()
    return average_rating, num_of_customers

def DisplayAverageRestaurantRatings(
        mycon, 
        average_rating: float, 
        num_of_customers: int
):
    _PrintPageHeader()
    if average_rating == 0.0:
        print('The Restaurant has not been Rated by Customers.')
    else:
        # To Do: Correct the indentation
        print(
            "The Rating for the Restaurant (out of 5)) is: ",
            average_rating,
            "given by ",
            num_of_customers,
            "customers."
        )
    previous_page = input('Press y and enter to return to the previous page.')
    _PrintReturnToPreviousMessage()

def RestaurantOwnerMenu(mycon, username: str):
    choice = 0
    while(choice!=7):
        _PrintPageHeader()
        print('Hello restaurant owner, ', username ,'! What would you like to do?')
        print()
        print('1. Add/Edit Restaurant Details')
        print('2. Add Items to the Menu')
        # To Do: Add an option to update items in the menu.
        print('3. Delete Items from Menu')
        # To Do: Add an option for adding items through a csv file.
        print('4. Display the Current Menu (as visible to the customers)')
        print('5. View Sales')
        print('6. Get Average Ratings')
        print('7. Return to the Previous Menu')
        choice = int(input('Enter choice: '))
        if choice == 1:
            AddOrEditRestaurantDetails(mycon, username)
        elif choice == 2:
            AddItemsToRestaurantMenu(mycon, username)
        elif choice == 3:
            DeleteItemsFromRestaurantMenu(mycon, username)
        elif choice == 4:
            menu_items_by_number = DisplayRestaurantMenu(mycon, username)
            previous_page = input('Press y and enter to return to the previous page: ')
            _PrintReturnToPreviousMessage()
        elif choice == 5:
            ViewRestaurantSales(mycon, username)
        elif choice == 6:
            average_rating, num_of_customers = (
                GetAverageRestaurantRatings(mycon, username)
            )
            DisplayAverageRestaurantRatings(
                mycon, 
                average_rating, 
                num_of_customers
            )
        elif choice == 7:
            _PrintReturnToPreviousMessage()

def AddOrEditCustomerDetails(mycon, username: str):
    _PrintPageHeader()
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query = (
        "SELECT COUNT(*) "+
        "FROM customer_details "+
        "WHERE username = '%s' " % (username)
    )
    my_cursor.execute(query)
    record_count = my_cursor.fetchone()
    if record_count[0] == 0:
        print('Customer details not present in the system.')
        print('Our pleasure adding your details to the system.')
        first_name = input('Enter Your First Name: ')
        last_name = input('Enter Your Last Name: ')
        # To do: Restrict to a number of cities for delivery time computation.
        city = input('Enter Your City: ')
        insert_statement = (
            "INSERT INTO customer_details "+
            "VALUES ('%s','%s','%s','%s');" % (
                username,
                first_name,
                last_name,
                city
            )
        )
        my_cursor.execute(insert_statement)
        mycon.commit()
        print('Your Details are Successfully Added to the System.')
    else:
        update_choice = 0
        print('Your details found in the system.')
        print('1. Update Your First Name.')
        print('2. Update Your Last Name.')
        print('3. Update Your City.')
        update_choice = int(input('Enter Choice: '))
        update_column = ''
        column_value = ''
        if update_choice == 1:
            update_column = 'first_name'
            column_value = input('Enter the First Name: ')
        elif update_choice == 2:
            update_column = 'last_name'
            column_value = input('Enter the Last Name: ')
        elif update_choice == 3:
            update_column = 'city'
            column_value = input('Enter the City: ')
        else:
            print('Incorrect choice entered for update.')
        if update_column != '':
            update_statement = (
                "UPDATE customer_details " +
                "SET %s = '%s'" % (update_column, column_value) +
                "WHERE username = '%s'" %(username)
            )
            my_cursor.execute(update_statement)
            mycon.commit()
            print('Your Details are Successfully Updated in the System.')
    my_cursor.close()
    previous_page = input('Press y and enter to return to the previous page')
    _PrintReturnToPreviousMessage()

def DisplayRestaurantsForOrders(mycon) -> dict:
    print('Get your desired food any of these awesome places: ')
    print()
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query = (
        "SELECT restaurant_details.username, "+
        "       restaurant_details.name, "+
        "       restaurant_details.city, "+
        "       restaurant_details.cuisine "
        "FROM restaurant_details; "
    )
    my_cursor.execute(query)
    restaurants = my_cursor.fetchall()
    restaurant_count = 0
    restaurants_by_count = {}
    for restaurant in restaurants:
        restaurant_count = restaurant_count + 1
        rating = ""
        query = ("SELECT AVG(IFNULL(ratings,0)) FROM restaurant_customer_ratings WHERE restaurant_username = '%s';" % (restaurant[0]))
        my_cursor.execute(query)
        ratings = my_cursor.fetchone()
        if ratings[0] == None:
            rating = 'Not Rated'
        else:
            rating = str(ratings[0])
        print(
            restaurant_count, '. ',
            restaurant[1], ' | ',
            restaurant[2], ' | ',
            restaurant[3], ' | ',
            rating
        )
        print('--------------------------------------------------------------------------------------')
        restaurants_by_count[restaurant_count] = restaurant[0]
    if len(restaurants) == 0:
        print('No Restaurants Present in the System.')
    my_cursor.close()
    return restaurants_by_count
    

def OrderFood(mycon, username: str):
    _PrintPageHeader()
    restaurants_by_count = DisplayRestaurantsForOrders(mycon)
    if len(restaurants_by_count) == 0:
        prev_screen = input('Press y and enter to go to the previous screen.')
    else:
        restaurant_number = int(input('Enter the Restaurant number to Order (or enter 999 to return to previous menu): '))
        if restaurant_number == 999:
            print('Going to the Previous Page',end = "")
        elif restaurant_number > len(restaurants_by_count):
            print('Invalid Restaurant Number.')
        else:
            menu_items_by_number = DisplayRestaurantMenu(
                mycon, restaurants_by_count[restaurant_number]
            )
            total_price = 0
            add_more_items = 'y'
            while(add_more_items != 'n'):
                dish_number = int(input('Enter the dish number to order: '))
                quantity = int(input('Enter the quantity: '))
                if quantity > menu_items_by_number[dish_number][3]:
                    print('Quantity > max quantity ordered. Therefore assigning max quantity.')
                total_price += menu_items_by_number[dish_number][2] * quantity
                add_more_items = input('Want to add more items (y/n)?')
            print('Order Complete. The total is Rs. ',total_price)
            print('Payment Options: ')
            print('1. Card')
            print('2. Cash On Delivery')
            print('3. UPI')
            # To Do: Include addition of input of card number and UPI id while payment
            payment_choice = int(input('Enter Choice'))
            mode_of_payment = ""
            if payment_choice == 1:
                mode_of_payment = 'Card'
            elif payment_choice == 2:
                mode_of_payment = 'COD'
            elif payment_choice == 3:
                mode_of_payment = 'UPI'
            else:
                print('Invalid Mode of Payment.')
            if mode_of_payment != "":
                # To Do: Put this into a function
                my_cursor = mycon.cursor()
                my_cursor.execute('USE alacarte;')
                current_date_time = datetime.now()
                mysql_formatted_date = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
                insert_statement = (
                    "INSERT INTO restaurant_customer_orders VALUES "+
                    "('%s','%s',%s,'%s','%s');" % (
                        restaurants_by_count[restaurant_number],
                        username,
                        total_price,
                        mysql_formatted_date,
                        mode_of_payment
                    )
                )
                # To Do: Compute time required for order delivery based on 
                # the Customer and Restaurant Location
                my_cursor.execute(insert_statement)
                mycon.commit()
                my_cursor.close()
                print('Order Placed Successfully!')
    previous_page = input('Press y and enter to return to the previous page')
    _PrintReturnToPreviousMessage()

def RateRestaurants(mycon, username: str):
    _PrintPageHeader()
    restaurants_by_count = DisplayRestaurantsForOrders(mycon)
    if len(restaurants_by_count) == 0:
        prev_screen = input('Press y and enter to go to the previous screen.')
    else:
        restaurant_number = int(input('Enter the Restaurant number to Rate: '))
        if restaurant_number > len(restaurants_by_count):
            print('Invalid Restaurant Number.')
        else:
            rating = int(input('Enter the rating (integer, between 1-5): '))
            if rating < 1 or rating > 5:
                print('Invalid Rating')
            else:
                # To Do: Put this into a function
                my_cursor = mycon.cursor()
                my_cursor.execute('USE alacarte;')
                insert_statement = (
                    "INSERT INTO restaurant_customer_ratings VALUES"+
                    "('%s','%s',%s);" % (
                        restaurants_by_count[restaurant_number],
                        username,
                        rating
                    )
                )
                my_cursor.execute(insert_statement)
                mycon.commit()
                my_cursor.close()
                print('Rating Successfully Sent!')
    previous_page = input('Press y and enter to return to the previous page')
    _PrintReturnToPreviousMessage()
                
def ViewPastCustomerOrders(mycon, username: str):
    _PrintPageHeader()
    my_cursor = mycon.cursor()
    my_cursor.execute('USE alacarte;')
    query=(
        "SELECT t2.name, t.order_amount, t.date_time, t.mode_of_payment "+
        "FROM restaurant_customer_orders AS t, restaurant_details AS t2 "+
        "WHERE customer_username = '%s'" % (username) +
        "ORDER BY date_time DESC;"
    )
    my_cursor.execute(query)
    orders = my_cursor.fetchall()
    for order in orders:
        print('Restaurant Name: ', order[0])
        print('Order Amount: ', order[1])
        print('Order Date and Time', order[2])
        print('Mode of Payment', order[3])
    if len(orders) == 0:
        print('No order placed by the customer')
    my_cursor.close()
    previous_page = input('Press y and enter to return to the previous page')
    _PrintReturnToPreviousMessage()    
    
def CustomerMenu(mycon, username: str):
    choice = 0
    while(choice!=5):
       _PrintPageHeader() 
       print('Hello customer, ', username ,'! What would you like to do?')
       print('1. Add/Edit Customer Details')
       print('2. Order Food')
       print('3. Rate Restaurant')
       print('4. View Past Orders')
       print('5. Return to Previous Menu')
       choice = int(input('Enter Choice: '))
       if choice == 1:
           AddOrEditCustomerDetails(mycon,username)
       elif choice == 2:
           OrderFood(mycon, username)
       elif choice == 3:
           RateRestaurants(mycon, username)
       elif choice == 4:
           ViewPastCustomerOrders(mycon, username)
       elif choice == 5:
           _PrintReturnToPreviousMessage()
       else:
           print('Incorrect choice entered.')
       
def UserStartUpMenu(mycon, restaurant_or_customer):
    """Function for asking restaurant owners to either login or create an 
    account."""
    choice = 0
    while(choice!=3):
        username = ""
        _PrintPageHeader()
        print('Hello '+restaurant_or_customer+'!')
        print()
        print('1. Already with us? Why dont we Login :)')
        print('2. New here? Create an account to enjoy our service!')
        print('3. Return to app startup.')
        choice = int(input('Enter choice (1,2 or 3): '))
        if choice == 1:
            username = Login(mycon,restaurant_or_customer)
            if username == "":
                print("Not Logged in Because of 3 Unsuccessful Tries.")
            elif restaurant_or_customer == 'restaurant':
                RestaurantOwnerMenu(mycon, username)
            elif restaurant_or_customer == 'customer':
                CustomerMenu(mycon, username)
        elif choice == 2:
            CreateAccount(mycon,restaurant_or_customer)
        elif choice == 3:
             _PrintReturnToPreviousMessage()
        else:
            print('Incorrect Choice Entered.')

def AppStartupMenu(mycon):
    """This function is the starting point for the app's control flow. It 
    will display the first menu and will call other functions depending on
    what the user chooses."""
    choice = 0
    while(choice!=3):
        _PrintPageHeader()
        print('Welcome to A La Carte')
        print()
        print('You are -')
        print('1. Restaurant')
        print('2. Customer')
        print('3. Done with ordering so want to close the app.')    
        choice = int(input('Enter choice (1,2 or 3): '))
        if choice == 1:
            UserStartUpMenu(mycon,'restaurant')
        elif choice == 2:
            UserStartUpMenu(mycon,'customer')
        elif choice == 3:
            print('It was good to have you visit our application. Please visit again!')
        else:
            print('Incorrect Choice Entered.')
            
if __name__=='__main__':
    # Starting the connection
    mycon = sqltor.connect(
        host = "localhost", user = "root", password = "pass")
    if not mycon.is_connected:
        print('Unable to connect to MySQL server.')
    setup(mycon)
    AppStartupMenu(mycon)
    mycon.close()
 