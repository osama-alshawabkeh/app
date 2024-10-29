from flet import *

class Dashboard(UserControl):
    def __init__(self, page):
        self.page = page
        super().__init__()

    def build(self):
        # Check if user is logged in via session
        user =self.page.session.get("user")
        
        return Column(
                controls=[
                    Text(f"Welcome, {user}!"),
                    ElevatedButton("Log Out", on_click=self.logout)
                ]
            )
       
            

    def logout(self, e):
        self.page.session.remove("user")
        self.page.go("/Login")