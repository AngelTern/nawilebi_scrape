import json

# Correct the way the data is passed as a string
data = json.loads("""
{
    "status": true,
    "count": 5,
    "result": [
        {
            "id": 1383,
            "photo": {
                "toArray": [
                    {
                        "filename": "/uploads/products/1383/thumb_20a27ead45aa63ef69dbe8c36841e31d.jpeg",
                        "large": "/uploads/products/1383/normal_20a27ead45aa63ef69dbe8c36841e31d.jpeg",
                        "isMainPhoto": false
                    }
                ],
                "second_image": {
                    "thumb": "/uploads/products/1383/thumb_20a27ead45aa63ef69dbe8c36841e31d.jpeg",
                    "large": "/uploads/products/1383/normal_20a27ead45aa63ef69dbe8c36841e31d.jpeg"
                },
                "first_image": {
                    "thumb": "/uploads/products/1383/thumb_20a27ead45aa63ef69dbe8c36841e31d.jpeg",
                    "large": "/uploads/products/1383/normal_20a27ead45aa63ef69dbe8c36841e31d.jpeg"
                }
            },
            "manufacturer": [
                {
                    "id": 28,
                    "name": "Audi Audi A4 2008-2012",
                    "photo": "/uploads/manufacturers/models/audi-a4-2008-2012.png"
                }
            ],
            "title": "\u10d9\u10d0\u10de\u10dd\u10e2\u10d8\u10e1 \u10de\u10d4\u10e2\u10da\u10d8",
            "short_description": "",
            "long_description": "",
            "meta_title": "",
            "meta_keywords": "",
            "meta_description": "",
            "price": {
                "calculated": 0,
                "price": 70,
                "discount": 0,
                "final_price": 0,
                "spatial_price": 0,
                "is_active": true
            },
            "categories": []
        }
    ]
}
""")

# Loop over the items and print the manufacturer
for item in data["result"]:
    print(item.get("title"))
