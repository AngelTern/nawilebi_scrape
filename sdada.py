import sqlite3

# Predefined phone values based on website
predefined_phone_map = {
    "https://apgparts.ge/": "555 21 21 96",
    "https://autogama.ge/": "593 10 08 78, 557 67 72 01, 568 82 93 33, 551 87 77 75",
    "https://autopia.ge": "0322 233 133",
    "https://autotrans.ge/": "511 30 13 03",
    "https://bgauto.ge/": "574 73 67 57",
    "https://carline.ge/": "514 22 98 98",
    "https://car-parts.ge": "577 12 73 76", 
    "https://www.crossmotors.ge/": "595 10 18 02",
    "https://geoparts.ge/": "596 80 20 00",
    "https://goparts.ge/ge": "577 01 20 06",
    "https://mmauto.ge/": "593 27 79 16, 599 38 21 18",
    "https://newparts.ge/": "599 84 88 45",
    "https://partscorner.ge/": "591 93 07 41",
    "https://pp.ge/": "322 80 13 13, 591 22 99 33",
    "https://pro-auto.ge/": "596 27 82 78, 571 00 00 71",
    "https://soloauto.ge/": "555 20 20 50",
    "https://topautoparts.ge/": "599 92 07 52",
    "https://vgparts.ge/": "555 74 41 11",
    "https://vsauto.ge/": "596 10 31 03",
    "https://zupart.ge/ka": "555 52 24 90"
}

# Connect to the database
conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

# Query to get all rows with website column
cursor.execute("SELECT id, website FROM your_table_name")

# Fetch all rows
rows = cursor.fetchall()

# Iterate over each row to update the phone column
for row in rows:
    row_id = row[0]
    website = row[1]

    # Find predefined phone number based on the website
    phone_number = predefined_phone_map.get(website)

    if phone_number:
        # Update the phone column with the predefined phone number
        cursor.execute(
            "UPDATE your_table_name SET phone = ? WHERE id = ?",
            (phone_number, row_id)
        )

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Phone numbers updated successfully!")
