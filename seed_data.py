from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import (Base, User, Category, Brand, Product, Post, Image, Review,
                    Phone, Laptop, Accessory, Fashion, HomeAppliance, RoleEnum)
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'ecommerce')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Xoa du lieu cu va reset ID sequences
session.execute(text("TRUNCATE TABLE reviews, images, posts, phones, laptops, accessories, fashion, home_appliances, products, brands, categories, users RESTART IDENTITY CASCADE"))
session.commit()

# ========== 1. Users ==========
users = [
    User(full_name="Nguyen Van A", email="seller1@gmail.com", phone="0901234567", password="hash123", role=RoleEnum.seller),
    User(full_name="Tran Thi B", email="seller2@gmail.com", phone="0912345678", password="hash123", role=RoleEnum.seller),
    User(full_name="Le Van C", email="buyer1@gmail.com", phone="0923456789", password="hash123", role=RoleEnum.buyer),
    User(full_name="Pham Thi D", email="buyer2@gmail.com", phone="0934567890", password="hash123", role=RoleEnum.buyer),
    User(full_name="Hoang Van E", email="both1@gmail.com", phone="0945678901", password="hash123", role=RoleEnum.both),
    User(full_name="Vo Thi F", email="seller3@gmail.com", phone="0956789012", password="hash123", role=RoleEnum.seller),
    User(full_name="Dang Van G", email="buyer3@gmail.com", phone="0967890123", password="hash123", role=RoleEnum.buyer),
    User(full_name="Bui Thi H", email="buyer4@gmail.com", phone="0978901234", password="hash123", role=RoleEnum.buyer),
    User(full_name="Ngo Van I", email="both2@gmail.com", phone="0989012345", password="hash123", role=RoleEnum.both),
    User(full_name="Ly Thi K", email="seller4@gmail.com", phone="0990123456", password="hash123", role=RoleEnum.seller),
]
session.add_all(users)
session.commit()

# ========== 2. Categories ==========
categories = [
    Category(category="Dien thoai"),
    Category(category="Laptop"),
    Category(category="Phu kien"),
    Category(category="Thoi trang"),
    Category(category="Gia dung"),
]
session.add_all(categories)
session.commit()

# ========== 3. Brands ==========
brands = [
    Brand(brand="Apple"),
    Brand(brand="Samsung"),
    Brand(brand="Xiaomi"),
    Brand(brand="Dell"),
    Brand(brand="Sony"),
    Brand(brand="Nike"),
    Brand(brand="Panasonic"),
    Brand(brand="Asus"),
    Brand(brand="Adidas"),
    Brand(brand="LG"),
    Brand(brand="Oppo"),
    Brand(brand="HP"),
    Brand(brand="JBL"),
    Brand(brand="Uniqlo"),
    Brand(brand="Sunhouse"),
]
session.add_all(brands)
session.commit()

# ========== 4. Products + Detail tables ==========

# --- 10 Dien thoai ---
phones_data = [
    (Product(name="iPhone 15 Pro Max", category_id=1, brand_id=1, weight=221),
     Phone(screen_size=6.7, ram=8, storage=256, battery=4422, os="iOS")),
    (Product(name="Samsung Galaxy S24", category_id=1, brand_id=2, weight=195),
     Phone(screen_size=6.2, ram=8, storage=256, battery=4000, os="Android")),
    (Product(name="Xiaomi 14", category_id=1, brand_id=3, weight=188),
     Phone(screen_size=6.4, ram=12, storage=256, battery=4610, os="Android")),
    (Product(name="iPhone 14", category_id=1, brand_id=1, weight=172),
     Phone(screen_size=6.1, ram=6, storage=128, battery=3279, os="iOS")),
    (Product(name="Samsung Galaxy A55", category_id=1, brand_id=2, weight=213),
     Phone(screen_size=6.6, ram=8, storage=128, battery=5000, os="Android")),
    (Product(name="Xiaomi Redmi Note 13", category_id=1, brand_id=3, weight=188),
     Phone(screen_size=6.7, ram=8, storage=128, battery=5000, os="Android")),
    (Product(name="Oppo Reno 11", category_id=1, brand_id=11, weight=184),
     Phone(screen_size=6.7, ram=12, storage=256, battery=5000, os="Android")),
    (Product(name="Samsung Galaxy Z Flip 5", category_id=1, brand_id=2, weight=187),
     Phone(screen_size=6.7, ram=8, storage=256, battery=3700, os="Android")),
    (Product(name="iPhone 15", category_id=1, brand_id=1, weight=171),
     Phone(screen_size=6.1, ram=6, storage=128, battery=3349, os="iOS")),
    (Product(name="Xiaomi 13T Pro", category_id=1, brand_id=3, weight=206),
     Phone(screen_size=6.7, ram=12, storage=512, battery=5000, os="Android")),
]

for prod, phone in phones_data:
    session.add(prod)
    session.flush()
    phone.product_id = prod.product_id
    session.add(phone)
session.commit()

# --- 10 Laptop ---
laptops_data = [
    (Product(name="Dell XPS 15", category_id=2, brand_id=4, weight=1860),
     Laptop(screen_size=15.6, ram=32, storage=1024, cpu="Intel Core i7-13700H", gpu="RTX 4060", battery_hours=11)),
    (Product(name="MacBook Pro 14", category_id=2, brand_id=1, weight=1600),
     Laptop(screen_size=14.2, ram=18, storage=512, cpu="Apple M3 Pro", gpu="Integrated", battery_hours=17)),
    (Product(name="Asus ROG Strix G16", category_id=2, brand_id=8, weight=2500),
     Laptop(screen_size=16.0, ram=16, storage=512, cpu="Intel Core i9-13980HX", gpu="RTX 4070", battery_hours=5)),
    (Product(name="HP Pavilion 15", category_id=2, brand_id=12, weight=1740),
     Laptop(screen_size=15.6, ram=16, storage=512, cpu="Intel Core i5-1335U", gpu="Integrated", battery_hours=10)),
    (Product(name="MacBook Air 15", category_id=2, brand_id=1, weight=1510),
     Laptop(screen_size=15.3, ram=16, storage=256, cpu="Apple M2", gpu="Integrated", battery_hours=18)),
    (Product(name="Dell Inspiron 14", category_id=2, brand_id=4, weight=1540),
     Laptop(screen_size=14.0, ram=8, storage=256, cpu="Intel Core i5-1235U", gpu="Integrated", battery_hours=8)),
    (Product(name="Asus Zenbook 14", category_id=2, brand_id=8, weight=1390),
     Laptop(screen_size=14.0, ram=16, storage=512, cpu="Intel Core Ultra 7", gpu="Integrated", battery_hours=13)),
    (Product(name="HP Envy x360", category_id=2, brand_id=12, weight=1580),
     Laptop(screen_size=14.0, ram=16, storage=512, cpu="AMD Ryzen 7 7730U", gpu="Integrated", battery_hours=12)),
    (Product(name="MacBook Pro 16", category_id=2, brand_id=1, weight=2140),
     Laptop(screen_size=16.2, ram=36, storage=1024, cpu="Apple M3 Max", gpu="Integrated", battery_hours=22)),
    (Product(name="Asus TUF Gaming F15", category_id=2, brand_id=8, weight=2200),
     Laptop(screen_size=15.6, ram=16, storage=512, cpu="Intel Core i7-12700H", gpu="RTX 4050", battery_hours=6)),
]

for prod, laptop in laptops_data:
    session.add(prod)
    session.flush()
    laptop.product_id = prod.product_id
    session.add(laptop)
session.commit()

# --- 10 Phu kien ---
accessories_data = [
    (Product(name="Tai nghe Sony WH-1000XM5", category_id=3, brand_id=5, weight=250),
     Accessory(accessory_type="Tai nghe", compatible_with="Universal", material="Nhua + Da")),
    (Product(name="Apple AirPods Pro", category_id=3, brand_id=1, weight=50),
     Accessory(accessory_type="Tai nghe", compatible_with="Apple", material="Nhua")),
    (Product(name="JBL Flip 6", category_id=3, brand_id=13, weight=550),
     Accessory(accessory_type="Loa bluetooth", compatible_with="Universal", material="Vai + Nhua")),
    (Product(name="Samsung Buds 2 Pro", category_id=3, brand_id=2, weight=51),
     Accessory(accessory_type="Tai nghe", compatible_with="Samsung", material="Nhua")),
    (Product(name="Apple Watch Ultra 2", category_id=3, brand_id=1, weight=61),
     Accessory(accessory_type="Dong ho thong minh", compatible_with="Apple", material="Titanium")),
    (Product(name="Sac nhanh Xiaomi 67W", category_id=3, brand_id=3, weight=120),
     Accessory(accessory_type="Sac", compatible_with="Universal", material="Nhua")),
    (Product(name="Op lung iPhone 15 Spigen", category_id=3, brand_id=1, weight=35),
     Accessory(accessory_type="Op lung", compatible_with="iPhone 15", material="TPU")),
    (Product(name="JBL Tune 520BT", category_id=3, brand_id=13, weight=155),
     Accessory(accessory_type="Tai nghe", compatible_with="Universal", material="Nhua")),
    (Product(name="Samsung Galaxy Watch 6", category_id=3, brand_id=2, weight=59),
     Accessory(accessory_type="Dong ho thong minh", compatible_with="Samsung", material="Nhom")),
    (Product(name="Sony WF-1000XM5", category_id=3, brand_id=5, weight=52),
     Accessory(accessory_type="Tai nghe", compatible_with="Universal", material="Nhua")),
]

for prod, acc in accessories_data:
    session.add(prod)
    session.flush()
    acc.product_id = prod.product_id
    session.add(acc)
session.commit()

# --- 10 Thoi trang ---
fashion_data = [
    (Product(name="Ao thun Nike Dri-FIT", category_id=4, brand_id=6, weight=200),
     Fashion(size="L", color="Den", material="Polyester", gender="Unisex")),
    (Product(name="Giay Nike Air Max", category_id=4, brand_id=6, weight=350),
     Fashion(size="42", color="Trang", material="Da + Vai", gender="Nam")),
    (Product(name="Ao hoodie Adidas Essentials", category_id=4, brand_id=9, weight=450),
     Fashion(size="XL", color="Xam", material="Cotton", gender="Nam")),
    (Product(name="Quan jogger Nike", category_id=4, brand_id=6, weight=300),
     Fashion(size="M", color="Den", material="Polyester", gender="Nam")),
    (Product(name="Ao khoac Uniqlo Ultra Light Down", category_id=4, brand_id=14, weight=250),
     Fashion(size="L", color="Xanh navy", material="Nylon", gender="Unisex")),
    (Product(name="Giay Adidas Ultraboost", category_id=4, brand_id=9, weight=310),
     Fashion(size="43", color="Den", material="Primeknit", gender="Nam")),
    (Product(name="Ao thun Uniqlo U", category_id=4, brand_id=14, weight=180),
     Fashion(size="M", color="Trang", material="Cotton", gender="Unisex")),
    (Product(name="Quan short Nike Flex", category_id=4, brand_id=6, weight=150),
     Fashion(size="L", color="Den", material="Polyester", gender="Nam")),
    (Product(name="Ao polo Adidas", category_id=4, brand_id=9, weight=220),
     Fashion(size="XL", color="Xanh la", material="Cotton + Polyester", gender="Nam")),
    (Product(name="Giay Nike Pegasus 40", category_id=4, brand_id=6, weight=280),
     Fashion(size="41", color="Xanh", material="Mesh + Cao su", gender="Unisex")),
]

for prod, fash in fashion_data:
    session.add(prod)
    session.flush()
    fash.product_id = prod.product_id
    session.add(fash)
session.commit()

# --- 10 Gia dung ---
appliance_data = [
    (Product(name="Quat Panasonic F-409K", category_id=5, brand_id=7, weight=5000),
     HomeAppliance(power=65, voltage=220, warranty_months=24)),
    (Product(name="Noi com dien Panasonic SR-CP108", category_id=5, brand_id=7, weight=3200),
     HomeAppliance(power=750, voltage=220, warranty_months=12)),
    (Product(name="May loc khong khi LG PuriCare", category_id=5, brand_id=10, weight=7500),
     HomeAppliance(power=48, voltage=220, warranty_months=24)),
    (Product(name="Tu lanh LG Inverter 335L", category_id=5, brand_id=10, weight=66000),
     HomeAppliance(power=150, voltage=220, warranty_months=24)),
    (Product(name="May giat Samsung 9kg", category_id=5, brand_id=2, weight=58000),
     HomeAppliance(power=500, voltage=220, warranty_months=24)),
    (Product(name="Dieu hoa Panasonic 1HP", category_id=5, brand_id=7, weight=35000),
     HomeAppliance(power=900, voltage=220, warranty_months=36)),
    (Product(name="Lo vi song LG NeoChef", category_id=5, brand_id=10, weight=12500),
     HomeAppliance(power=1200, voltage=220, warranty_months=12)),
    (Product(name="May hut bui Samsung Jet", category_id=5, brand_id=2, weight=2700),
     HomeAppliance(power=550, voltage=220, warranty_months=12)),
    (Product(name="Binh nong lanh Panasonic", category_id=5, brand_id=7, weight=8000),
     HomeAppliance(power=2500, voltage=220, warranty_months=36)),
    (Product(name="Noi chien khong dau Sunhouse SHD5058", category_id=5, brand_id=15, weight=4500),
     HomeAppliance(power=1500, voltage=220, warranty_months=12)),
]

for prod, app in appliance_data:
    session.add(prod)
    session.flush()
    app.product_id = prod.product_id
    session.add(app)
session.commit()

# ========== 5. Posts ==========
# Giá thực tế theo từng sản phẩm (VND)
real_prices = [
    # --- 10 Dien thoai ---
    (34990000, 32990000),   # iPhone 15 Pro Max
    (22990000, 20990000),   # Samsung Galaxy S24
    (12990000, 11490000),   # Xiaomi 14
    (19990000, 17990000),   # iPhone 14
    (9490000, 8490000),     # Samsung Galaxy A55
    (4990000, 4490000),     # Xiaomi Redmi Note 13
    (9990000, 8990000),     # Oppo Reno 11
    (25990000, 23990000),   # Samsung Galaxy Z Flip 5
    (22990000, 21490000),   # iPhone 15
    (11990000, 10990000),   # Xiaomi 13T Pro

    # --- 10 Laptop ---
    (35990000, 33990000),   # Dell XPS 15
    (43990000, None),       # MacBook Pro 14
    (32990000, 29990000),   # Asus ROG Strix G16
    (15990000, 14490000),   # HP Pavilion 15
    (27490000, None),       # MacBook Air 15
    (13990000, 12490000),   # Dell Inspiron 14
    (22990000, 20990000),   # Asus Zenbook 14
    (19990000, 17990000),   # HP Envy x360
    (67990000, None),       # MacBook Pro 16
    (24990000, 22990000),   # Asus TUF Gaming F15

    # --- 10 Phu kien ---
    (7490000, 6490000),     # Sony WH-1000XM5
    (5990000, 5490000),     # Apple AirPods Pro
    (2490000, 2190000),     # JBL Flip 6
    (3490000, 2990000),     # Samsung Buds 2 Pro
    (21990000, None),       # Apple Watch Ultra 2
    (490000, 390000),       # Sac nhanh Xiaomi 67W
    (390000, 290000),       # Op lung Spigen
    (1290000, 990000),      # JBL Tune 520BT
    (6490000, 5490000),     # Samsung Galaxy Watch 6
    (5990000, 4990000),     # Sony WF-1000XM5

    # --- 10 Thoi trang ---
    (690000, 590000),       # Ao thun Nike Dri-FIT
    (3990000, 3490000),     # Giay Nike Air Max
    (1890000, 1590000),     # Ao hoodie Adidas
    (1290000, 990000),      # Quan jogger Nike
    (1990000, None),        # Ao khoac Uniqlo Ultra Light Down
    (4290000, 3790000),     # Giay Adidas Ultraboost
    (390000, 290000),       # Ao thun Uniqlo U
    (890000, 690000),       # Quan short Nike Flex
    (1290000, 990000),      # Ao polo Adidas
    (3290000, 2890000),     # Giay Nike Pegasus 40

    # --- 10 Gia dung ---
    (1290000, 1090000),     # Quat Panasonic
    (1790000, 1590000),     # Noi com dien Panasonic
    (8990000, 7990000),     # May loc khong khi LG
    (12490000, 10990000),   # Tu lanh LG 335L
    (8990000, 7990000),     # May giat Samsung 9kg
    (9990000, None),        # Dieu hoa Panasonic 1HP
    (3290000, 2790000),     # Lo vi song LG
    (7990000, 6990000),     # May hut bui Samsung Jet
    (4990000, 4490000),     # Binh nong lanh Panasonic
    (1490000, 1190000),     # Noi chien khong dau Sunhouse
]

all_products = session.query(Product).all()
sellers = [1, 2, 6, 10]  # user_ids co role seller

posts = []
for i, prod in enumerate(all_products):
    seller_id = sellers[i % len(sellers)]
    price, sale_price = real_prices[i]
    posts.append(Post(
        seller_id=seller_id,
        product_id=prod.product_id,
        description=f"Ban {prod.name} chinh hang, moi 100%",
        price=price,
        sale_price=sale_price,
        currency="VND",
        status="active",
        quantity=(i + 1) * 5,
        sold_count=(i + 1) * 2,
    ))
session.add_all(posts)
session.commit()

# ========== 6. Images ==========
all_posts = session.query(Post).all()
images = []
for post in all_posts:
    images.append(Image(post_id=post.post_id, image_url=f"https://example.com/product-{post.post_id}-1.jpg"))
    images.append(Image(post_id=post.post_id, image_url=f"https://example.com/product-{post.post_id}-2.jpg"))
session.add_all(images)
session.commit()

# ========== 7. Reviews ==========
buyers = [3, 4, 7, 8]  # user_ids co role buyer
comments = [
    "San pham chat luong, giao hang nhanh",
    "Hang dung mo ta, se ung ho lan sau",
    "Gia tot, dang dong tien",
    "Dong goi can than, san pham dep",
    "Rat hai long, se gioi thieu ban be",
]

reviews = []
for i, post in enumerate(all_posts):
    buyer_id = buyers[i % len(buyers)]
    reviews.append(Review(
        post_id=post.post_id,
        buyer_id=buyer_id,
        rating=(i % 3) + 3,  # rating 3-5
        comment=comments[i % len(comments)],
    ))
session.add_all(reviews)
session.commit()

print("Da insert du lieu mau thanh cong!")
print(f"- Users: {session.query(User).count()}")
print(f"- Categories: {session.query(Category).count()}")
print(f"- Brands: {session.query(Brand).count()}")
print(f"- Products: {session.query(Product).count()}")
print(f"  + Phones: {session.query(Phone).count()}")
print(f"  + Laptops: {session.query(Laptop).count()}")
print(f"  + Accessories: {session.query(Accessory).count()}")
print(f"  + Fashion: {session.query(Fashion).count()}")
print(f"  + Home Appliances: {session.query(HomeAppliance).count()}")
print(f"- Posts: {session.query(Post).count()}")
print(f"- Images: {session.query(Image).count()}")
print(f"- Reviews: {session.query(Review).count()}")

session.close()
