import re

class Valid:
    def __init__(self,user,email=None,password=None,phone=None):
        self.user=user
        self.email=email
        self.password=password
        self.phone=phone

    validUser=lambda self:True if self.user!="" and re.search(r"^[A-Za-z0-9]{5,15}$",self.user) else False
    validEmail=lambda self:True if self.email!="" and re.search(r"^[A-Za-z0-9]+@(gmail|email|hotmail|outlouk).com$",self.email) else False
    validPassword=lambda self:True if self.password!="" and re.search(r"^(?=.*\d)(?=.*\W)(?=.*\w).{8,18}$",self.password) else False
    validPhone=lambda self:True if self.phone!="" and re.search(r"^(\+2126|\+2127|06|07)+[0-9]{8}$",self.phone) else False
    


