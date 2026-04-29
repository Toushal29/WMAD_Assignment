import flet as ft
from auth.login import login_page
from auth.register import register_page
from pages.home import home_page

def main(page: ft.Page):
    page.title = "Saveur Moris"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Route handling
    def route_change(route):
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
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Start with login page
    page.go("/login")

ft.app(target=main)