import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft

def main(page: ft.Page):
    page.title = "Saveur Moris"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Create in-memory user store (simple dict)
    users = {"demo": "password123"}
    
    # Track logged in user
    current_user = None
    
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
    
    def logout():
        nonlocal current_user
        current_user = None
        show_login()
    
    def show_login():
        nonlocal current_user
        page.controls.clear()
        page.appbar = None
        page.navigation_bar = None
        
        # Login UI
        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)
        error_text = ft.Text("", color=ft.Colors.RED)
        
        def do_login(e):
            nonlocal current_user
            username = username_field.value
            password = password_field.value
            
            if username in users and users[username] == password:
                current_user = username
                show_home()
            else:
                error_text.value = "Invalid username or password"
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
        
        def do_register(e):
            username = username_field.value
            email = email_field.value
            password = password_field.value
            confirm = confirm_field.value
            
            if not all([username, email, password, confirm]):
                error_text.value = "Please fill all fields"
            elif password != confirm:
                error_text.value = "Passwords do not match"
            elif username in users:
                error_text.value = "Username already exists"
            else:
                users[username] = password
                show_login()
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
    
    # Start with login screen
    show_login()

ft.app(target=main)