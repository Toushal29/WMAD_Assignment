import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft
import httpx
from pages.profile import profile_page


def main(page: ft.Page):
    page.title = "Saveur Moris"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    
    host = "http://127.0.0.1:8000/"
    
    # Track logged in user (simple variables, no session)
    current_user = None
    auth_token = None
    
    # Main home screen after login
    def show_home():
        page.controls.clear()
        page.appbar = None
        page.navigation_bar = None
        
        # AppBar
        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.FOOD_BANK),
            title=ft.Text(f"Saveur Moris - Hi, {current_user}"),
            bgcolor=ft.Colors.ORANGE_100,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem("My Profile", on_click=lambda e: show_profile()),
                        ft.PopupMenuItem("Logout", on_click=lambda e: logout()),
                    ]
                ),
            ],
        )
        
        # Home content
        home_content = ft.Column(
            [
                ft.Text("Welcome to Saveur Moris", size=25, weight="bold"),
                ft.Text("Experience the best Mauritian cuisine", italic=True),
                ft.Divider(height=20),
                ft.Text("Select an option from the menu below:", size=16),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
        
        page.add(home_content)
        page.update()
    
    def show_profile(e=None):
        nonlocal auth_token
        page.controls.clear()
        page.appbar = None
        page.navigation_bar = None
        
        # Use the token from login
        my_token = auth_token if auth_token else "no_token"
        
        # Create profile view
        profile_view = profile_page(page, my_token, host)
        
        def go_back(e):
            show_home()
        
        # Add back button
        content = ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back),
                ft.Text("Back", size=16),
            ], spacing=5),
            profile_view.controls[1],  # The container with profile content
        ])
        
        page.add(content)
        page.update()
    
    def logout():
        nonlocal current_user, auth_token
        current_user = None
        auth_token = None
        show_login()
    
    def show_login():
        nonlocal current_user, auth_token
        page.controls.clear()
        page.appbar = None
        page.navigation_bar = None
        
        # Login UI
        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)
        error_text = ft.Text("", color=ft.Colors.RED)
        loading_indicator = ft.ProgressRing(visible=False)
        
        def do_login(e):
            nonlocal current_user, auth_token
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
                        auth_token = token
                        current_user = username
                        show_home()
                    else:
                        error_text.value = "Login failed: No token received"
                else:
                    error_text.value = "Invalid username or password"
            except Exception as ex:
                loading_indicator.visible = False
                error_text.value = "Cannot connect to server. Make sure Django is running."
                print(f"Error: {ex}")
            
            page.update()
        
        def go_to_register(e):
            show_register()
        
        login_btn = ft.ElevatedButton("Login", on_click=do_login, width=300)
        register_link = ft.TextButton("Create an Account", on_click=go_to_register)
        
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Welcome Back!", size=30, weight="bold"),
                        ft.Divider(height=20),
                        username_field,
                        password_field,
                        loading_indicator,
                        error_text,
                        login_btn,
                        register_link,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                expand=True,
            )
        )
        page.update()
    
    def show_register():
        page.controls.clear()
        
        username_field = ft.TextField(label="Username", width=300)
        email_field = ft.TextField(label="Email", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)
        confirm_field = ft.TextField(label="Confirm Password", password=True, width=300)
        error_text = ft.Text("", color=ft.Colors.RED)
        loading_indicator = ft.ProgressRing(visible=False)
        
        def do_register(e):
            username = username_field.value
            email = email_field.value
            password = password_field.value
            confirm = confirm_field.value
            
            if not all([username, email, password, confirm]):
                error_text.value = "Please fill all fields"
                page.update()
                return
            elif password != confirm:
                error_text.value = "Passwords do not match"
                page.update()
                return
            
            # Show loading
            error_text.value = ""
            loading_indicator.visible = True
            page.update()
            
            try:
                # Call Django register API
                response = httpx.post(
                    f"{host}api/auth/register/",
                    json={
                        "username": username,
                        "password": password,
                        "email": email
                    },
                    timeout=10.0
                )
                
                loading_indicator.visible = False
                
                if response.status_code in [200, 201]:
                    show_login()
                else:
                    error_text.value = f"Registration failed: {response.status_code}"
            except Exception as ex:
                loading_indicator.visible = False
                error_text.value = "Cannot connect to server"
                print(f"Error: {ex}")
            
            page.update()
        
        def back_to_login(e):
            show_login()
        
        register_btn = ft.ElevatedButton("Register", on_click=do_register, width=300)
        login_link = ft.TextButton("Back to Login", on_click=back_to_login)
        
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Create Account", size=30, weight="bold"),
                        ft.Divider(height=20),
                        username_field,
                        email_field,
                        password_field,
                        confirm_field,
                        loading_indicator,
                        error_text,
                        register_btn,
                        login_link,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                expand=True,
            )
        )
        page.update()
    
    # Start with login screen (no session persistence)
    show_login()

ft.app(target=main)