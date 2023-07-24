# from flask import Flask, render_template, request, make_response, session, jsonify,json, redirect, url_for
from flask import *
import pymysql
from werkzeug.wrappers import response
from model import model
from datetime import datetime
from ViewClasses import *

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]

            # -----------------------------Admin-----------------------------
@app.route('/')
def home():
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    data = m.getChildCat(id)
    list = m.getData('ProductItem')
    subCat = []
    for e in data:
        id = m.getCatID(e)
        subCat.append(m.getChildCat(id))
    return render_template("home.html",List=data, List1=subCat, error="False", errormsg="")
    # return render_template("homePage.html",list=list,error="False", errormsg="")

@app.route('/getList',methods=["GET"])
def gettingList():
    m = model(app.config["DB_IP"], app.config["DB_USER"],app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    Listing=m.getChildCat(id)
    return jsonify(Listing)

@app.route("/showAll",methods=["GET"])
def gettingALLDATA():
    m = model(app.config["DB_IP"], app.config["DB_USER"],app.config["DB_PASSWORD"], app.config["DATABASE"])
    list = m.getData('ProductItem')
    return jsonify(list)

@app.route("/showItems")
def showItems():
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    data = m.getChildCat(id)
    subCat = []
    for e in data:
        id = m.getCatID(e)
        subCat.append(m.getChildCat(id))
    rows = m.getProducts()
        # return render_template('showItems.html', products=rows)
        
    return render_template("showItems.html",List=data, List1=subCat, products=rows, error="False", errormsg="")
    # return render_template("showItems.html",List=data, List1=subCat, products=rows, error="False", errormsg="")

@app.route('/category')
def category():
    if session.get("email") != None:
        m = model(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
        data = m.getCategories(True)
        return render_template("category.html", List = data, error="False", errormsg=None)
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route('/items')
def items():
    if session.get("email") != None:
        m = model(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
        data = m.getCategories(False)
        return render_template("items.html", List = data, error="False", errormsg=None)
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route('/order')
def order():
    if session.get("email") != None:
        return render_template("order.html", error="False", errormsg=None)
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route('/about')
def about():
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    data = m.getChildCat(id)
    subCat = []
    for e in data:
        id = m.getCatID(e)
        subCat.append(m.getChildCat(id))
    return render_template("about.html",List=data, List1=subCat, error="False", errormsg="")

@app.route('/admin')
def admin():
    return render_template("Admin.html", error="False", errormsg=None)
    
# Admin log in
@app.route('/login', methods=["POST"])
def login():
    email = request.form["email"]
    pwd = request.form["pwd"]
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    if not m.checkUserExist(email, "Admin"):
        return render_template("Admin.html", error="True", errormsg="User does not exist")
    else:
        if not m.validatePassword(email, pwd, "admin"):
            return render_template("Admin.html", error="True", errormsg="Invalid Password")
        else:
            session["email"] = email
            return render_template("adminHome.html", error="False", errormsg="")

# Admin log out
@app.route("/logOut")
def logOut():
    if session.get("email") != None:
        session.clear()
    return render_template("Admin.html", error="False", errormsg="")

@app.route('/adminHome')
def adminHome():
    if session.get("email") != None:
        return render_template("adminHome.html", error="False", errormsg=None)
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route("/addcategory", methods=["POST"])
def addcategory():
    if session.get("email") != None:
        catName = request.form["catname"]
        parent = request.form["parent"]
        m = model(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DATABASE"])
        parentID = m.getCatID(parent)
        c = ProductCategories(parentID, catName)
        data = m.getCategories(True)
        if (m.chkCatExist(catName)):
            return render_template("adminHome.html", error="True", errormsg="Category alredy exists")
        else:
            if (m.insertProductCategories(c)):
                return render_template("category.html", List=data, error="False", errormsg="")
            else:
                return render_template("category.html", List=data, error="True", errormsg="Category not inserted")
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route("/additem", methods=["GET", "POST"])
def additem():
    if session.get("email") != None:
        if request.method == "POST":
            name = request.form["name"]
            quantity = request.form["quantity"]
            price = request.form["price"]
            amount = request.form["amount"]
            image = "static/images/"+ request.form["filename"]
            desc = request.form["description"]
            catName = request.form["catname"]
            p = ProductItem(name, quantity, price, amount, image, desc)
            m = model(app.config["DB_IP"], app.config["DB_USER"],
                    app.config["DB_PASSWORD"], app.config["DATABASE"])
            data = m.getCategories(False)
            if (m.chkItemExist(name, amount)):
                return render_template("items.html", List=data, error="True", errormsg="Item already exist.")
            else:
                if (m.chkCatExist(catName)):
                    if (m.insertProductItem(p, catName)):
                        return render_template("items.html", List=data, error="False", errormsg=None)
                    else:
                        return render_template("items.html", List=data, error="True", errormsg="Error in inserting Item.")
                else:
                    return render_template("items.html", List=data,error="True",errormsg="Category not found!\nItem not inserted.")
        else:
            return render_template("adminHome.html",error="True",errormsg="Item not inserted.")
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route("/deleteitem", methods=["POST"])
def deleteitem():
    if session.get("email") != None:
        if request.method == "POST":
            ID = request.form["id"]
            m = model(app.config["DB_IP"], app.config["DB_USER"],
                    app.config["DB_PASSWORD"], app.config["DATABASE"])
            m.deleteItem(ID)
            data = m.getCategories(True)
            return render_template("category.html", List = data, error="False", errormsg="")
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route("/updateitem", methods=["POST"])
def updateitem():
    if session.get("email") != None:
        if request.method == "POST":
            ID = request.form["id"]
            quantity = request.form["quantity"]
            price = request.form["price"]
            amount = request.form["amount"]
            m = model(app.config["DB_IP"], app.config["DB_USER"],
                    app.config["DB_PASSWORD"], app.config["DATABASE"])
            m.updateItem(quantity, price, amount, ID)
            data = m.getCategories(False)
            return render_template("items.html", List = data,error="False",errormsg="")
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")

@app.route("/getCate" , methods=["GET"])
def getCate():
    m = model(app.config["DB_IP"], app.config["DB_USER"],app.config["DB_PASSWORD"], app.config["DATABASE"])
    catList=m.getData("ProductCategories")
    return jsonify(catList)

@app.route("/getItem" , methods=["GET"])
def getItem():
    m = model(app.config["DB_IP"], app.config["DB_USER"],app.config["DB_PASSWORD"], app.config["DATABASE"])
    itemList=m.getItems()
    return jsonify(itemList)

@app.route("/getOrder" , methods=["GET"])
def getOrders():
    m = model(app.config["DB_IP"], app.config["DB_USER"],app.config["DB_PASSWORD"], app.config["DATABASE"])
    orderList=m.getData("Orders")
    return jsonify(orderList)

@app.route("/updateOrder", methods=['POST', "GET"])
def updateOrder():
    if session.get("email") != None:
        if request.method == "POST":
            ID = request.form["id"]
            status= request.form['status']
            m = model(app.config["DB_IP"], app.config["DB_USER"],
                    app.config["DB_PASSWORD"], app.config["DATABASE"])
            m.updateOrderStatus(ID, status)
            return render_template("order.html", error="False", errormsg=None)
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")
 
@app.route("/deleteCat", methods=['POST', "GET"])
def  deleteCat():
    if session.get("email") != None:
        if request.method == "POST":
            ID = request.form["id"]
            m = model(app.config["DB_IP"], app.config["DB_USER"],
                    app.config["DB_PASSWORD"], app.config["DATABASE"])
            m.deleteCat(ID)
        data = m.getCategories(True)
        return render_template("category.html", List=data, error="False", errormsg="")
    else:
        return render_template("Admin.html", error="True", errormsg="Log in first")
            # -----------------------------Customer-----------------------------
# customer log in 
@app.route("/signupCus", methods = ["POST"])
def signupCus():    
    Name = request.form["username"]
    Email = request.form["email"]
    Password = request.form["password"]
    Address = request.form["Address"]
    City = request.form["City"]
    ZipCode = request.form["ZipCode"]
    Country = request.form["Country"]
    c = Customer(Name, Email, Password, Address, City, ZipCode,Country)
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    data = m.getChildCat(id)
    subCat = []
    for e in data:
        id = m.getCatID(e)
        subCat.append(m.getChildCat(id))
    if m.checkUserExist(Email, "Customer"):
        return render_template("home.html", List=data, List1=subCat, errormsg="Customer already exists")
    else:
        m.insertCustomer(c)
        session["EmailC"] = Email
        return render_template("home.html", List=data, List1=subCat, error="False", errormsg="")

@app.route('/loginCus', methods=["POST"])
def loginCus():
    Email = request.form["email"]
    Password = request.form["password"]
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    data = m.getChildCat(id)
    subCat = []
    for e in data:
        id = m.getCatID(e)
        subCat.append(m.getChildCat(id))
    if not m.checkUserExist(Email, "Customer"):
        return render_template("home.html", List=data, List1=subCat, error="True", errormsg="Customer does not exist")
    else:
        if not m.validatePassword(Email, Password, "Customer"):
            return render_template("home.html", List=data, List1=subCat, error="True", errormsg="Invalid Password")
        else:
            session["EmailC"] = Email
            return render_template("home.html", List=data, List1=subCat, error="False", errormsg="")

# Admin log out
@app.route("/logOutCust")
def logOutCust():
    if session.get("EmailC") != None:    
        session.clear()
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    data = m.getChildCat(id)
    subCat = []
    for e in data:
        id = m.getCatID(e)
        subCat.append(m.getChildCat(id))
    return render_template("home.html", List=data, List1=subCat, error="True", errormsg="Logged off")

@app.route("/home")
def CusHome():
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    id = m.getCatID("None")
    data = m.getChildCat(id)
    subCat = []
    for e in data:
        id = m.getCatID(e)
        subCat.append(m.getChildCat(id))
    return render_template("home.html", List = data, List1 = subCat, error = "False", errormsg="")

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    if session.get("EmailC") != None:
        m = model(app.config["DB_IP"], app.config["DB_USER"],
                    app.config["DB_PASSWORD"], app.config["DATABASE"])
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        # validate the received values
        if _quantity and _code and request.method == 'POST':
            row = m.getRow(_code) #aik data
            row['ItemID'] = str(row['ItemID'])
            itemArray = {
                row['ItemID']: {'Name': row['Name'], 'ItemID': row['ItemID'], 'Quantity': _quantity, 'Price': row['Price'],
                                'Picture': row['Picture'], 'Total_price': _quantity * row['Price']}}
            
            all_total_price = 0
            all_total_quantity = 0
            total_quantity = 0

            session.modified = True
            if 'cart_item' in session: 
                if str(row['ItemID']) in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if str(row['ItemID']) == key:
                            old_quantity = session['cart_item'][key]['Quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['Quantity'] = total_quantity
                            session['cart_item'][key]['Total_price'] = total_quantity * row['Price']
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)
                
                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['Quantity'])
                    individual_price = float(session['cart_item'][key]['Total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * row['Price']

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            return redirect(url_for('.products'))
        else:
            return 'No quantity provided'
    else:  
        return 'Login first'

@app.route('/products')
def products():
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])
    rows = m.getProducts()
    return render_template('showItems.html', products=rows)
    
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print("Excepton in line 92",e)


@app.route('/delete/<string:code>')
def delete_product(code):  
    m = model(app.config["DB_IP"], app.config["DB_USER"],
              app.config["DB_PASSWORD"], app.config["DATABASE"])   
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['Quantity'])
                        individual_price = float(session['cart_item'][key]['Total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        # return redirect('/')
        if (m.deleteItemFromCart(code)):
            return redirect(url_for('.showItems'))
        else:
            print("Error in delete item from cart")
    except Exception as e:
        print("Excepton in line 122",e)


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

@app.route('/placeOrder' , methods=['POST'])
def placeOrder():
    print("in funtion")
    newdate = datetime.now()
    newdate1 = newdate.strftime('%Y-%m-%d %H:%M:%S')
    if session.get("EmailC") != None:
        m = model(app.config["DB_IP"], app.config["DB_USER"],
                    app.config["DB_PASSWORD"], app.config["DATABASE"])
        custId = m.getCustId(session.get("EmailC"))
        print("custID: ",custId)
        print("Session Data in place Order \n:", type(session['cart_item']) ,session['cart_item'])
        for key, value in session['cart_item'].items():
            individual_quantity = int(session['cart_item'][key]['Quantity'])
            individual_id = float(session['cart_item'][key]['ItemID'])
            c = Cart(custId, individual_id, individual_quantity)
            m.addToCart(c)
            print("added to the cart")
            print("total price in app.py: ",session['all_total_price'])

        if(m.generateOrder(custId, session['all_total_price'],newdate)):
            print("generated")

        return redirect(url_for('.products'))

        # if (m.addToCart(c)):

        #     return redirect(url_for('.products'))
        # else:
        #     return 'Error while adding item to cart in db'

if __name__ == '__main__':
    app.run(debug = True)