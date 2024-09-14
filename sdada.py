import MySQLdb

try:
    connection = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="12XklsD!?NmG1509",
        db="nawilebi"
    )
    print("Connection successful!")
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")
