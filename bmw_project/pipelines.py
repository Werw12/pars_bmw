import sqlite3
from scrapy.exceptions import DropItem

class DataValidationPipeline:
    def process_item(self, item, spider):
        # Validate required fields
        for field in ['name', 'model', 'registration']:
            if not item.get(field):
                raise DropItem(f"Missing required field {field} in {item}")
        
        # Clean mileage
        mileage = item.get('mileage')
        if mileage:
            try:
                # Remove commas, spaces, etc., and convert to int
                # e.g., '8,143' -> 8143
                cleaned_mileage = str(mileage).replace(',', '').replace(' ', '')
                item['mileage'] = int(cleaned_mileage)
            except ValueError:
                spider.logger.warning(f"Could not convert mileage to int: {mileage}")
        
        # Lowercase fuel
        fuel = item.get('fuel')
        if fuel:
            item['fuel'] = str(fuel).lower()

        return item

class AsyncSQLitePipeline:

    def open_spider(self, spider):
        self.conn = sqlite3.connect("bmw_cars.db")
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("DROP TABLE IF EXISTS cars")

        self.cursor.execute("""
        CREATE TABLE cars (
            name TEXT,
            model TEXT,
            mileage INTEGER,
            registered TEXT,
            engine TEXT,
            range TEXT,
            fuel TEXT,
            transmission TEXT,
            registration TEXT,
            exterior TEXT,
            upholstery TEXT
        )
        """)

        self.conn.commit()

    def process_item(self, item, spider):
        self.cursor.execute("""
        INSERT INTO cars VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            item.get("name"),
            item.get("model"),
            item.get("mileage"),
            item.get("registered"),
            item.get("engine"),
            item.get("range"),
            item.get("fuel"),
            item.get("transmission"),
            item.get("registration"),
            item.get("exterior"),
            item.get("upholstery"),
        ))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
