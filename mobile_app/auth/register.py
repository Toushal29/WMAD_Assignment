import flet as ft

def register_page(page: ft.Page):
    username_field = ft.TextField(
        label="Username",
        width=300,
        border_color=ft.colors.ORANGE_700,
        prefix_icon=ft.icons.PERSON,
    )
    
    email_field = ft.TextField(
        label="Email",
        width=300,
        border_color=ft.colors.ORANGE_700,
        prefix_icon=ft.icons.EMAIL,
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.colors.ORANGE_700,
        prefix_icon=ft.icons.LOCK,
    )
    
    confirm_field = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.colors.ORANGE_700,
        prefix_icon=ft.icons.LOCK_OUTLINE,
    )
    
    error_text = ft.Text("", color=ft.colors.RED, size=14)
    
    def register_click(e):
        username = username_field.value
        email = email_field.value
        password = password_field.value
        confirm = confirm_field.value
        
        if not all([username, email, password, confirm]):
            error_text.value = "Please fill all fields"
        elif password != confirm:
            error_text.value = "Passwords do not match"
        elif username in page.users:
            error_text.value = "Username already exists"
        else:
            # Save user
            page.users[username] = password
            page.session.set("registered", True)
            page.go("/login")
        
        page.update()
    
    register_btn = ft.ElevatedButton(
        "Register",
        on_click=register_click,
        width=300,
        bgcolor=ft.colors.ORANGE,
        color=ft.colors.WHITE,
    )
    
    login_link = ft.TextButton(
        "Already have an account? Login",
        on_click=lambda e: page.go("/login"),
        style=ft.ButtonStyle(color=ft.colors.ORANGE),
    )
    
    return ft.View(
        "/register",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Create Account", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE),
                        ft.Text("Join Saveur Moris today", size=16, color=ft.colors.GREY_600),
                        ft.Divider(height=30, color=ft.colors.TRANSPARENT),
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
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )