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
    
    cursor.execute("select * from products")
    
    
    for row in cursor.fetchall():
        print(row)
        
    cnxn.close()
    
except pyodbc.Error as ex:
    print("erreur lors de la connexion:", ex)