import pyodbc

dsn_name = "christmasshop"
user_id = "elf"
password = "admin"

try:
    cnxn = pyodbc.connect(f"DSN={dsn_name};UID={user_id};PWD={password};")
    print("connexion reussie via DSN avec UID et PWD")
    
    cursor = cnxn.cursor()
    cursor.execute("select * from customers")
    for row in cursor.fetchall():
        print(row)
        
    cnxn.close()
    
except pyodbc.Error as ex:
    print("erreur lors de la connexion:", ex)
    
    