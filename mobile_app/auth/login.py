import flet as ft

def login_page(page: ft.Page):
    # Create a simple in-memory user store (replace with database later)
    if not hasattr(page, "users"):
        page.users = {"demo": "password123"}  # username: password
    
    username_field = ft.TextField(
        label="Username",
        width=300,
        border_color=ft.colors.ORANGE_700,
        focused_border_color=ft.colors.ORANGE,
        prefix_icon=ft.icons.PERSON,
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.colors.ORANGE_700,
        focused_border_color=ft.colors.ORANGE,
        prefix_icon=ft.icons.LOCK,
    )
    
    error_text = ft.Text("", color=ft.colors.RED, size=14)
    
    def login_click(e):
        username = username_field.value
        password = password_field.value
        
        if not username or not password:
            error_text.value = "Please enter username and password"
        elif username in page.users and page.users[username] == password:
            page.session.set("logged_in", True)
            page.session.set("username", username)
            error_text.value = ""
            page.go("/home")
        else:
            error_text.value = "Invalid username or password"
        
        page.update()
    
    login_btn = ft.ElevatedButton(
        "Login",
        on_click=login_click,
        width=300,
        bgcolor=ft.colors.ORANGE,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    
    register_link = ft.TextButton(
        "Don't have an account? Register",
        on_click=lambda e: page.go("/register"),
        style=ft.ButtonStyle(color=ft.colors.ORANGE),
    )
    
    return ft.View(
        "/login",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Welcome Back!", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE),
                        ft.Text("Login to your account", size=16, color=ft.colors.GREY_600),
                        ft.Divider(height=30, color=ft.colors.TRANSPARENT),
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