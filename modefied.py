def build(self):
        # Check if user is logged in via session
        user =self.page.session.get("user")
        if user:
            return Column(
                controls=[
                    Text(f"Welcome, {user}!"),
                    ElevatedButton("Log Out", on_click=self.logout)
                ]
            )
        else:
            # If no session, redirect to login
            print("User not logged in, redirecting to Login...")
            
            self.page.go("/SignIn")