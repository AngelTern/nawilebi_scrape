
from datetime import datetime
import mysql.connector
from itemadapter import ItemAdapter
import logging
import re
from utilities.additional_functions import *


'''class NawilebiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        in_stock_value = adapter.get("in_stock")

        if isinstance(in_stock_value, bool):
            adapter["in_stock"] = in_stock_value
        elif isinstance(in_stock_value, str):
            in_stock_value = in_stock_value.strip()
            if in_stock_value == "მარაგშია":
                adapter["in_stock"] = True
            else:
                adapter["in_stock"] = False
        else:
            adapter["in_stock"] = False

        field_names = adapter.field_names()

        for field_name in field_names:
            value = adapter.get(field_name)

            if isinstance(value, str):
                adapter[field_name] = value.strip()
            if field_name == "price":
                adapter[field_name] = parse_price(value)
            if field_name == "original_price":
                if value is not None:
                    adapter[field_name] = parse_price(value)

        return item
'''
class NawilebiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        adapter['start_year'] = int(adapter.get("start_year"))
        adapter['end_year'] = int(adapter.get("end_year"))
        

class YearProcessPipeline:
    def process_item(self, item, spider):
        year_str = item.get('year', None)
        start_year = None
        end_year = None

        if year_str:
            year_str = year_str.strip()
            if '-' in year_str:
                parts = year_str.split('-')
                if len(parts) == 2:
                    start_year_str = parts[0].strip()
                    try:
                        start_year = int(start_year_str)
                    except ValueError:
                        start_year = None

                    end_year_str = parts[1].strip()
                    if end_year_str == '':
                        end_year = datetime.now().year
                    else:
                        try:
                            end_year = int(end_year_str)
                        except ValueError:
                            end_year = None
            else:
                try:
                    start_year = int(year_str)
                    end_year = start_year
                except ValueError:
                    start_year = None
                    end_year = None

        item['start_year'] = start_year
        item['end_year'] = end_year

        return item


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12XklsD!?NmG1509',
            database='nawilebi'
        )
        self.cur = self.conn.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS nawilebi(
                id int NOT NULL auto_increment,
                part_url VARCHAR(1000),
                car_mark VARCHAR(70),
                car_model VARCHAR(150),
                part_full_name VARCHAR(150),
                start_year INT,
                end_year INT,
                price NUMERIC,
                original_price NUMERIC,
                in_stock BOOLEAN,
                website VARCHAR(255),
                city VARCHAR(50),
                PRIMARY KEY (id)
            )
        ''')

    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT INTO nawilebi(
                part_url, car_mark, car_model, part_full_name,
                start_year, end_year, price, original_price,
                in_stock, city, website
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            item.get('part_url'),
            item.get('car_mark'),
            item.get('car_model'),
            item.get('part_full_name'),
            item.get('start_year'),
            item.get('end_year'),
            item.get('price'),
            item.get('original_price'),
            item.get('in_stock'),
            item.get('city'),
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
            
            if isinstance(value, str):
                adapter[field_name] = value.strip()

            if field_name == "car_mark":
                adapter[field_name] = value.upper().strip()
                
            elif field_name == "car_model":
                car_model_adjusted, car_model_unchanged = process_car_model_autopia(value, adapter.get("car_mark"))
                adapter[field_name] = car_model_adjusted
                
            elif field_name == "in_stock":
                if value == "modal-wrapper":
                    adapter[field_name] = True
                else:
                    adapter[field_name] = False
                
            elif field_name == "part_full_name":
                car_model_unchanged = adapter.get("car_model") if 'car_model' in adapter else ""
                adapter[field_name] = process_part_full_name_autopia(value, adapter.get("car_model"), adapter.get("car_mark"))
                
            elif field_name == "price":
                adapter[field_name] = parse_price(value)
            elif field_name == "year":
                adapter["start_year"], adapter["end_year"] = process_year_autopia(value)
                
        return item


class VgpartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_model":
                year, car_model = process_car_model_vgparts(value)
                adapter["year"] = year
                adapter["car_model"] = car_model
            elif field_name == "year":
                adapter["start_year"], adapter["end_year"] = process_year_vgparts(value)

        return item


class TopautopartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        year_range, car_model, start_year, end_year = None, None, None, None
        
        for field_name in field_names:
            value = adapter.get(field_name)

            if field_name == "car_model":
                year_range, car_model, start_year, end_year = process_car_model_topautoparts(value)
                adapter["start_year"] = int(start_year) if start_year else None
                adapter["end_year"] = int(end_year) if end_year else None
                adapter["year"] = year_range
                adapter["car_model"] = car_model

            if field_name == "part_full_name":
                adapter[field_name] = process_car_part_full_topautoparts(value, car_model)

            if field_name == "price":
                adapter[field_name] = parse_price(value)

        return item

class CarpartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_model":
                adapter[field_name] = process_car_model_carparts(value)
            elif field_name == "part_full_name":
                adapter[field_name] = process_part_full_name_carparts(value, adapter.get("car_model"), adapter.get("car_mark"))
            elif field_name == "year":
                adapter["year"], start_year, end_year = process_year_carparts(value)
                adapter["start_year"] = int(start_year) if start_year else None
                adapter["end_year"] = int(end_year) if end_year else None
            elif field_name == "price":
                adapter[field_name] = parse_price(value)

        return item

class VsautoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_model":
                year, car_model = process_car_model_vsauto(value)
                adapter["year"] = year
                adapter["car_model"] = car_model
            elif field_name == "price":
                adapter[field_name] = float(value) if float(value) else None
            elif field_name == "year":
                adapter["start_year"], adapter["end_year"] = process_year_vsauto(value)
        return item


class AutotransPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_model":
                start_year, end_year, cleaned_car_model = process_and_clean_car_model_autotrans(value)
                adapter["start_year"] = start_year
                adapter["end_year"] = end_year
                adapter["car_model"] = cleaned_car_model

        return item

class CarlinePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_mark":
                if value == "KIA":
                    adapter["car_model"], adapter["part_full_name"] = process_kia_carline(adapter.get("part_full_name"))
            if field_name == "car_model":
                adapter["year"], adapter[field_name] = clean_car_model_carline(value, adapter.get("car_mark"))
            if field_name == "in_stock":
                if value == 'არ არის მარაგში':
                    adapter[field_name] = False
                elif value == "მარაგში":
                    adapter[field_name] = True
            elif field_name == "part_full_name":
                adapter["part_full_name"] = process_part_full_name_carline(value, adapter.get("car_model"), adapter.get("car_mark"))

        return item

class PartscornerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "year":
                adapter["start_year"], adapter["end_year"] = process_year_partscorner(value)
            elif field_name == "price":
                adapter["price"] = parse_price(value)
                
        return item
    
class GopartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            
            if isinstance(value, str):
                adapter[field_name] = value.strip()
                
            if field_name == "car_mark":
                if value == "B.M.W":
                    adapter[field_name] = re.sub(r'[^a-zA-Z]', '', value)
                elif value == "MERCEDES-BENZ":
                    adapter[field_name] = "MERCEDES"
            elif field_name == "car_model":
                adapter[field_name], adapter["start_year"], adapter["end_year"], adapter["year"] = process_year_goparts(value)
            elif field_name == "part_full_name":
                if value == "0- საქარე მინის გერმეტიკი 310მლ":
                    adapter[field_name] = "საქარე მინის გერმეტიკი 310მლ"
                else:
                    adapter[field_name] = process_part_full_name_goparts(value)
            
        return item
    
class GeoparsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            
            if field_name == "car_model":
                adapter[field_name], adapter["start_year"], adapter["end_year"], adapter["year"] = process_car_model_geoparts(value, adapter.get("car_mark"))
            elif field_name == "price" or field_name == "original_price":
                adapter[field_name] = parse_price(value)
                
        return item
    
class ZupartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        car_model = adapter.get('car_model')
        if car_model:
            if "19980-05" in car_model:
                car_model = car_model.replace("19980-05", "1998-05")
            adapter['car_model'], adapter['start_year'], adapter['end_year'], adapter['year'] = process_car_model_zuparts(car_model)

        price = adapter.get('price')
        if price:
            adapter['price'] = parse_price(price)
        
        return item

class NewpartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
        
        year = adapter.get("year")
        if year:
            adapter["year"], adapter["start_year"], adapter["end_year"] = process_year_newparts(year)
        
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"] = process_car_model_newparts(car_model)
        return item
    
class BgautoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
            
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"], adapter["start_year"], adapter["end_year"], adapter["year"] = process_car_model_bgauto(car_model, adapter.get("car_mark"))
        
        part_full_name = adapter.get("part_full_name")
        if part_full_name:
            adapter["part_full_name"] = process_part_full_name_bgauto(part_full_name)
        
        return item
    
class ProautoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        year = adapter.get("year")
        if year:
            adapter["start_year"], adapter["end_year"], adapter["year"] = process_year_proauto(year)
            
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
        
        original_price = adapter.get("original_price")
        if original_price:
            adapter["original_price"] = parse_price(original_price)
            
        
        return item