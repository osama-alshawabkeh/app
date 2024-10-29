from flet import *
from reg import Valid
from Database import Database  # تأكد من استيراد فئة Database

class Login(UserControl):
    def __init__(self, page):
        self.page = page
        self.database = Database()  # إنشاء مثيل من قاعدة البيانات
        super().__init__()

    def build(self):
        # SnackBar messages
        self.snk = SnackBar(Text("", color=colors.WHITE), bgcolor=colors.RED)
        self.snkV = SnackBar(Text("Login successful", color=colors.WHITE70), bgcolor=colors.GREEN)

        # Validation function
        def valid(e):
            Res = Valid(self.user.value, "", self.password.value)
            if not Res.validUser():
                self.snk.content = Text("Invalid UserName", color=colors.WHITE)
                self.snk.open = True
                self.page.show_snack_bar(self.snk)
            elif not Res.validPassword():
                self.snk.content = Text("Invalid Password", color=colors.WHITE)
                self.snk.open = True
                self.page.show_snack_bar(self.snk)
            else:
                try:
                    # Validate user credentials from the database
                    if self.database.validate_user(self.user.value, self.password.value):
                        # Set session on successful login
                        self.page.session.set("user", self.user.value)
                        self.snkV.open = True
                        self.page.show_snack_bar(self.snkV)
                        # Clear the input fields after success
                        self.user.value = ""
                        self.password.value = ""
                        self.page.go("/Dashboard")  # Navigate to dashboard after successful login
                    else:
                        self.snk.content = Text("Invalid username or password", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                except Exception as ex:
                    # Handling possible database connection or query errors
                    self.snk.content = Text(f"Database error: {str(ex)}", color=colors.WHITE)
                    self.snk.open = True
                    self.page.show_snack_bar(self.snk)

        # User and Password input fields
        self.user = TextField(
            label="UserName", prefix_icon=icons.PERSON, width=250, height=45,
            text_style=TextStyle(color=colors.WHITE), border_color=colors.WHITE,
            label_style=TextStyle(color=colors.WHITE),
            hint_style=TextStyle(color=colors.WHITE, size=10),
            hint_text="Enter UserName"
        )

        self.password = TextField(
            label="Password", prefix_icon=icons.PASSWORD, width=250, height=45, password=True,
            text_style=TextStyle(color=colors.WHITE), label_style=TextStyle(color=colors.WHITE),
            border_color=colors.WHITE,
            hint_text="Enter Password", hint_style=TextStyle(color=colors.WHITE, size=10), can_reveal_password=True
        )

        # Login layout
        login = Column(
            controls=[
                Container(Text("Please Log In", size=45, color=colors.WHITE), alignment=alignment.center),
                Container(self.user, alignment=alignment.center, margin=margin.only(top=100)),
                Container(self.password, alignment=alignment.center, margin=margin.only(top=50)),
                Container(
                    Row(
                        controls=[
                            Container(
                                ElevatedButton("Log In", width=200, height=45, on_click=valid)
                            ),
                            Container(
                                TextButton("Create Account", on_click=lambda _: self.page.go("/SignIn"))
                            ),
                        ]
                    ),
                    margin=margin.only(top=50)
                )
            ]
        )
        return login

    def on_close(self):
        self.database.close()  # Close the database connection when done
