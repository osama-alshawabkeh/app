from flet import *
from SingInmod import SignIn
from Loginmod import Login
from Dashboard import Dashboard

def App(page:Page):
    page.title="Form"
    page.window.height = 630
    page.window.width = 380
    page.theme_mode="DARK"
    page.window.center()
    def router(e):
        page.views.clear()
        print("Navigating to:", page.route)
        
        if page.route == "/" or page.route == "/Login":
            page.views.append(
                View(
                    "/Login",[
                        Login(page)
                        ]
                    )
                )
        elif page.route=="/SignIn":
            page.views.append(
                View(
                    "/SignIn",[
                        SignIn(page)
                        ]
                    )  
                )
        elif page.route == "/Dashboard":
            if page.session.get("user"):
                 page.views.append(
                 View(
                    "/Dashboard", [
                        Dashboard(page)
                        ]
                ))
            else:
                 print("User not logged in, redirecting to Login....")
                 page.go("/Login")

             
        else:
            # Redirect to login if route is not recognized
            page.go("/Login")
        
              
        page.update()
    def PopView():
        if len(page.views) > 1:
         page.views.pop()
         topView=page.views[-1]
         page.go(topView.route)
         
    if page.session.get("user"):
        page.go("/Dashboard")
    else:
        page.go("/Login")

    page.on_route_change=router
    page.on_view_pop=PopView


    
    page.go(page.route if page.route else "/Login")
    page.update()


if "__main__"==__name__:
    app(App,view=AppView.WEB_BROWSER)
