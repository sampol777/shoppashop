# from itertools import product
# from re import search
# from types import MethodDescriptorType
from flask import Flask,jsonify, render_template, request, flash, redirect, session, url_for
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, UserEditForm, CheckPasswordForm, LoginForm, AddNewProduct, AddToCartForm, SearchProductForm, EditSellerProductForm
from models import ProductOrderDetails, db, connect_db, User , Order , Product , Role, SellerProductInfo
import os, sys, subprocess, platform

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import datetime
import pydf


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
mail = Mail(app)
s = URLSafeTimedSerializer('Thisissecret')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///shop_clone')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'hellosecret1')
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)


@app.before_request
def add_user_to_sess():
    if 'user_id' in session:
        print('hello')
    else:
        session['user_id'] = None

def do_login(user):
    session['user_id'] = user.id

def do_logout():

    if 'user_id' in session:
        del session['user_id']


@app.route('/clear')
def clear():
    session.clear()
    return redirect('/login')

##########################################################################
##### HOME

@app.route("/")
def root():
    

    user = User.query.filter_by(id = session['user_id']).first()
    if user != None:
        page = request.args.get('page', 1, type = int)
        searchform = SearchProductForm()
        form = AddToCartForm()
        products = SellerProductInfo.query.filter(SellerProductInfo.deleted == False).paginate(page=page,per_page = 6)
        
        print(user)
        
        return render_template('home.html', products= products, user = user, form = form, searchform = searchform)
    return redirect("/login")

#########################################################################
#####Autofil search        
@app.route("/products")
def searchproduct():
    list_products = [r.to_dict() for r in Product.query.all()]
    return jsonify(list_products) 

@app.route("/products", methods = ['POST'])
def showsearched():
    user = User.query.filter_by(id = session['user_id']).first()
    if user != None:
        page = request.args.get('page', 1, type = int)
        searchform = SearchProductForm()
        form = AddToCartForm()
        products = SellerProductInfo.query.join(Product).filter(SellerProductInfo.deleted == False, Product.name == searchform.product.data).paginate(page=page,per_page = 6)
        print(products)
        print(searchform.product.data)
    return render_template('home.html', products= products, user = user, form = form, searchform = searchform)



#####################################################################
# User signup/login/logout

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    """Handle user signup"""
    if 'user_id' in session:
        del session['user_id']
    form = UserAddForm()
    form.role.choices = [(role.id, role.role_name) for role in Role.query.all()]
    
    if form.validate_on_submit():
        
        try:
            user = User.signup(
                role_id = form.role.data,
                username = form.username.data,
                password = form.password.data,
                email = form.email.data
            )
            db.session.commit()
            
        except :
            flash("Username already taken!!", 'danger')
            return render_template('signup.html', form = form)
        
        session['user_id']= user.id
        
        return redirect("/")

    else:
        flash("Fill all inputs, please", 'danger')
        print(form.errors)
            
   

        return render_template('signup.html', form = form)

    

@app.route("/login" , methods=["GET", "POST"])
def logIn():
    
    if 'user_id' in session:
        del session['user_id']
    form = LoginForm()
    
    if form.validate_on_submit():
        
        user = User.authenticate(form.username.data,form.password.data)

        if user:
            session['user_id'] = user.id
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form= form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

#####################################################################
### ACCOUNT 

@app.route("/account",  methods=["GET", "POST"])
def accountShow():

    page = request.args.get('page', 1, type = int)
    form = UserEditForm()
    user = User.query.filter_by(id = session['user_id']).first()
    ##editing user
    if form.validate_on_submit():
        print('vvvvaaaaalidated')
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            return redirect("/account")
        print("Wrong password, please try again.", 'danger')

    ###account for seller
    if user.role.role_name == 'seller':
        
        orders = {}
        productorders=ProductOrderDetails.query.join(SellerProductInfo).filter(SellerProductInfo.seller_id == user.id).order_by(ProductOrderDetails.order_id.desc()).paginate(page=page,per_page = 10)
        
        i=0  ##counter for orders dict
        for order in productorders.items:
             total = order.seller_product.unit_price * order.quantity
             orders [i]={'order':order.order_id, 'product_name':order.seller_product.product.name,'product_color':order.seller_product.product.color, 'quantity': order.quantity,  'unit_price': order.seller_product.unit_price, 'total': total } 
             i+=1 
           
        return render_template( 'account.html' ,user = user,productorders=productorders, orders = orders, form = form)
    
    ##account for buyer
    if user.role.role_name == "buyer":
        
        orders = Order.query.filter( Order.buyer_id == user.id ).order_by(Order.id.desc()).paginate(page=page,per_page = 3)
        products=None
        
        
              
        return render_template( 'account.html', user = user, orders= orders, form = form)

##sellers products list   
@app.route('/account/product_list', methods=["GET", "POST"])
def showProdList():
    user = User.query.get_or_404(session['user_id'])
    if (user.role.role_name == "seller"):
        page = request.args.get('page', 1, type = int)
        form = EditSellerProductForm()
        

        if form.validate_on_submit():
            if User.authenticate(user.username, form.password.data):
                if form.validate_on_submit():
                    sellerproduct = SellerProductInfo.query.filter_by(id = form.sellerproduct_id.data).first() 
                    sellerproduct.unit_price = form.price.data,
                    sellerproduct.stock = form.stock.data
                    
                    db.session.commit()
                    return redirect("/account/product_list")   
            else:
                flash("Please check the password you've entered!")
                return redirect('/account/product_list')
        products = SellerProductInfo.query.filter(SellerProductInfo.seller_id == session['user_id'], SellerProductInfo.deleted == False ).order_by(SellerProductInfo.id).paginate(page=page,per_page = 6) 
        return render_template('sellerProdList.html', products= products, form = form)
    else:
                flash("Unauthorized!!")
                return redirect('/account')   



@app.route('/delete_user', methods=["POST"])
def delete_user():
    """Delete user."""

    
    user = User.query.filter_by(id = session['user_id']).first()
    user.deleted = True
    SellerProductInfo.query.filter(SellerProductInfo.seller_id == user.id).update({SellerProductInfo.deleted:True})
    
    db.session.commit()

    return redirect("/signup")


############################################################
#####PRODUCT


@app.route("/addproduct", methods = ["GET", "POST"])
def addProduct():
    
    form = AddNewProduct()
    form.name.choices = [(product.id, product.name) for product in Product.query.all()]
    if form.validate_on_submit():
       
        sellerproductinfo = SellerProductInfo(
            product_id = form.name.data,
            seller_id = session['user_id'],
            unit_price = form.price.data,
            stock = form.stock.data
        )

        db.session.add(sellerproductinfo)
        db.session.commit()
        
        return redirect("/account/product_list")
    else:
        print("didn't work")
        return render_template('addproduct.html',form = form)

@app.route("/deleteproduct/<int:product_id>", methods=["DELETE"])
def remove_product(product_id):
    
    
    product = SellerProductInfo.query.get_or_404(product_id)
    product.deleted = True
    
    db.session.commit()

    return jsonify(message="Deleted")

##########################################
###Cart

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



@app.route('/addtocart', methods = ['POST'])
def addCart():
    form = AddToCartForm()
    if form.validate_on_submit():
        try:
            
            product_id = form.sellerproduct_id.data
            quantity = form.quantity.data
            product =  SellerProductInfo.query.filter_by(id= product_id).first()

            DictItems = {product_id:{'name':product.product.name, 'color': product.product.color, 'price': product.unit_price, 'quantity': quantity, 'seller_name':product.users.username}}
            
            if 'Shoppingcart' in session:
                if product_id in session['Shoppingcart']:
                    session['Shoppingcart'][product_id]['quantity']= str(int(session['Shoppingcart'][product_id]['quantity']) + int(quantity))
                    session['TotalCartItems'] = str(int(session['TotalCartItems'])+int(quantity))
                    
                    session.modified = True
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    session['TotalCartItems'] = str(int(session['TotalCartItems'])+int(quantity))
                    
                    return redirect('/')
            else:
                session['Shoppingcart'] = DictItems
                session['TotalCartItems'] = quantity
                return redirect(request.referrer)

        except Exception as e:
            print(e)

        finally:
            return redirect(request.referrer)
    else:
        print("didn't work")

@app.route('/cart')
def showCart():
    

    if 'Shoppingcart' not in session :
        flash(u'Your cart is empty!', 'error')
        return redirect(request.referrer)

    
    totalorder = 0

    for key, product in session['Shoppingcart'].items():
        subtotal = float(product['price']) * int(product['quantity'])
        totalorder += float("%.2f" % subtotal)
    session['TotalOrder'] = totalorder
    return render_template('cart.html', totalorder= totalorder)

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect('/')
    
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        try:
            print ('try')
            session.modified = True
            for key , product in session['Shoppingcart'].items():
                if int(key)== code:
                    print(code)
                    difference =int(quantity) -int(product['quantity'])
                    print(difference)
                    product['quantity'] = str(quantity)
                    print(product['quantity'])
                    session['TotalCartItems'] = str(int(session['TotalCartItems'])+ difference)
                    print(session['TotalCartItems'])
                    return redirect(request.referrer)

        except Exception as e:
            print('no coooooode')
            print(e)
            return redirect(url_for('showCart'))

@app.route('/removefromcart/<int:code>', methods=['POST'])
def removeFromCart(code):
    
    
    if request.method == 'POST':
        try:
            for key , item in session['Shoppingcart'].items(): 
                if int(key)== code:
                    session.modified = True
                    quantity = item['quantity']
                    session['Shoppingcart'].pop(key,None)
                    session['TotalCartItems'] = str(int(session['TotalCartItems']) - int(quantity))
                    return redirect("/cart")
        except Exception as e:
            print('no coooooode')
            print(e)
            return redirect(url_for('showCart'))

#####################Methods to generate pdf email
@app.route('/sendTodaysOrders')
def sendTodaysOrders():
    
    products = ProductOrderDetails.query.join(Order).join(SellerProductInfo).filter(Order.order_date > datetime.datetime.today() - datetime.timedelta(days=1)).order_by(SellerProductInfo.seller_id.desc())
    
    users = [] 

    for product in products :
        
        if product.seller_product.seller_id not in users:
           users.append(product.seller_product.seller_id)
        
        
    for user in users:
        userproducts = ProductOrderDetails.query.join(Order).join(SellerProductInfo).filter(Order.order_date > datetime.datetime.today() - datetime.timedelta(days=1), SellerProductInfo.seller_id == user).order_by(Order.id.desc())
        seller = User.query.filter(User.id == user).first()
        
    
        rendered = render_template('pdf_template_seller.html',products = userproducts, seller = seller)
        pdf = pydf.generate_pdf(rendered)
        msg = Message('Your daily summary', sender = 'shoppyshopshop683@gmail.com', recipients = [seller.email])
        msg.attach("order.pdf", "application/pdf", pdf)
        mail.send(msg)
        print('sent')
        return redirect('/')
 


def sendEmailToBuyer(email, order,sessInfo):
    rendered = render_template('pdf_template_buyer.html', order = order,session = sessInfo)
    pdf = pydf.generate_pdf(rendered)
    msg = Message('Thank you for your order', sender = 'shoppyshopshop683@gmail.com', recipients = [email])
    msg.attach("order.pdf", "application/pdf", pdf)
    mail.send(msg)
    return print('mail sent')


@app.route('/placeorder')
def submitOrder():    
    
    order = Order(buyer_id = session['user_id'], subtotal = session['TotalOrder'])
    buyer = User.query.filter_by(id = session['user_id']).first()
    email = buyer.email
    db.session.add(order)
    db.session.commit()
    
    sendEmailToBuyer(email,order, session['Shoppingcart'])

    for key, product in session['Shoppingcart'].items():
        sellersproduct = SellerProductInfo.query.filter_by(id = key).first()
        
        subtotal = float(product['price']) * int(product['quantity'])
        productOrderDetails = ProductOrderDetails(seller_product_info_id = key, order_id = order.id, quantity = product['quantity'] , total = subtotal )
        sellersproduct.stock -=  int(product['quantity'])
        db.session.add(productOrderDetails)
        db.session.commit()
        
    del session['Shoppingcart']
    del session['TotalOrder']
    del session['TotalCartItems']

        
    
    return render_template('orderPlaced.html', username = buyer.username)


