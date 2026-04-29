import flet as ft

def login_page(page: ft.Page):
    username_field = ft.TextField(
        label="Username",
        width=300,
        border_color=ft.Colors.ORANGE_700,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.PERSON,
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.Colors.ORANGE_700,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.LOCK,
    )
    
    error_text = ft.Text("", color=ft.Colors.RED, size=14)
    
    def login_click(e):
        username = username_field.value
        password = password_field.value
        
        if not username or not password:
            error_text.value = "Please enter username and password"
        elif username in page.users and page.users[username] == password:
            page.session.set("logged_in", True)
            page.session.set("username", username)
            error_text.value = ""
            page.push_route("/home")  # Changed from go() to push_route()
        else:
            error_text.value = "Invalid username or password"
        
        page.update()
    
    login_btn = ft.ElevatedButton(
        "Login",
        on_click=login_click,
        width=300,
        bgcolor=ft.Colors.ORANGE,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    
    register_link = ft.TextButton(
        "Don't have an account? Register",
        on_click=lambda e: page.push_route("/register"),  # Changed from go()
        style=ft.ButtonStyle(color=ft.Colors.ORANGE),
    )
    
    return ft.View(
        "/login",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Welcome Back!", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                        ft.Text("Login to your account", size=16, color=ft.Colors.GREY_600),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        username_field,
                        password_field,
                        error_text,
                        login_btn,
                        register_link,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )