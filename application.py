from logging import error
import re
import sqlite3, hashlib, os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask.helpers import url_for
from flask_session import Session
from tempfile import mkdtemp

from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        db = conn.cursor()
        if 'email' not in session:
            isLogged = False
            firstName = ''
            numOfItems = 0
        else:
            isLogged = True
            db.execute("SELECT user_id, firstName FROM users WHERE email = ?", (session['email'],))
            user_id, firstName = db.fetchone()
            db.execute("SELECT count(product_id) FROM cart WHERE user_id = ?", (user_id, ))
            numOfItems = db.fetchone()[0]

    conn.close()
    return (isLogged, firstName, numOfItems)

@app.route('/')
def index():
    isLogged, firstName, numOfItems= getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        db = conn.cursor()
        db.execute('SELECT product_id, productName, price, description, image, qty FROM PRODUCTS')
        productsDetails = db.fetchall()
        db.execute('SELECT categoryId, name FROM categories')
        categoryData = db.fetchall()
    productsDetails = parse(productsDetails)  
    return render_template('index.html', isLogged = isLogged, firstName=firstName, numOfItemsInCart=numOfItems, categoryData=categoryData, productsDetails=productsDetails)

@app.route("/logInForm")
def signIn():
    if 'email' in session:
        return redirect(url_for*('/'))
    else:
        return render_template("login.html", error='')


@app.route("/registerForm")
def registerForm():
    return render_template("register.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # get form data 
        email = request.form.get('email')
        password = request.form.get('password')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        address1 = request.form.get('addressLine1')
        address2 = request.form.get('addressLine2')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        postalCode = request.form.get('postalCode')
        phone = request.form.get('contact')

        with sqlite3.connect('database.db') as con:
            try:
                db = con.cursor()
                db.execute('INSERT INTO USERS (email,password,firstName,lastName,addressLine1,addressLine2,city,state,country,postalCode,contact) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (email, hashlib.md5(password.encode()).hexdigest(), firstName, lastName, address1, address2, city, state, country, phone, postalCode))

                con.commit()
                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        db.close()
        return render_template("login.html", error=msg)

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if is_valid(email, password):
            session['email'] = email
            return redirect('/')
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

# load categories
@app.route("/add")
def admin():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('addProduct.html', categories=categories)

# app product
@app.route("/addProducts", methods=["GET", "POST"])
def addProducts():
    if request.method == "POST":
        productName = request.form.get('productName')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        qty = int(request.form.get('qty'))
        categoryId = int(request.form.get('category'))

        #Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (productName, price, description, image, qty, categoryId) VALUES (?, ?, ?, ?, ?, ?)''', (productName, price, description, imagename, qty, categoryId))
                conn.commit()
                msg="Product added successfully"
            except:
                msg="Somthing went wrong"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect('/')

# rout delete page
@app.route("/remove")
def remove():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        productData = cur.fetchall()
    conn.close()
    return render_template('remove.html', productData=productData)

# remove products 
@app.route("/removeProduct")
def removeItem():
    product_id = request.args.get('product_id')
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM products WHERE product_iD = ?', (product_id, ))
            conn.commit()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    print(msg)
    return redirect('/')

# display category vice products
@app.route("/displayCategory")
def displayCategory():
        loggedIn, firstName, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId")
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT products.product_id, products.productName, products.price, products.image, categories.name FROM products, categories  WHERE products.categoryId = categories.categoryId AND categories.categoryId = ?", (categoryId, ))
            data = cur.fetchall()
        conn.close()
        categoryName = data[0][4]
        data = parse(data)
        return render_template('displayCategory.html', productsDetails=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)

# product descirption
@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    product_id = request.args.get('product_id')
    with sqlite3.connect('database.db') as conn:
        db = conn.cursor()
        db.execute('SELECT product_id, productName, price, description, image, qty FROM PRODUCTS WHERE product_id=?', (product_id, ))
        productData = db.fetchone()
    conn.close()
    return render_template("productDescription.html", productData=productData, loggedIn=loggedIn, firstName=firstName, noOfItems = noOfItems)

# add to cart
@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect('login.html')
    else:
        product_id = int(request.args.get('product_id'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id FROM users WHERE email = ?", (session['email'], ))
            user_id = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO cart (user_id, product_id) VALUES (?, ?)", (user_id, product_id))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect('/')

# cart routing
@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect('login.html')
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('select email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans