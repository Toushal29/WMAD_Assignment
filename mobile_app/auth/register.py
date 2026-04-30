import flet as ft

def register_page(page: ft.Page, on_register_success=None):
    username_field = ft.TextField(
        label="Username",
        width=300,
        border_color=ft.Colors.ORANGE_700,
        prefix_icon=ft.Icons.PERSON,
    )
    
    email_field = ft.TextField(
        label="Email",
        width=300,
        border_color=ft.Colors.ORANGE_700,
        prefix_icon=ft.Icons.EMAIL,
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.Colors.ORANGE_700,
        prefix_icon=ft.Icons.LOCK,
    )
    
    confirm_field = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.Colors.ORANGE_700,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
    )
    
    error_text = ft.Text("", color=ft.Colors.RED, size=14)
    
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
            error_text.value = ""
            
            # Call success callback if provided
            if on_register_success:
                on_register_success(username)
            else:
                # Fallback: go to login page
                page.go("/login")
        
        page.update()
    
    register_btn = ft.ElevatedButton(
        "Register",
        on_click=register_click,
        width=300,
        bgcolor=ft.Colors.ORANGE,
        color=ft.Colors.WHITE,
    )
    
    login_link = ft.TextButton(
        "Already have an account? Login",
        on_click=lambda e: page.go("/login"),
        style=ft.ButtonStyle(color=ft.Colors.ORANGE),
    )
    
    # Create the main content column
    content_column = ft.Column(
        [
            ft.Text("Create Account", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
            ft.Text("Join Saveur Moris today", size=16, color=ft.Colors.GREY_600),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
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
    )
    
    # Create container with the column
    container = ft.Container(
        content=content_column,
        expand=True,
    )
    
    # Return the view
    return ft.View(
        "/register",
        container,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )