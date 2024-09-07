# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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
                         CREATE TABLE IF NOT EXISTS nawilebi()
                         """)
    
    def process_item(self, item, spider):
        self.cur.execute("""
                         insert into nawilebi()""")
        
        self.conn.commit()
        return item
    
    def close_spider(self, item, spider):
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
                    adapter[field_name] = "in_stock"
                else:
                    adapter[field_name] = "not_stock"
        
        return item
    
    
