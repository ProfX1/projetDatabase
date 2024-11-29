import pyodbc

dsn_name = "projetDatabase"
user_id = "santa"
password = "admin"

try:
    cnxn = pyodbc.connect(f"DSN={dsn_name};UID={user_id};PWD={password};")
    print("connexion reussie via DSN avec UID et PWD")
    
    cursor = cnxn.cursor()
    
    cursor.execute("SET autocommit = 0")
    cursor.execute("BEGIN WORK")
    
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