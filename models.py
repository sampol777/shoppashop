from datetime import datetime, date
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1606555549496-2619dfd8e502?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTN8fGZsb3dlciUyMGRyYXdpbmd8ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    role_name = db.Column(db.String(80), unique = True)
    users = db.relationship('User', backref = 'role')





class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    deleted = db.Column(db.Boolean, default = False)
    products = db.relationship('SellerProductInfo', backref = 'users')
    orders = db.relationship('Order' ,backref = 'buyer')
    
    @classmethod
    def signup(cls, role_id, username, email, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            role_id = role_id,
            username = username,
            email = email,
            password = hashed_pwd
            )
        print('moodels')
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        
        user = cls.query.filter_by(username = username).first()
        
        
        if user and user.deleted == False:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Product(db.Model):
    
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    name = db.Column(db.Text, unique = True)
    color = db.Column(db.String)
    image = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE)
    sellers_products = db.relationship('SellerProductInfo', backref = 'product')

    
    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            
        }  

class SellerProductInfo(db.Model):
    
    __tablename__ = "sellers_products_info"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    unit_price = db.Column(db.Float, nullable = False )
    stock = db.Column(db.Integer, nullable = False)
    deleted = db.Column(db.Boolean, default = False)

    product_orders_details= db.relationship('ProductOrderDetails', backref = 'seller_product')

class ProductOrderDetails(db.Model):
    __tablename__ = 'product_orders_info'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    seller_product_info_id =db.Column( db.Integer, db.ForeignKey('sellers_products_info.id'))
    order_id = db.Column( db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column( db.Integer, nullable = False)
    total = db.Column(db.Float, nullable = False)
    
    @classmethod
    def calcTotal(cls, seller_product_info_id, quantity):
        info= SellerProductInfo.query.filter_by( seller_product_info_id).first()

        return info.untit_price * quantity


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subtotal = db.Column(db.Float)
    order_date = db.Column(db.DateTime, nullable = False, default= date.today())
    status = db.Column(db.String)
    products = db.relationship('ProductOrderDetails', backref = 'order' )
    

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)









    





