import pyodbc

dsn_name = "projetDatabase"
user_id = "santa"
password = "admin"

try:
    cnxn = pyodbc.connect(f"DSN={dsn_name};UID={user_id};PWD={password};")
    print("connexion reussie via DSN avec UID et PWD")
    
    ##########################
    #We need to make a password field for the customer
    #need to verify the password
    #need to encrypt the password when it goes in the database
    #need to decrypt the password when we fatch it from the database
    #when a customer is entered check if it is in the database, if so then ask password, if customer is not in the database then add phone number and password
    #Secret_Key = Christmas
    
    #ALTER TABLE customers 
    #ADD COLUMN password VARBINARY(255) NOT NULL; --*NOT NULL* needs to be added after all the customers have a password, we should add a way to reset the password after three tries
    # INSERT INTO customers (customer_name, customer_phone_number, password)
    # VALUES ('John Doe', '123456789', AES_ENCRYPT('secure_password', 'Christmas'));
    
    #how to select data from database
    # SELECT customer_name, 
    #    AES_DECRYPT(password, 'Christmas') AS decrypted_password
    # FROM customers;
    ##########################
    cursor = cnxn.cursor()
    #John doe wants to buy 5 christmas trees, a sales gets inserted in sales with the customer_id and the product_id, when a product gets sold the quantity sold gets removed from the quantity of the product sold
    cursor.execute("SET autocommit = 0")
    cursor.execute("BEGIN WORK")
    #lock tables to work on the database without interruptions from another user
    print("Locking tables...")
    cursor.execute("LOCK TABLES customers WRITE, products WRITE, sales WRITE, order_products WRITE, v_sales WRITE")
    #select last inserted id
    select_id = "SELECT LAST_INSERT_ID()"
    
    #start order
    print('who is ordering something')
    name=input()
    
    #confirmation stuff customer
    select_customer_query = "select customer_id, customer_name from customers where customer_name = ?"
    cursor.execute(select_customer_query, name)
    customer_query = cursor.fetchall()
    #select customer id
    select_customer_id = "select customer_id from customers where customer_name = ?"
    cursor.execute(select_customer_id, name)
    customer_id_tuple = cursor.fetchone()
    ########
    password_not_passed = True
    tries = 3
    while password_not_passed : 
        print('please enter the password for this customer')
        customer_password = input()
        if customer_id_tuple is None:
            print('please enter a phone number for the customer')
            phone_number = input()
            insert_customer_pass = """INSERT INTO customers (customer_name, customer_phone_number, password)
            VALUES (?, ?, AES_ENCRYPT(?, 'Christmas'))"""
            cursor.execute(insert_customer_pass, (name, phone_number, customer_password))
            password_not_passed = False
        else:
            
            if tries > 0:
                
                password_lookup = "SELECT AES_DECRYPT(password, 'Christmas') AS decrypted_password FROM customers where customer_id = ?"
                new_password_query = """UPDATE customers
                SET password = AES_ENCRYPT(?, 'Christmas')
                WHERE customer_id = ?"""
                cursor.execute(password_lookup, customer_id_tuple[0])
                confirm_password_tuple = cursor.fetchone()
                confirm_password = confirm_password_tuple[0].decode('utf-8')
                print(confirm_password)
                if confirm_password == customer_password:
                    print('if you would like to change your password please enter yes')
                    change_pass = input().lower()
                    if change_pass =='yes':
                        cursor.execute(new_password_query, (customer_password, customer_id_tuple[0]))
                        print('your password has been changed')
                        password_not_passed = False
                    else:
                        password_not_passed = False
                elif confirm_password_tuple is None:
                    print('the password that has been entered will be set as your password')
                    cursor.execute(new_password_query, (customer_password, customer_id_tuple[0]))
                else :
                    tries = tries-1
            else:
                print('please enter a new password')
                new_password = input()
                new_password_query = """UPDATE customers
                    SET password = AES_ENCRYPT(?, 'Christmas')
                    WHERE customer_id = ?"""
                cursor.execute(new_password_query, (new_password, customer_id_tuple[0]))
                
    ########
    #select customer id
    # select_customer_id = "select customer_id from customers where customer_name = ?"
    # cursor.execute(select_customer_id, name)
    # customer_id_tuple = cursor.fetchone()
    # if customer_id_tuple is None:
    #     print('please enter a phone number for the customer')
    #     phone_number = input()
    #     insert_customer = "insert into customers (customer_name, customer_phone_number) values(?, ?)"
    #     cursor.execute(insert_customer, (name, phone_number))
    #     cursor.execute(select_id)
    #     customer_id_tuple = cursor.fetchone()
    # else:
    #     print('customer is in the database')
    ########
        
    customer_id = customer_id_tuple[0]
    print (customer_id)
    
    print ('what is the customer ordering')
    item=input()
    print('how many of this item')
    quantity=int(input())
    order=(name, item, quantity)
    
    
    #confirmation stuff customer
    select_customer_query = "select customer_id, customer_name from customers where customer_name = ?"
    cursor.execute(select_customer_query, name)
    customer_query = cursor.fetchall()
    #select customer id
    select_customer_id = "select customer_id from customers where customer_name = ?"
    cursor.execute(select_customer_id, name)
    customer_id_tuple = cursor.fetchone()
    if customer_id_tuple is None:
        print('please enter a phone number for the customer')
        phone_number = input()
        insert_customer = "insert into customers (customer_name, customer_phone_number) values(?, ?)"
        cursor.execute(insert_customer, (name, phone_number))
        cursor.execute(select_id)
        customer_id_tuple = cursor.fetchone()
    else:
        print('customer is in the database')
        
    customer_id = customer_id_tuple[0]
    print (customer_id)
    #confirmation stuff product
    select_item_query = "select product_id, product_name from products where product_name = ?"
    cursor.execute(select_item_query, item)
    select_query = cursor.fetchall()
    #select product_id
    select_item_id = "select product_id from products where product_name = ?"
    cursor.execute(select_item_id, item)
    item_id_tuple = cursor.fetchone()
    if item_id_tuple is None:
        print('please enter a price for the item')
        price = float(input())
        print('please enter a quantity that is getting ordered for this item')
        qty = float(input())
        insert_item = "insert into products (product_name, price, quantity) values(?, ?, ?)"
        cursor.execute(insert_item, (item, price, qty))
        cursor.execute(select_id)
        item_id_tuple = cursor.fetchone()
    else:
        print("this item is in the database")
    item_id = item_id_tuple[0]
    print (item_id)
    #confirmation stuff product again
    select_quantity_query = "select product_name, quantity from products where product_name = ?"
    cursor.execute(select_quantity_query, item)
    quantity_query = cursor.fetchall()
    #select product quantity
    select_item_quantity = "select quantity from products where product_name = ?"
    cursor.execute(select_item_quantity, item)
    qty_check = cursor.fetchone()[0]
    
    #update quantity queries
    update_quantity1 = "UPDATE products SET quantity = quantity - ? WHERE product_id = ?"
    update_quantity2 = "UPDATE products SET quantity = quantity + ? WHERE product_id = ?"
    
    #check that the item is available
    if qty_check >= quantity:
        print('good to go')
        print('you have enough of this item')
        cursor.execute(update_quantity1, (quantity, item_id))
        
    #order more of the item requested(put it on order)
    else:
        print ('you need to order more ', item, ', please enter a quantity that you are placing on order for this item')
        amount_order = int(input())
        #check that the order will actually work once the new amount is done
        if (qty_check + amount_order) >= quantity:
            
            cursor.execute(update_quantity2, (amount_order, item_id))
            cursor.execute(update_quantity1, (quantity, item_id))
            insert_order_products = "insert into order_products (product_id) values (?)"
            cursor.execute(insert_order_products, item_id)
            
        else:
            cursor.execute("ROLLBACK")
            cursor.execute("UNLOCK TABLES")
            print('transaction rolled back and tables are unlocked')
            
    print('here is your order')    
    for row in customer_query:
        print(row)
    for row in select_query:
        print(row)
    for row in quantity_query:
        print(row)
    print('you ordered ', quantity, ' of this item')
    print('end of order')
    # now to add the sale in the database

    print('is everything correct yes or no')
    answer = input().strip().lower()
    if answer =='yes':
        # now to add the sale in the database
        insert_sales = "insert into sales (customer_id, product_id, quantity) values (?, ?, ?)"
        cursor.execute(insert_sales, (customer_id, item_id, quantity))
        cursor.execute(select_id)
        order_confirm = int(cursor.fetchone()[0])
        order_confirm_query = "select customer, product, quantity from v_sales where id = ?"
        # order_confirm_query = """
        # select customers.customer_name as customer, products.product_name as product, sales.quantity as quantity from sales 
        # join 
        # customers on customers.customer_id = sales.customer_id 
        # join
        # products on products.product_id = sales.product_id
        # where sale_id = ?"""
        cursor.execute(order_confirm_query, order_confirm)
        final_order = cursor.fetchall()
        for row in final_order:
            print(row)
        
        print('is everything correct yes or no')
        answer1 = input()
        if answer1 == 'yes':
                
            cnxn.execute('COMMIT')
        else:
            cnxn.execute('ROLLBACK')
            cursor.execute("UNLOCK TABLES")
            print('transaction rolled back and tables are unlocked')
    else :
        cnxn.execute('ROLLBACK')
        cursor.execute("UNLOCK TABLES")
        print('transaction rolled back and tables are unlocked')
    cnxn.close()
    
except pyodbc.Error as ex:
    print("erreur lors de la connexion:", ex)
    cnxn.execute('ROLLBACK')
    cursor.execute("UNLOCK TABLES")
    print('transaction rolled back and tables are unlocked')