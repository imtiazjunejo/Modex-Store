from app import app, db
from models import Product

with app.app_context():
    db.create_all()
    # Add sample products if not exist
    product_data = [
        {"name": "Classic Hoodie", "price": 7000, "image": "claasichodie.jpg", "category": "Hoodies"},
        {"name": "Premium T-Shirt", "price": 5000, "image": "moderntshirt.jpg", "category": "T-Shirts"},
        {"name": "Denim Jacket", "price": 11000, "image": "daniem jacket.jpg", "category": "Jackets"},
        {"name": "Blue Jeans", "price": 8000, "image": "bluejeans.jpg", "category": "Jeans"},
        {"name": "Black T-Shirt", "price": 4000, "image": "blacktshirt.jpg", "category": "T-Shirts"},
        {"name": "Grey Hoodie", "price": 6000, "image": "grey hodie.jpg", "category": "Hoodies"},
        {"name": "Leather Jacket", "price": 16000, "image": "latherjacj.jpg", "category": "Jackets"},
        {"name": "White Jeans", "price": 9000, "image": "whitejeans.jpg", "category": "Jeans"},
        {"name": "Snapback Cap", "price": 2500, "image": "snackback.jpg", "category": "Caps"},
        {"name": "Graphic T-Shirt", "price": 4500, "image": "graphic.jpg", "category": "T-Shirts"},
        {"name": "Pullover Hoodie", "price": 6500, "image": "pullover.jpg", "category": "Hoodies"},
        {"name": "Light Denim Jacket", "price": 10000, "image": "daniem jacket.jpg", "category": "Jackets"},
        {"name": "Cargo Pants", "price": 7500, "image": "cargo.jpg", "category": "Pants"},
        {"name": "Beanie", "price": 2000, "image": "beannie.jpg", "category": "Accessories"},
        {"name": "Hooded Jacket", "price": 12000, "image": "jacket.jpg", "category": "Jackets"},
        {"name": "Slim Fit Jeans", "price": 8500, "image": "jeans.jpg", "category": "Jeans"},
    ]

    for data in product_data:
        existing = Product.query.filter_by(name=data["name"]).first()
        if not existing:
            product = Product(name=data["name"], price=data["price"], image=data["image"], category=data["category"])
            db.session.add(product)
        elif existing.category is None or existing.category == "":
            existing.category = data["category"]
    db.session.commit()
    print("Products checked, added if missing, and updated categories.")
    print("Database initialized.")