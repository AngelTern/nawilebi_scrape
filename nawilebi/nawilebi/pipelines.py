
from datetime import datetime
import mysql.connector
from itemadapter import ItemAdapter
import logging
import re
from utilities.additional_functions import *


class NawilebiPipeline:
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

            if field_name == "in_stock":
                if value == "modal-wrapper":
                    adapter[field_name] = True
                else:
                    adapter[field_name] = False

            if field_name == "part_full_name" and "year" in field_names:
                part_full_name = value
                year = adapter.get("year")
                car_mark = adapter.get("car_mark")

                if part_full_name and year:
                    georgian_string, car_model = process_part_full_name_autopia(part_full_name, year, car_mark)

                    if georgian_string is None or car_model is None:
                        spider.logger.info(f"Dropping item as part_full_name contains 'სატესტო': {part_full_name}")
                        return None

                    adapter["part_full_name"] = georgian_string
                    adapter["car_model"] = car_model
                else:
                    spider.logger.warning(f"Missing part_full_name or year for item: {item}")

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

        return item


class TopaoutopartsPipelines:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_model":
                year_range, car_model = process_car_model_topautoparts(value)
                adapter["year"] = year_range
                adapter["car_model"] = car_model
            if field_name == "part_full_name":
                adapter[field_name] = process_car_part_full_topautoparts(value, adapter.get("year"), adapter.get("car_model"))

        return item


class CarpartsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_model":
                adapter[field_name] = process_car_model_carparts(value)
            if field_name == "part_full_name":
                adapter[field_name] = process_part_full_name(value, adapter.get("car_model"))

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

        return item


class AutotransPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == "car_model":
                adapter["year"] = process_car_model_autotrans(value)
                adapter["car_model"] = clean_car_model_autotrans(value)

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
