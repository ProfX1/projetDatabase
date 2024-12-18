import pyodbc

dsn_name = "projetmysql"
user_id = "elf"
password = "admin"

#cet utilisateur a seulement acces a la database christmasshop en select, il ne peut pas faire d'autres actions
try:
    cnxn = pyodbc.connect(f"DSN={dsn_name};UID={user_id};PWD={password};")
    print("connexion reussie via DSN avec UID et PWD")
    
    cursor = cnxn.cursor()
    cursor.execute("select * from products")
    for row in cursor.fetchall():
        print(row)
        
    cnxn.close()
    
except pyodbc.Error as ex:
    print("erreur lors de la connexion:", ex)
    
    