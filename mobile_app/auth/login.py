import flet as ft
import httpx

def login_page(page: ft.Page, on_login_success=None):
    host = "http://127.0.0.1:8000/"
    
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
    loading_indicator = ft.ProgressRing(visible=False)
    
    def login_click(e):
        username = username_field.value
        password = password_field.value
        
        if not username or not password:
            error_text.value = "Please enter username and password"
            page.update()
            return
        
        # Show loading
        error_text.value = ""
        loading_indicator.visible = True
        page.update()
        
        try:
            # Call Django login API
            response = httpx.post(
                f"{host}api/auth/login/",
                json={
                    "username": username,
                    "password": password
                },
                timeout=10.0
            )
            
            loading_indicator.visible = False
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                
                if token:
                    # Store token in session
                    page.session.set("token", token)
                    page.session.set("username", username)
                    page.session.set("logged_in", True)
                    
                    # Call success callback if provided, otherwise navigate directly
                    if on_login_success:
                        on_login_success(username)
                    else:
                        page.go("/home")
                else:
                    error_text.value = "Login failed: No token received"
            else:
                error_text.value = "Invalid username or password"
        except Exception as ex:
            loading_indicator.visible = False
            error_text.value = f"Cannot connect to server. Make sure Django is running."
            print(f"Error: {ex}")
        
        page.update()
    
    def go_to_register(e):
        page.go("/register")
    
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
        on_click=go_to_register,
        style=ft.ButtonStyle(color=ft.Colors.ORANGE),
    )
    
    # Create the main content column
    content_column = ft.Column(
        [
            ft.Text("Welcome Back!", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
            ft.Text("Login to your account", size=16, color=ft.Colors.GREY_600),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            username_field,
            password_field,
            loading_indicator,
            error_text,
            login_btn,
            register_link,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )
    
    # Create container with the column
    container = ft.Container(
        content=content_column,
        expand=True,
    )
    
    # Return the view
    return ft.View(
        "/login",
        container,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )