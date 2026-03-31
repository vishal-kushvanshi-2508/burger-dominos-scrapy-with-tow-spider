# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import Error




class BurgerKingScrapyPipeline:
    def __init__(self):
        # Database configuration
        self.host = "localhost"
        self.user = "root"
        self.password = "actowiz"  # replace with your MySQL password
        self.port = "3306"
        self.database = "burgerking_scrapy_db"

    def open_spider(self, spider):
        """Runs when spider starts"""
        try:
            # Connect to MySQL server
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.conn.cursor()

            # Create database if not exists
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.conn.database = self.database

            # Create table if not exists with UNIQUE on city_link
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS burger_stores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                brand_name VARCHAR(255),
                state_name VARCHAR(255),
                city_name VARCHAR(255),
                city_link VARCHAR(255) ,
                address TEXT,
                pincode VARCHAR(20),
                phone_number VARCHAR(50),
                time VARCHAR(50),
                website VARCHAR(255),
                map VARCHAR(255)
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dominos_stores (
                id INT AUTO_INCREMENT PRIMARY KEY,

                brand_name VARCHAR(255),
                city_name VARCHAR(100),
                city_link TEXT,

                region VARCHAR(255),
                address TEXT,

                delivery_time VARCHAR(50),
                cost VARCHAR(100),
                time VARCHAR(100),
                good_for TEXT,

                phone_number VARCHAR(20)

            )
            """)
            self.conn.commit()

        except Error as e:
            spider.logger.error(f"Error connecting to MySQL: {e}")



    

    def process_item(self, item, spider):
        if spider.name == "burger_spider":
            self.insert_burgerking(item, spider)

        elif spider.name == "dominos_spider":
            self.insert_dominos(item, spider)
        return item


    def insert_burgerking(self, item, spider):

        """Insert each item into MySQL"""
        try:
            sql = """
            INSERT INTO burger_stores
            (brand_name, state_name, city_name, city_link, address, pincode, phone_number, time, website, map)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            address=VALUES(address),
            pincode=VALUES(pincode),
            phone_number=VALUES(phone_number),
            time=VALUES(time),
            website=VALUES(website),
            map=VALUES(map)
            """
            # print("process_items : ", item)
            values = (
                item.get('brand_name'),
                item.get('state_name'),
                item.get('city_name'),
                item.get('city_link'),
                item.get('address'),
                item.get('pincode'),
                item.get('phone_number'),
                item.get('time'),
                item.get('website'),
                item.get('map')
            )
            self.cursor.execute(sql, values)
            self.conn.commit()
        except Error as e:
            spider.logger.error(f"Error inserting item: {e}")
        return item



    def insert_dominos(self, item, spider):


        try:

            #  Insert query
            insert_query = """
            INSERT INTO dominos_stores (
                brand_name,
                city_name,
                city_link,
                region,
                address,
                delivery_time,
                cost,
                time,
                good_for,
                phone_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                item.get("brand_name"),
                item.get("city_name"),
                item.get("city_link"),
                item.get("region"),
                item.get("address"),
                item.get("delivery_time"),
                item.get("cost"),
                item.get("time"),
                item.get("good_for"),
                item.get("phone_number")
            )

            #  Execute query
            self.cursor.execute(insert_query, values)
            self.conn.commit()
        except Exception as e:
            print(" DB Error:", e)

        return item
    
    def close_spider(self, spider):
        """Close database connection when spider closes"""
        try:
            self.cursor.close()
            self.conn.close()
        except Error as e:
            spider.logger.error(f"Error closing MySQL connection: {e}")





