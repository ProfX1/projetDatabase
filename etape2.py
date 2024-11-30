import pyodbc

dsn_name = "projetDatabase"
user_id = "santa"
password = "admin"

try:
    cnxn = pyodbc.connect(f"DSN={dsn_name};UID={user_id};PWD={password};")
    print("connexion reussie via DSN avec UID et PWD")
    
    cursor = cnxn.cursor()
    #John doe wants to buy 5 christmas trees, a sales gets inserted in sales with the customer_id and the product_id, when a producct gets sold the quantity sold gets removed from the quantity of the product sold
    cursor.execute("SET autocommit = 0")
    cursor.execute("BEGIN WORK")
    print('who is ordering something')
    name=input()
    print ('what is he ordering')
    item=input()
    print('how many of this item')
    quantity=int(input())
    order=(name, item, quantity)
    #select last inserted id
    select_id = "SELECT LAST_INSERT_ID()"
    
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
        cursor.execute(insert_customer, name, phone_number)
        cursor.execute(select_id)
        customer_id_tuple = cursor.fetchone()
        
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
    item_id = item_id_tuple[0]
    print (item_id)
    #confirmation stuff product again
    select_quantity_query = "select product_name, quantity from products where product_name = ?"
    cursor.execute(select_quantity_query, item)
    quantity_query = cursor.fetchall()
    for row in customer_query:
        print(row)
    for row in select_query:
        print(row)
    for row in quantity_query:
        print(row)
        
    # now to add the sale in the database
    
    
    # cursor.execute("update products set quantity = 15 where product_id=1")
    # cursor.execute("select quantity from products")
    

    # for row in cursor.fetchall():
    #     print(row)
    print('est-ce que tout est bon yes or no')
    answer = input()
    if answer =='yes':
        # now to add the sale in the database
        insert_sales = "insert into sales (customer_id, product_id) values (?, ?)"
        insert_order_products = "insert into order_products (product_id) values (?)"
        remove_quantity = "update"
        print('est-ce que tout est bon yes or no')
        answer1 = input()
        if answer1 == 'yes':
                
            cnxn.execute('COMMIT')
        else:
            cnxn.execute('ROLLBACK')
    else :
        cnxn.execute('rollback')
    cnxn.close()
    
except pyodbc.Error as ex:
    print("erreur lors de la connexion:", ex)