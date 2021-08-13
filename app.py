from logging import debug
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import time, timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'flask'
app.permanent_session_lifetime = timedelta(minutes=5)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/elsa45/CASE_WEB/galith.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)

# represent user object in database (database model)
class products(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    product_name = db.Column("name", db.String(255))
    product_image = db.Column("img", db.String(255))
    product_price = db.Column("price", db.Integer)
    product_description = db.Column("desc", db.String(255))

  # primary key is created automatically
    def __init__(self,name, img, price, desc):
        self.name = name
        self.img = img
        self.price = price
        self.desc = desc

class Cart():
    def __init__(self, product, size, color, quantity):
        self.product = product
        self.size = size
        self.color = color
        self.quantity = quantity

@app.route("/cart")
def cart(edit=None):
    cart = []
    if 'cart' in session:
        cart = session['cart']
    return render_template("cart.html", data=cart, edit=edit)

@app.route("/products")
def product():
    return render_template("products.html", data=products.query.all())

@app.route("/details/<prod_id>")
def detail(prod_id):
    product = products.query.filter_by(_id=prod_id).first()
    return render_template("details.html", data=product)

@app.route("/")
def home(): 
    return render_template("home.html")

@app.route('/add-to-cart/<prod_id>', methods=['POST', 'GET'])
def addToCart(prod_id):
    if request.method == 'POST':
        size = request.form['size']
        color = request.form['color']
        product = products.query.filter_by(_id=prod_id).first()

        cart = []
        if 'cart' in session:
            cart = session['cart']

        for c in cart:
            if c.product == product:
                c.product.qty += 1
                break
            else:
                cart.append(Cart(product, size, color, 1))
                break

        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/delete-from-cart/<idx>')
def deleteFromCart(idx):
    pass

@app.route('/update-cart/<idx>', methods=['POST', 'GET'])
def updateCart(idx):
    if request.method == 'POST':
        size = request.form['size']
        color = request.form['color']
        quantity = request.form['quantity']

        cart = session['cart']
        cart[idx].product.size = size
        cart[idx].product.color = color
        cart[idx].product.quantity = quantity
        
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/edit-cart/<idx>')
def editCart(idx):
    return redirect(url_for('cart'), edit=idx)

@app.route('/checkout')
def deleteAllFromCart():
    pass

if __name__ == "__main__":
    db.create_all() # create all tables
    app.run(debug=True)
    # session.pop('cart', None)
