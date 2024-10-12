
from datetime import datetime
import mysql.connector
from itemadapter import ItemAdapter
import logging
import re
from utilities.additional_functions import *
from scrapy.exceptions import DropItem

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
    
    phone_map = {
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
                "https://zupart.ge/ka": "555 52 24 90",
                "https://otoparts.ge/": "577 54 51 74",
                "https://megaautoparts.ge/": "568 68 55 36"
            }
    
    def process_item(self, item, spider):
        
        name_combinations = [
            ["ფრთა", "კრილო"],
            ["ფარი", "მაშუქი", "სტოპი"],
            ["სამაგრი", "ბრეკეტი", "სალასკა"],
            ["ფრთის საფენი", "პატკრილნიკი"],
            ["ძელი", "ბალკა"],
            ["ავზი", "ბაჩოკი"],
            ["ეკრანი", "რადიატორების დამჭერი"],
            ["ცხაურა", "აბლიცოვკა", "ბადე"],
            ["პეტლი", "ანჯამი"],
            ["ლოგო", "ემბლემა"],
            ["დამცავი", "საფარი"],
            ["ფილტრი", "ჰაერი"]
        ]
        
        adapter = ItemAdapter(item)
        part_full_name = adapter.get("part_full_name")
        
        alternative_names = []
        found_primary = False

        for name_list in name_combinations:
            for name in name_list:
                if name.lower() in part_full_name:
                    primary_name = name
                    alternative_names = [alt_name for alt_name in name_list if alt_name.lower() != primary_name.lower()]
                    found_primary = True
                    break
            if found_primary:
                break

        item["alternative_name_1"] = alternative_names[0] if len(alternative_names) >= 1 else None
        item["alternative_name_2"] = alternative_names[1] if len(alternative_names) >= 2 else None
        
        website = item.get('website')

        if website in self.phone_map:
            item['phone'] = self.phone_map[website]
        else:
            spider.logger.info(f'No phone number found for website: {website}')       
              
        return item



                    
        

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
        # Connect to the MySQL database using mysql.connector
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12XklsD!?NmG1509',
            database='nawilebi'
        )
        self.cur = self.conn.cursor()

        # Read freeze_yesterday and update_day from the text file
        self.freeze_yesterday, self.update_day = self.read_control_file()

        # Get the current date
        current_day = datetime.datetime.now().strftime("%Y-%m-%d")

        # Only proceed with table changes if update_day is not the current day
        if self.update_day != current_day:
            # If freeze_yesterday is 1, don't move data to nawilebi_yesterday
            if self.freeze_yesterday == 0:
                # Check if the 'nawilebi_yesterday' table exists, if not, create it
                self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS nawilebi_yesterday LIKE nawilebi;
                ''')

                # Truncate 'nawilebi_yesterday' if it already contains data
                self.cur.execute('''
                    TRUNCATE TABLE nawilebi_yesterday;
                ''')

                # Copy the data from 'nawilebi' to 'nawilebi_yesterday' (only if there's data in 'nawilebi')
                self.cur.execute('''
                    INSERT INTO nawilebi_yesterday SELECT * FROM nawilebi;
                ''')

            # Truncate 'nawilebi' to clear out the data without affecting the structure or triggers
            self.cur.execute('''
                TRUNCATE TABLE nawilebi;
            ''')

    def read_control_file(self):
        """
        Reads the control values from a text file.
        Expects a file format like:
        freeze_yesterday=0
        update_day=2024-10-08
        """
        freeze_yesterday = 0
        update_day = ""
        
        with open("control_file.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "freeze_yesterday" in line:
                    freeze_yesterday = int(line.split('=')[1].strip())
                if "update_day" in line:
                    update_day = line.split('=')[1].strip()
                    
        return freeze_yesterday, update_day

    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT INTO nawilebi(
                part_url, car_mark, car_model, part_full_name, alternative_name_1,
                alternative_name_2, start_year, end_year, price, original_price,
                in_stock, city, website, phone
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            item.get('part_url', ''),            
            item.get('car_mark', ''),            
            item.get('car_model', ''),           
            item.get('part_full_name', ''),      
            item.get('alternative_name_1', ''),  
            item.get('alternative_name_2', ''),  
            item.get('start_year', None),        
            item.get('end_year', None),          
            item.get('price', 0),                
            item.get('original_price', 0),       
            item.get('in_stock', False),         
            item.get('city', ''),                
            item.get('website', ''),             
            item.get('phone', '')                
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
                
            if field_name == "car_mark":
                adapter[field_name] = value.upper()

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
                adapter[field_name], year_value = process_part_full_name_carparts(value, adapter.get("car_model"), adapter.get("car_mark"))
            elif field_name == "year":
                if value != None:
                    adapter["year"], start_year, end_year = process_year_carparts(value)
                    adapter["start_year"] = int(start_year) if start_year else None
                    adapter["end_year"] = int(end_year) if end_year else None
                else:
                    adapter["year"], start_year, end_year = process_year_carparts(year_value)
                    adapter["start_year"] = int(start_year) if start_year else None
                    adapter["end_year"] = int(end_year) if end_year else None
            elif field_name == "price":
                adapter[field_name] = parse_price(value)
            elif field_name == "in_stock":
                if value == "მარაგშია":
                    adapter[field_name] = 1
                else:
                    adapter[field_name] = 0

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
            if field_name == "price":
                adapter["price"] = parse_price(value)
            if field_name == "year":
                if value:
                    adapter["start_year"] = int(value)

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
            elif field_name == "in_stock":
                if value == "მარაგშია":
                    adapter[field_name] = True
                else:
                    adapter[field_name] = False
            elif field_name == "car_mark":
                if value:
                    adapter[field_name] = value.upper()
            elif field_name == "car_model":
                if value and value == "akordi":
                    adapter[field_name] = "ACCORD"
                elif value and value == "hrv":
                    adapter[field_name] = "HR-V"
                else:
                    adapter[field_name] = value.upper()
                    
                
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
                    adapter[field_name] = process_part_full_name_goparts(value, adapter.get("car_model"), adapter.get("car_mark"))
            elif field_name == "in_stock":
                if value =="in_stock":
                    adapter[field_name] = 1
                else:
                    adapter[field_name] = 0
            elif field_name == "price":
                adapter[field_name] = parse_price(value)
            
        return item
    
class GeopartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        
        for field_name in field_names:
            value = adapter.get(field_name)

            if field_name == "car_mark" and value == "ᲢᲝᲘᲝᲢᲐ":
                
                adapter["car_mark"] = "TOYOTA"
                
            elif field_name == "car_model":
                adapter[field_name], adapter["start_year"], adapter["end_year"], adapter["year"] = process_car_model_geoparts(value, adapter.get("car_mark"))
            elif field_name in ["price", "original_price"]:
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
    
class SoloautoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"], adapter["start_year"], adapter["end_year"], adapter["year"] = process_car_model_proauto(car_model, adapter.get("car_mark"))
            
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
            
        car_mark = adapter.get("car_mark")
        if car_mark:
            adapter["car_mark"] = car_mark.upper()
            
        return item
    
class CrossmotorsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"], adapter["start_year"], adapter["end_year"], adapter["year"] = process_car_model_crossmotors(car_model)
            
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
            
        return item
    
class AutogamaPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        part_full_name = adapter.get("part_full_name")
        if part_full_name:
            adapter["part_full_name"], adapter["price"] = process_part_full_name_autogama(part_full_name)

        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_mark"], adapter["car_model"], adapter["start_year"], adapter["end_year"], adapter["year"] = process_car_model_autogama(car_model)

        return item

    
class ApgpartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        part_full_name = adapter.get("part_full_name")
        
        if 'აქსესუარი 1' in part_full_name:
            raise DropItem(f"Dropping item with part_full_name: {part_full_name}")
        
        if part_full_name:
            adapter["part_full_name"], adapter["car_mark"], adapter["car_model"], adapter["start_year"], adapter["end_year"], adapter["year"] = process_part_full_name_apgparts(part_full_name, adapter.get("car_model"))
        
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"] = car_model.strip().upper()
        
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
        
        return item

class PpPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        car_model = adapter.get('car_model')
        car_mark = adapter.get("car_mark")
        
        if car_model and car_mark:
            adapter["car_model"] = process_car_model_pp(car_model, car_mark)
            
        in_stock = adapter.get("in_stock")
        if in_stock:
            adapter["in_stock"] = process_in_stock_pp(in_stock)
            
        price = adapter.get("price")
        original_price = adapter.get("original_price")
        if price:
            adapter["price"] = procees_price_pp(price)
        if original_price:
            original_price_parsed = procees_price_pp(original_price)
            adapter["original_price"] = original_price_parsed if original_price_parsed and original_price_parsed != 0 else None
            
        year_list = adapter.get("year")
        if year_list:
            adapter["year"], adapter["start_year"], adapter["end_year"] = process_year_pp(year_list)
            
        part_full_name = adapter.get("part_full_name")
        if part_full_name:
            adapter["part_full_name"] = process_part_full_name_pp(part_full_name)
            
            
        return item
            
            
class MmautoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"], adapter["year"], adapter["start_year"], adapter["end_year"] = process_car_model_mmauto(car_model)
            
        in_stock = adapter.get("in_stock")
        if in_stock:
            adapter["in_stock"] = process_in_stock(in_stock)
            
        part_full_name = adapter.get("part_full_name")
        if part_full_name:
            adapter["part_full_name"] = part_full_name.strip()
            
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
            
            
        return item
    
class OtopartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"], adapter["year"], adapter["start_year"], adapter["end_year"] = process_car_model_otoparts(car_model, adapter.get("car_mark"))
            
        part_full_name = adapter.get("part_full_name")
        if part_full_name:
            adapter["part_full_name"] = re.sub(r"[-–]", "", part_full_name)
            
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
            
        car_mark = adapter.get("car_mark")
        if car_mark:
            adapter["car_mark"] = car_mark.upper()
            
        return item
    
class MetaautopartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        car_model = adapter.get("car_model")
        if car_model:
            adapter["car_model"], adapter["start_year"], adapter["end_year"], adapter["year"] = process_car_model_megaauto(car_model, adapter.get("car_mark"))
            
        price = adapter.get("price")
        if price:
            adapter["price"] = parse_price(price)
            
        return item
        
            
        