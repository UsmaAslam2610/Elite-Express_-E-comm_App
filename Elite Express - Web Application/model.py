from logging import shutdown

from pymysql import Date
from ViewClasses import *
import pymysql
import random

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
cursor = None
class model:
    # constructor
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        except Exception as e:
            print("There is error in connection", str(e))

    # Destructor
    def __del__(self):

        if self.connection != None:
            self.connection.close()

    # for log in
    # agar admin chk krna tw tableName my Admin pass krna ha aur agar customer ka chk krna tw Customer
    def checkUserExist(self, email, tableName):
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                cursor.execute(f"select Email from {tableName};")
                emailList = cursor.fetchall()
                for e in emailList:
                    if email == e[0]:
                        return True
                return False
        except Exception as e:
            print("Exception in checkUserExist", str(e))
        finally:
            if cursor != None:
                cursor.close()

    # for signUp
    def insertAdmin(self, user):  # agar admin
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                query = "insert into Admin (Email,Name,Password) values (%s,%s,%s)"
                args = (user.email, user.name, user.password)
                cursor.execute(query, args)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertAdmin", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def insertCustomer(self, user):  # agar customer aye tw Customer
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                query = f"insert into Customer (Name, Email, Password, Address, City, ZipCode, Country) values ('{user.Name}','{user.Email}','{user.Password}','{user.Address}','{user.City}', {user.ZipCode}, '{user.Country}')"
                cursor.execute(query)
                self.connection.commit()
                print("mail: ", user.Email)
                self.SignUpMail(user.Email,user.Name)
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertCustomer", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    # validate Password on log in
    def validatePassword(self, email_, password_, tableName):
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                cursor.execute(f"select Password from {tableName} where Email = '{email_}';")
                password = cursor.fetchall()
                if password_ == password[0][0]:
                    return True
                return False
        except Exception as e:
            print("Exception in validatePassword", str(e))
        finally:
            if cursor != None:
                cursor.close()

    # -----------------------------Admin------------------------------
    # add item into inventory
    # insert into ProductItemCategories
    def insertProductItemCategories(self, Name, catName):  # pass category
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                query = f'''insert into ProductItemCategories (ProductID, CategoryID) values 
                ((select ItemID from `ProductItem` where Name like '{Name}'), 
                (select ID from `ProductCategories` where CategoriesName like '{catName}'));'''
                cursor.execute(query)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertProductItemCategories", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    # insert ProductCategories
    def insertProductCategories(self, category):  # pass category
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                query = f"insert into ProductCategories(CategoriesName, Parent) values('{category.CategoriesName}', {category.Parent});"
                cursor.execute(query)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertProductCategories", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    # insert ProductItem
    def insertProductItem(self, pItem, catName):  # pass category
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                query = "insert into ProductItem (Name, Quantity, Price, Amount, Picture, Description) values (%s, %s, %s, %s, %s, %s);"
                args = (pItem.Name, pItem.Quantity, pItem.Price, pItem.Amount,
                        pItem.Picture, pItem.Description)
                cursor.execute(query, args)
                self.connection.commit()
                num = catName
                n = self.insertProductItemCategories(pItem.Name, num)
                return True
            else:
                return False
        except Exception as e:
            print("Exception in insertProductItem", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def updateItem(self, quantity, price, amount, ID):
        try:
            if self.connection != None:
                global cursor
                cursor = self.connection.cursor()
                query = f'''update ProductItem set Quantity = {quantity}, Price = {price}, Amount = '{amount}' where  ItemID = {ID};'''
                cursor.execute(query)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in updateItem", str(e))
            return False
        finally:
            if cursor:
                cursor.close()

    # delete category from inventory
    def deleteCat(self, ID):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = f"delete from ProductCategories where ID = {ID} OR Parent = {ID};"
                cursor.execute(query)
                self.connection.commit()
                query = f"delete from ProductItem where ItemID = {ID};"
                cursor.execute(query)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in deleteCat", str(e))
            return False
        finally:
            if cursor:
                cursor.close()

    # delete item into inventory
    def deleteItem(self, id):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = f"delete from ProductItem where ItemID = {id}"
                cursor.execute(query)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in deleteItem", str(e))
            return False
        finally:
            if cursor:
                cursor.close()

    # option to Admin -> dropdown milly ga
    def updateOrderStatus(self, id, status):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()  
                query = f"update `Orders` set Status = '{status}' where Order_ID = {id};"
                cursor.execute(query)
                self.connection.commit()               
                if status == "Dispatch":
                    query = f"select CusID,Email from Customer where CusID = (select CustID from Orders where Order_ID = {id});"
                    cursor.execute()
                    data = cursor.fetchall()
                    self.message(data[0][1],"status",data[0][0],id)
                return True
            else:
                return False
        except Exception as e:
            print("Exception in update Order Status", str(e))
            return False
        finally:
            if cursor:
                cursor.close()
    
    # ----------------------------Customer---------------------------------------
    # Add -> itemID, amount  #quantity <= available quantity
    def addToCart(self, cart):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = f"insert into Cart(CustID, ItemID, Quantity) VALUES ({cart.CustID}, {cart.ItemID}, {cart.Quantity});"
                cursor.execute(query)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in deleteItem", str(e))
            return False
        finally:
            if cursor:
                cursor.close()

    # Delete from the cart
    def deleteItemFromCart(self, ID):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = f"delete from cart where ItemID = {ID};"
                cursor.execute(query)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in deleteItemFromCart", str(e))
            return False
        finally:
            if cursor:
                cursor.close()
    # update quantity of an item in cart
    # line 196

    # -----------------------------Generate order---------------------------------
    def decreaseQuantity(self, newQuan, itemID):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = f"select Quantity from ProductItem where ItemID = {itemID};"
                cursor.execute(query)
                quantity = cursor.fetchall()
                newQuan = quantity[0][0] - newQuan
                # model.updateItemQuantity(newQuan, itemID, "ProductItem")
                cursor.execute(f"update `ProductItem` set Quantity = '{newQuan}' where ItemID = {itemID};")
                return True
            else:
                return False
        except Exception as e:
            print("Exception in updateItem", str(e))
            return False
        finally:
            if cursor:
                cursor.close()

    def generateOrder(self, custID,totalPrice,date):  # CustID jo user login howa wahan sy a jaye ga
        try:
            if self.connection != None:
                print("generate order i funt")
                cursor = self.connection.cursor()
                query = f"select ItemID, Quantity from Cart where CustID = {custID}"
                cursor.execute(query)
                data = cursor.fetchall()  # [(1,15),(2,15)]
                print(type(data) ,"", data)
                list = []
                for i in data:
                    query = f"select Price from ProductItem where ItemID = {i[0]};"
                    cursor.execute(query)
                    price = cursor.fetchall()
                    print("price:", type(price), price[0][0])
                    # totalPrice += price[i][0] * i[1]
                    # print("t p : ", totalPrice)
                    dic = {"ItemID": i[0], "Quantity": i[1], "Price": price[0][0]}
                    list.append(dic)
                    print("itemID: ", i[0] , type( i[0] ))
                    print("uantity: ",i[1], type( i[1] ))
                    self.decreaseQuantity(i[1], i[0])
                trakingID = str(custID) + str(data.__len__()) + \
                    str(random.randrange(1000, 9999, 1))
                 
                # date = date[0]
             

                
                # print("date: ", date, type(date[0]))
                print("newdate: ", date, type(date))
                print(date, " ", trakingID, " ",custID, " ", totalPrice)
                query = "INSERT INTO `Orders` (OrderTime, TrackingID, CustID, TotalPrice, Status) VALUES (%s, %s, %s, %s,%s);"
                args = (date,trakingID, custID, totalPrice, 'In Process')
                cursor.execute(query, args)
                print("query date executed")
                cursor.execute(f"select * from `Orders`")
                list = cursor.fetchall()
                print("data from db: ", list)
                query = f"select max(Order_ID) from `Orders` where custID = {custID};"
                cursor.execute(query)
                oID = cursor.fetchall()

                print("query order executed", oID)
                print("list:", list, "type: " , type(list))
                for i in list:
                    print(i)
                    id = int(i[0])
                    qty = int(i[3])
                    prc = int(i[4])

                    query = f"INSERT INTO OrderDetails (OrderID, ItemsID, Quantity, ItemPrice) VALUES ({oID[0][0]}, {id}, {qty}, {prc});"
                    print(id, qty, prc)
                    cursor.execute(query)
                    print("order inserted")
                    list= []
                    cursor.execute(f"select * from `OrderDetails`")
                    list = cursor.fetchall()
                    print("data from db: ", list)
                # query = f"select Email from Customer where CusID = {custID};"
                # cursor.execute(query)
                # email = cursor.fetchone()
                # print("sending mail:")
                # self.message(email,"placed",custID,oID)
                # query = f"delete from cart where custID = {custID};"
                # cursor.execute(query)
                # print("deleted from the cart")
                return True
            else:
                return False
        except Exception as e:
            print("Exception in generateOrder", str(e))
            return False
        finally:
            if cursor:
                cursor.close()

    # show krwany waly sth sth bnayen gy


# select ItemID, Quantity from Cart where CustID = 1
# -- then usy aik list of dictionary my rkh lo
# INSERT INTO `Orders` (OrderTime, TrackingID, CustID, TotalPrice) VALUES ((SELECT SYSDATE()), '1234EW2', 1, 100);
# INSERT INTO OrderDetails (OrderID, ItemsID, Quantity, ItemPrice) VALUES (1, 1, 15, 100);
# -- un un ko cart my del kr do jo order my place ho gaen hain
# delete from cart where custID = 1;

#check category exists

    def chkCatExist(self, catName):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select CategoriesName from ProductCategories")
                l = cursor.fetchall()
                for i in l:
                    if catName == i[0]:
                        return True
                return False
        except Exception as e:
            print("Exception in check Category Exists", str(e))
        finally:
            if cursor != None:
                cursor.close()

    #check item exists in this category
    def chkItemExist(self, iName, iAmount):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select Name, Amount from ProductItem")
                l = cursor.fetchall()
                for i in l:
                    if iName == i[0] and iAmount == i[1]:
                        return True
                return False
        except Exception as e:
            print("Exception in check item Exists", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getData(self, tableName):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(f"select * from {tableName};")
                data = cursor.fetchall()
                return data
        except Exception as e:
            print("Exception in getCategory: ", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()

    def getItems(self):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select ItemID, Name, Quantity, Price, Amount, Description from ProductItem;")
                data = cursor.fetchall()
                return data
        except Exception as e:
            print("Exception in getItem: ", str(e))
            return False
        finally:
            if cursor != None:
                cursor.close()
    
    def getCategories(self, flag): #for categories flag True for items false
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute("select CategoriesName from ProductCategories;")
                l = cursor.fetchall()
                data = []
                if flag == True:
                    data.append('None')                
                for i in l:
                    data.append(i[0])
                return data
        except Exception as e:
            print("Exception in check Category Exists", str(e))
        finally:
            if cursor != None:
                cursor.close()
  
    def getCatID(self, name):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                if name == 'None':
                    return 0
                else:
                    cursor.execute(f"select ID from ProductCategories where CategoriesName = '{name}';")
                    l = cursor.fetchall()
                    return l[0][0]
        except Exception as e:
            print("Exception in getCatID", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getChildCat(self, parent): # parent ka naam aye ga not ID
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(f"select CategoriesName from ProductCategories where Parent = {parent};")
                l = cursor.fetchall()
                data = []
                for i in l:
                    data.append(i[0])
                return data
        except Exception as e:
            print("Exception in getChildCat", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getCatItems(self, id):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(f'''select i.ItemID, i.Name, i.Quantity, i.Price, i.Picture, i.Description 
                from productitem i , productitemcategories c where c.CategoryID = {id} and c.ProductID = i.ItemID;''')
                l = cursor.fetchall()
                return l
        except Exception as e:
            print("Exception in getCatItems", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def mail(self,email,text):
        senderMail = "elite.express243@gmail.com"
        message = MIMEMultipart("alternative")
        message.attach(text)
        message = message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(senderMail, "auba1422")
            server.sendmail(
                senderMail, email, message
            )

    def message(self,email, action, cusID, oID):
        # print("function called")
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                query = f"select `Name` from `Customer` where CusID = {cusID};"
                cursor.execute(query)
                name = cursor.fetchone()
                if action == "status":    
                    text = """
                        <html>
                        <body>
                            <p>Hi <b><i>{name[0]}</i></b>,<br><br>
                            Your Order has been dispatch. You will get your order in 30 minutes.
                            Hope you have a great experience.<br>
                            Happy Shopping :)
                            </p>
                        </body>
                        </html>
                            """
                    text = MIMEText(text.format(name = name),"html")
                elif action == "placed":
                    query = f"select * from Orders where Order_ID = {oID} and CustID = {cusID};"
                    cursor.execute(query)
                    data = cursor.fetchall()
                    text = """
                        <html>
                        <body>
                            <p>Hi <b><i>{name[0]}</i></b>,<br><br>
                            We have received your order<br>
                            Your Order details are as follow:<br>
                            Order No. {data[0][0]} <br>
                            Tracking No. {data[0][2]} <br>
                            Date and Time: {data[0][1]} <br>
                            Payment Method: Cash on Delivery <br>
                            Total Price: {data[0][4]} <br>
                            Hope you have a great experience.<br>
                            Happy Shopping :)
                            </p>
                        </body>
                        </html>
                            """
                    text = MIMEText(text.format(name = name, data = data),"html")
                self.mail(email,text)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Exception in message: ", str(e))
            return False
        finally:
            if cursor:
                cursor.close()

    def SignUpMail(self,email,Name):
        print(email)
        try:
            text = """\
                <html>
                <body>
                    <p>Hi <b>{name}</b>,<br><br>
                    Welcome to Elite Express website...!!<br>
                    Hope you have a great experience.<br>
                    Happy Shopping :)
                    </p>
                </body>
                </html>
                """
            text = MIMEText(text.format(name = Name),"html")
            self.mail(email,text)
            print("succeed")
            return True
        except Exception as e:
            print("Exception in signupmail: ", str(e))
            return False
                    
    def getRow(self, id):
        try:
            if self.connection != None:
                cursor = self.connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM ProductItem WHERE ItemID=%s;", id)
                row = cursor.fetchone()
                return row
        except Exception as e:
            print("Exception in getRow", str(e))
        finally:
            if cursor != None:
                cursor.close()
    
    def getProducts(self):
        try:
            if self.connection != None:
                cursor = self.connection.cursor(pymysql.cursor.DictCursor)
                cursor.execute("SELECT * FROM ProductItem;")
                row = cursor.fetchall()
                return row
        except Exception as e:
            print("Exception in getProducts", str(e))
        finally:
            if cursor != None:
                cursor.close()

    def getCustId(self, email):
        try:
            if self.connection != None:
                cursor = self.connection.cursor()
                cursor.execute(f"select CusID from customer where Email = '{email}';")
                row = cursor.fetchall()
                return row[0][0]
        except Exception as e:
            print("Exception in getProducts", str(e))
        finally:
            if cursor != None:
                cursor.close()