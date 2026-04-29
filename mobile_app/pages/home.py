import flet as ft

def home_page(page: ft.Page):
    username = page.session.get("username", "User")
    
    def logout_click(e):
        page.session.set("logged_in", False)
        page.session.remove("username")
        page.go("/login")
    
    return ft.View(
        "/home",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Welcome, {username}!", color=ft.colors.WHITE),
                bgcolor=ft.colors.ORANGE,
                actions=[
                    ft.IconButton(ft.icons.LOGOUT, on_click=logout_click, icon_color=ft.colors.WHITE),
                ],
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.RESTAURANT_MENU, size=80, color=ft.colors.ORANGE),
                        ft.Text("Saveur Moris", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text("Discover the best Mauritian cuisine!", size=16, color=ft.colors.GREY_600),
                        ft.Divider(height=30),
                        ft.ElevatedButton(
                            "View Menu",
                            on_click=lambda e: print("Navigate to menu"),
                            width=200,
                            bgcolor=ft.colors.ORANGE,
                            color=ft.colors.WHITE,
                        ),
                        ft.ElevatedButton(
                            "Make a Reservation",
                            on_click=lambda e: print("Navigate to reservation"),
                            width=200,
                            bgcolor=ft.colors.ORANGE_100,
                            color=ft.colors.ORANGE_900,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
    )