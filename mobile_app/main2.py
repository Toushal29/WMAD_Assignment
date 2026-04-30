import flet as ft
from auth.login import login_page
from auth.register import register_page
from pages.home import home_page

def main(page: ft.Page):
    page.title = "Saveur Moris"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 400
    page.window_height = 700
    
    # Create in-memory user store
    if not hasattr(page, "users"):
        page.users = {"demo": "password123"}
    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/login":
            page.views.append(login_page(page))
        elif page.route == "/register":
            page.views.append(register_page(page))
        elif page.route == "/home":
            page.views.append(home_page(page))
        else:
            page.views.append(login_page(page))
        
        page.update()
    
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.push_route(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Start with login page
    page.push_route("/login")

ft.app(target=main)