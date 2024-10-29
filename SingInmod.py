from flet import *
from reg import Valid
from Database import Database

class SignIn(UserControl):
    def __init__(self, page):
        self.page = page
        self.database = Database()  # Create an instance of Database
        super().__init__()

    def build(self):
        self.snk = SnackBar(Text("", color=colors.WHITE), bgcolor=colors.RED)
        self.snkV = SnackBar(Text("Account created successfully!", color=colors.WHITE70), bgcolor=colors.GREEN)

        def valid(e):
                try:
                    Res = Valid(self.user.value, self.email.value, self.password.value, self.phone.value)
                    
                    if not Res.validUser():
                        self.snk.content = Text("Invalid UserName", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                    elif not Res.validEmail():
                        self.snk.content = Text("Invalid Email", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                    elif not Res.validPassword():
                        self.snk.content = Text("Invalid Password", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                    elif not Res.validPhone():
                        self.snk.content = Text("Invalid Phone", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                    elif not self.rdGrp.value:
                        self.snk.content = Text("Invalid Checked", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                    elif not self.drop.value:
                        self.snk.content = Text("Invalid Selected", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                    elif self.database.user_exists(self.user.value, self.email.value):
                        self.snk.content = Text("Username or Email already exists", color=colors.WHITE)
                        self.snk.open = True
                        self.page.show_snack_bar(self.snk)
                    else:
                        # Save data to SQLite and JSON
                        self.database.add_user(self.user.value, self.email.value, self.password.value, self.phone.value)
                        self.page.session.set("user", self.user.value)
                        # Show success message
                        self.snkV.open = True
                        self.page.show_snack_bar(self.snkV)

                        # Redirect to Dashboard
                        self.page.go("/Dashboard")
                except Exception as ex:
                    print(f"An error occurred: {ex}")
                    self.snk.content = Text("An error occurred during sign-up. Please try again.", color=colors.WHITE)
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

        self.email = TextField(
            label="Email", prefix_icon=icons.EMAIL, width=250, height=45,
            text_style=TextStyle(color=colors.WHITE), border_color=colors.WHITE,
            label_style=TextStyle(color=colors.WHITE),
            hint_text="Enter Email", hint_style=TextStyle(color=colors.WHITE, size=10)
        )

        self.password = TextField(
            label="Password", prefix_icon=icons.PASSWORD, border_color=colors.WHITE, width=250, height=45, password=True,
            text_style=TextStyle(color=colors.WHITE), label_style=TextStyle(color=colors.WHITE),
            hint_text="Enter Password", hint_style=TextStyle(color=colors.WHITE, size=10), can_reveal_password=True
        )

        self.phone = TextField(
            label="Phone Number", prefix_icon=icons.PHONE, border_color=colors.WHITE, width=250, height=45,
            text_style=TextStyle(color=colors.WHITE),
            label_style=TextStyle(color=colors.WHITE),
            hint_style=TextStyle(color=colors.WHITE, size=10), hint_text="Enter Phone Number"
        )

        self.drop = Dropdown(
            hint_text="Choose Languages",
            width=200,
            height=50,
            hint_style=TextStyle(color=colors.WHITE),
            options=[
                dropdown.Option("Arabic"),
                dropdown.Option("English"),
                dropdown.Option("French")
            ],
            focused_color=colors.WHITE, border_color=colors.WHITE
        )

        self.rdGrp = RadioGroup(content=Row([
            Radio(value="male", label="male", fill_color=colors.WHITE),
            Radio(value="female", label="female", fill_color=colors.WHITE)
        ]))

        c = Column(
            controls=[
                Container(
                    Text("Create Account", size=30, color=colors.RED_200),
                    alignment=alignment.center
                ),
                Container(self.user, alignment=alignment.center, margin=margin.only(0, 20)),
                Container(self.email, alignment=alignment.center, margin=margin.only(0, 20)),
                Container(self.password, alignment=alignment.center, margin=margin.only(0, 20)),
                Container(self.phone, alignment=alignment.center, margin=margin.only(0, 20)),
                Row(
                    controls=[
                        Container(
                            self.rdGrp,
                            bgcolor=colors.BLACK12,
                            width=150,
                            height=50,
                            border_radius=10
                        )
                    ], alignment=MainAxisAlignment.SPACE_AROUND
                ),
                Container(self.drop, alignment=alignment.center, margin=margin.only(top=10)),
                Row(
                    controls=[
                        Container(ElevatedButton("Sign up", width=200, height=45, on_click=valid)),
                        Container(TextButton("Have an account?", on_click=lambda _: self.page.go("/Login"))),
                    ], alignment=MainAxisAlignment.SPACE_AROUND
                ),
            ]
        )
        return c

    def on_close(self):
        self.database.close()  # Close the database connection when done
