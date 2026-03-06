import sqlite3


class AsyncSQLitePipeline:

    def open_spider(self):

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

    def process_item(self, item):

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

    def close_spider(self):

        self.conn.close()