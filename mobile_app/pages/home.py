import flet as ft

def home_page(page: ft.Page):
    username = page.session.get("username", "User")
    
    def logout_click(e):
        page.session.set("logged_in", False)
        page.session.remove("username")
        page.push_route("/login")  # Changed from go()
    
    return ft.View(
        "/home",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Welcome, {username}!", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.ORANGE,
                actions=[
                    ft.IconButton(ft.Icons.LOGOUT, on_click=logout_click, icon_color=ft.Colors.WHITE),
                ],
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.RESTAURANT_MENU, size=80, color=ft.Colors.ORANGE),
                        ft.Text("Saveur Moris", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text("Discover the best Mauritian cuisine!", size=16, color=ft.Colors.GREY_600),
                        ft.Divider(height=30),
                        ft.ElevatedButton(
                            "View Menu",
                            on_click=lambda e: print("Navigate to menu"),
                            width=200,
                            bgcolor=ft.Colors.ORANGE,
                            color=ft.Colors.WHITE,
                        ),
                        ft.ElevatedButton(
                            "Make a Reservation",
                            on_click=lambda e: print("Navigate to reservation"),
                            width=200,
                            bgcolor=ft.Colors.ORANGE_100,
                            color=ft.Colors.ORANGE_900,
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