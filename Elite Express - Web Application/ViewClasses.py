# class Admin:
#     def __init__(self, Name, Email, Password):
#         self.Name = Name
#         self.Email = Email
#         self.Password = Password

class Customer:
    def __init__(self, Name, Email, Password, Address, City, ZipCode,Country):
        # self.CusID = CusID
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.Address = Address
        self.City = City
        self.ZipCode = ZipCode
        self.Country = Country

class ProductCategories:
    def __init__(self, Parent, CategoriesName):
        self.Parent = Parent
        self.CategoriesName = CategoriesName

class ProductItem:
    def __init__(self, Name, Quantity, Price, Amount, Picture, Description):
        # self.ItemID = ItemID
        self.Name = Name
        self.Quantity = Quantity
        self.Price = Price
        self.Amount = Amount
        self.Picture = Picture
        self.Description = Description

class ProductItemCategory:
    def __init__(self, productId, categoryID):
        self.productId = productId
        self.categoryID = categoryID
        
class Orders:
    def __init__( self, OrderTime, TrackingID, CusID, TotalPrice, Status):
        # self.OrderID = OrderID
        self.OrderTime = OrderTime
        self.TrackingID = TrackingID
        self.CusID = CusID
        self.TotalPrice = TotalPrice
        self.Status = Status

class OrderDetails:
    def __init__(self, OrderID, ItemsID, Quantity, Price):
        self.OrderID = OrderID
        self.ItemsID = ItemsID
        self.Quantity = Quantity
        self.Price = Price
        
class Cart:
    def __init__(self, CustID, ItemID, Quantity):
        self.CustID = CustID
        self.ItemID = ItemID
        self.Quantity = Quantity