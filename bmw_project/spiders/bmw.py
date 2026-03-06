import scrapy
import json
from ..items import CarItem

class BmwSpider(scrapy.Spider):
    name = "bmw"

    async def start(self):
        yield scrapy.Request(
            url="https://usedcars.bmw.co.uk/",
            method="GET",
            callback=self.parse_initial,
            dont_filter=True
        )

    def parse_initial(self, response):
        csrf_token = ""
        for cookie in response.headers.getlist("Set-Cookie"):
            cookie_str = cookie.decode("utf-8")
            if "csrftoken" in cookie_str:
                parts = cookie_str.split("csrftoken=", 1)
                if len(parts) > 1:
                    csrf_token = parts[1].split(";")[0]

        url = "https://usedcars.bmw.co.uk/vehicle/api/list/?payment_type=cash&size=23&source=home&page=1"

        yield scrapy.Request(
            url,
            method="GET",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://usedcars.bmw.co.uk",
                "Referer": "https://usedcars.bmw.co.uk/",
                "X-CSRFToken": csrf_token,
                "Accept-Language": "en-US,en;q=0.9",
            },
            callback=self.parse,
            meta={"page": 1, "csrf_token": csrf_token}
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            data = {}

        cars_list = data.get("results", []) if isinstance(data, dict) else data

        for car in cars_list:
            item = CarItem()

            item["name"] = car.get("title") or car.get("name")
            item["model"] = car.get("derivative")
            item["mileage"] = car.get("mileage")

            # Registration
            reg = car.get("registration")
            if isinstance(reg, dict):
                item["registration"] = reg.get("registration")
                item["registered"] = reg.get("date")
            else:
                item["registration"] = reg
                item["registered"] = None

          
            eng = car.get("engine")
            if isinstance(eng, dict):
                engine_val = eng.get("litres") or eng.get("cc")
            else:
                engine_val = car.get("engine_capacity")
            
            if engine_val in (0, "0", 0.0):
                engine_val = None
            item["engine"] = engine_val

          
            consumption = car.get("consumption", {})
            range_data = consumption.get("range", {})
            range_val = None
            if isinstance(range_data, dict):
                values = range_data.get("values", {})
                total_range = values.get("total") or values.get("electric") or values.get("combined")
                unit = range_data.get("unit") or ""
                if total_range is not None:
                    range_val = f"{total_range} {unit}".strip()
            
           
            if not range_val:
                range_val = car.get("range")
            
       
            if range_val in (0, "0", "0 ", "0.0"):
                range_val = None

            item["range"] = range_val

     
            fuel = car.get("fuel_type") or car.get("fuel")
            item["fuel"] = fuel.get("name") if isinstance(fuel, dict) else fuel

            trans = car.get("transmission")
            item["transmission"] = trans.get("name") if isinstance(trans, dict) else trans

         
            ext = car.get("exterior_colour") or car.get("colour") or car.get("paint")
            exterior_val = ext.get("name") if isinstance(ext, dict) else ext

            uph = car.get("upholstery") or car.get("interior") or car.get("trim")
            upholstery_val = uph.get("name") if isinstance(uph, dict) else uph

            
            if not exterior_val or not upholstery_val:
                features = car.get("features", {})
                additional = features.get("additional", [])
                standard = features.get("standard", [])
                all_features = additional + standard

                if not exterior_val:
                    ext_feats = [
                        f.get("description") for f in all_features 
                        if str(f.get("category", "")).lower() in ("exterior", "paint", "exterior colour", "colour")
                    ]
                    if ext_feats:
                        exterior_val = ext_feats[0]

                if not upholstery_val:
                    int_feats = [
                        f.get("description") for f in all_features 
                        if str(f.get("category", "")).lower() in ("interior", "trim", "upholstery", "interior trim")
                    ]
                    if int_feats:
                        upholstery_val = int_feats[0]
                        
               
                if not exterior_val:
                    fallback_ext = [f.get("description") for f in all_features if "metallic" in str(f.get("description", "")).lower() or "paint" in str(f.get("description", "")).lower()]
                    if fallback_ext: exterior_val = fallback_ext[0]
                if not upholstery_val:
                    fallback_int = [f.get("description") for f in all_features if "leather" in str(f.get("description", "")).lower() or "cloth" in str(f.get("description", "")).lower()]
                    if fallback_int: upholstery_val = fallback_int[0]

            item["exterior"] = exterior_val if exterior_val else "Unspecified"
            item["upholstery"] = upholstery_val if upholstery_val else "Unspecified"

            yield item

        page = response.meta["page"]
        csrf_token = response.meta.get("csrf_token", "")

        if page < 5:
            next_page = page + 1
            url = f"https://usedcars.bmw.co.uk/vehicle/api/list/?payment_type=cash&size=23&source=home&page={next_page}"

            yield scrapy.Request(
                url,
                method="GET",
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://usedcars.bmw.co.uk",
                    "Referer": "https://usedcars.bmw.co.uk/",
                    "X-CSRFToken": csrf_token,
                },
                callback=self.parse,
                meta={"page": next_page, "csrf_token": csrf_token}
            )