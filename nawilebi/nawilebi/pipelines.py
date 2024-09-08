# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging

#from nawilebi.utilities.additional_functions import extract_numbers, process_part_full_name
from utilities.additional_functions import extract_numbers, process_part_full_name_autopia

class NawilebiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        for field_name in field_names:
            value = adapter.get(field_name)

            if isinstance(value, str):
                adapter[field_name] = value.strip()

        return item

import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '12XklsD@?NmG1509',
            database = 'nawilebi'
        )

        self.cur = self.conn.cursor()
        
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS nawilebi(
                             id int NOT NULL auto_increment, 
                             part_url VARCHAR(1000),
                             car_mark VARCHAR(70),
                             part_full_name VARCHAR(150),
                             car_model VARCHAR(150),
                             year VARCHAR(10),
                             price INT,
                             in_stock BOOLEAN,
                             website VARCHAR(255),
                             PRIMARY KEY (id)                                                         
                         )
                         """)
    
    def process_item(self, item, spider):
        self.cur.execute("""
                         insert into nawilebi(
                             part_url, car_mark, part_full_name, car_model, year, price, in_stock, website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                             (
                                item.get('part_url'),
                                item.get('car_mark'),
                                item.get('part_full_name'),
                                item.get('car_model'),
                                item.get('year'),
                                item.get('price'),
                                item.get('in_stock'),
                                item.get('website')
                             ))
        
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        
class AutopiaPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        for field_name in field_names:
            value = adapter.get(field_name)

            
            if field_name == "in_stock":
                if value == "modal-wrapper":
                    adapter[field_name] = True
                else:
                    adapter[field_name] = False
            if field_name == "price":
                adapter[field_name] = int(extract_numbers(value)) if value else 0
            if field_name == "part_full_name" and "year" in field_names:
                part_full_name = value
                year = adapter.get("year")
                
                if part_full_name and year:
                    georgian_string, car_model = process_part_full_name_autopia(part_full_name, year)

                    if georgian_string is None or car_model is None:
                        spider.logger.info(f"Dropping item as part_full_name contains 'სატესტო': {part_full_name}")
                        return None 
                    
                    adapter["part_full_name"] = georgian_string
                    adapter["car_model"] = car_model
                else:
                    spider.logger.warning(f"Missing part_full_name or year for item: {item}")
                    
                    
        
        return item
    
    
