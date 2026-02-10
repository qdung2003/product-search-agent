from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class RoleEnum(enum.Enum):
    buyer = "buyer"
    seller = "seller"
    both = "both"


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    user_created_at = Column(DateTime, server_default=func.now())
    role = Column(Enum(RoleEnum), default=RoleEnum.buyer)

    # Relationships
    posts = relationship("Post", back_populates="seller", foreign_keys="Post.seller_id")
    reviews = relationship("Review", back_populates="buyer", foreign_keys="Review.buyer_id")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False, unique=True)

    # Relationships
    products = relationship("Product", back_populates="category_rel")


class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True)
    brand = Column(String(100), nullable=False, unique=True)

    # Relationships
    products = relationship("Product", back_populates="brand_rel")


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    weight = Column(Numeric(10, 2))

    # Relationships
    category_rel = relationship("Category", back_populates="products")
    brand_rel = relationship("Brand", back_populates="products")
    posts = relationship("Post", back_populates="product")
    phone = relationship("Phone", back_populates="product", uselist=False)
    laptop = relationship("Laptop", back_populates="product", uselist=False)
    accessory = relationship("Accessory", back_populates="product", uselist=False)
    fashion = relationship("Fashion", back_populates="product", uselist=False)
    home_appliance = relationship("HomeAppliance", back_populates="product", uselist=False)


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), unique=True, nullable=False)
    screen_size = Column(Numeric(3, 1))       # inch (6.7)
    ram = Column(Integer)                      # GB
    storage = Column(Integer)                  # GB
    battery = Column(Integer)                  # mAh
    os = Column(String(50))                    # iOS, Android

    product = relationship("Product", back_populates="phone")


class Laptop(Base):
    __tablename__ = 'laptops'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), unique=True, nullable=False)
    screen_size = Column(Numeric(3, 1))       # inch (15.6)
    ram = Column(Integer)                      # GB
    storage = Column(Integer)                  # GB
    cpu = Column(String(100))                  # Intel i7, Apple M3
    gpu = Column(String(100))                  # RTX 4060, Integrated
    battery_hours = Column(Integer)            # Thoi luong pin (gio)

    product = relationship("Product", back_populates="laptop")


class Accessory(Base):
    __tablename__ = 'accessories'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), unique=True, nullable=False)
    accessory_type = Column(String(100))       # Tai nghe, Sac, Op lung
    compatible_with = Column(String(200))      # iPhone, Samsung, Universal
    material = Column(String(100))             # Nhua, Kim loai, Da

    product = relationship("Product", back_populates="accessory")


class Fashion(Base):
    __tablename__ = 'fashion'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), unique=True, nullable=False)
    size = Column(String(10))                  # S, M, L, XL
    color = Column(String(50))
    material = Column(String(100))             # Cotton, Polyester, Len
    gender = Column(String(20))                # Nam, Nu, Unisex

    product = relationship("Product", back_populates="fashion")


class HomeAppliance(Base):
    __tablename__ = 'home_appliances'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), unique=True, nullable=False)
    power = Column(Integer)                    # Watt
    voltage = Column(Integer)                  # Volt (220V)
    warranty_months = Column(Integer)          # Thang bao hanh

    product = relationship("Product", back_populates="home_appliance")


class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    description = Column(Text)
    price = Column(Numeric(12, 2), nullable=False)
    sale_price = Column(Numeric(12, 2))
    currency = Column(String(10), default='VND')
    status = Column(String(50), default='active')
    quantity = Column(Integer, default=0)
    sold_count = Column(Integer, default=0)
    post_created_at = Column(DateTime, server_default=func.now())
    post_updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    seller = relationship("User", back_populates="posts", foreign_keys=[seller_id])
    product = relationship("Product", back_populates="posts")
    images = relationship("Image", back_populates="post")
    reviews = relationship("Review", back_populates="post")


class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    image_url = Column(String(500), nullable=False)

    # Relationships
    post = relationship("Post", back_populates="images")


class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    review_created_at = Column(DateTime, server_default=func.now())
    review_updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    post = relationship("Post", back_populates="reviews")
    buyer = relationship("User", back_populates="reviews", foreign_keys=[buyer_id])
