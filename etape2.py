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
    cursor.execute("update products set quantity = 15 where product_id=1")
    cursor.execute("select quantity from products")
    

    for row in cursor.fetchall():
        print(row)
    print('est-ce que tout est bon yes or no')
    answer = input()
    if answer =='yes':    
        cnxn.execute('COMMIT')
    else :
        cnxn.execute('rollback')
    cnxn.close()
    
except pyodbc.Error as ex:
    print("erreur lors de la connexion:", ex)