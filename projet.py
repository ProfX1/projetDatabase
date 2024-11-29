import pyodbc

dsn_name = "3dhub"
user_id = "python"
password = "python"

try:
    cnxn = pyodbc.connect(f"DSN={dsn_name};UID={user_id};PWD={password};")
    print("connexion reussie via DSN avec UID et PWD")
    
    cursor = cnxn.cursor()
    cursor.execute("select * from costs where listed_price >= 110")
    for row in cursor.fetchall():
        print(row)
        
    cnxn.close()
    
except pyodbc.Error as ex:
    print("erreur lors de la connexion:", ex)
    
    