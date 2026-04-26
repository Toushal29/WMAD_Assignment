import flet as ft
# Import your function from the api folder
from api_functions import *

import flet_map as ftm #Imports for the map feature

async def main(page: ft.Page):
    page.window.always_on_top = True
    page.title = "API Calls Profile - main2.py"
    page.window.width = 400
    page.window.height = 700
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    
    
    # Configuration
    my_token = "55242da82c27f93d95e939bdda2b49076f0672c2"
    # my_token = "048c128a5ff6d5415239fa69f33dad9763e942da"
    host = "http://127.0.0.1:8000/"
    
    result_text = ft.Text()

    home_layout = ft.Column([
                    ft.Text("Welcome to Saveur Moris", size=25, weight="bold"),
                    ft.Text("Experience the best Mauritian cuisine", italic=True),
                    ft.Image(src="https://flet.dev/img/pages/quick-start/flet-app-icons.png", width=200), # Example placeholder
                    ft.Text("Select an option from the menu to get started."),
                    ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    # Normal view
    main_content = ft.Container(
        content=home_layout,
        expand=True,
    )

    # Function to return home
    def go_home(e):
        main_content.content = home_layout
        page.update()
    
    # Reset the view to remove what orderId added
    def reset_view():
        main_content.content = ft.Column([result_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    # Use page.run_task to call the imported async function
    def on_profile_click(e):
        reset_view()
        container = ft.Column(spacing=10)
        main_content.content = ft.Column(
            controls=[
                ft.Text("User Profile", size=20, weight="bold"),
                container,
                ft.Row(
                    controls=[
                        ft.Button("Update", bgcolor=ft.Colors.BLUE_300, on_click=update_profile_click),
                        ft.Button("Delete", bgcolor=ft.Colors.RED_300, on_click=delete_profile_click),
                    ],
                    alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()
        page.run_task(get_my_profile_api, page, container, my_token, host)

    # update profile
    def update_profile_click(e):
        # We find the container within our main_content: main_content.content.controls[1] is the 'container' Column
        profile_container = main_content.content.controls[1]
        page.run_task(update_profile_api, page, profile_container, my_token, host)

    # delete profile
    def delete_profile_click(e):
        # 1. Create a "Danger Zone" confirmation view
        confirmation_view = ft.Column(
            controls=[
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="red", size=50),
                ft.Text("Confirm Account Deletion", size=20, weight="bold"),
                ft.Text("Are you absolutely sure? This cannot be undone.", text_align="center"),
                ft.Row([
                    ft.ElevatedButton(
                        "YES, DELETE", 
                        bgcolor=ft.Colors.RED_400, 
                        color="white",
                        on_click=lambda _: page.run_task(delete_profile_api, page, main_content, my_token, host)
                    ),
                    ft.TextButton(
                        "Cancel", 
                        on_click=on_profile_click # Go back to profile view
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        # 2. Swap the main container
        main_content.content = confirmation_view
        page.update()


    def on_review_click(e):
        reset_view()
        container = ft.Column(spacing=10)
        main_content.content = ft.Column(
            controls=[
                ft.Text("My reviews", size=20, weight="bold"),
                container
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()
        page.run_task(get_myreviews_api, page, container, my_token, host)


    def on_reservation_click(e):
        reset_view()
        container = ft.Column(spacing=10)
        main_content.content = ft.Column(
            controls=[
                ft.Text("My Reservation", size=20, weight="bold"),
                container
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()
        page.run_task(get_myreservations_api, page, container, my_token, host)


    def on_orders_click(e):
        reset_view()
        container = ft.Column(spacing=10)
        main_content.content = ft.Column(
            controls=[
                ft.Text("My Orders", size=20, weight="bold"),
                container
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()
        page.run_task(get_myorders_api, page, container, my_token, host)


    def myorder_byID_page(e):
        reset_view()
        id_input = ft.TextField(label="Order ID", width=300)
        container = ft.Column(spacing=10)
        new_view = ft.Column(
            controls=[
                ft.Text("Enter your Order ID below:", size=20, weight="bold"),
                id_input,
                ft.ElevatedButton("Search Order", on_click=lambda _: page.run_task(get_myorder_byID_api, page, container, my_token, host, id_input)),
                container,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        main_content.content = new_view
        page.update()


    #================ Codes for map (placeholder message) ==================
    
    def on_find_us_click(e):
        reset_view()

        map_view = ft.Column(
            controls=[
                ft.Text("Find Us", size=22, weight="bold"),

                #Map 
                


                
            ],
            expand=True
        )

        main_content.content = map_view
        page.update()
   

    #=======================================================================

    
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.FOOD_BANK),
        # leading_width=40,
        title=ft.Text("Saveur Moris"),
        center_title=False,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem("My Profile", on_click=on_profile_click),
                    ft.PopupMenuItem("My Reviews", on_click=on_review_click),
                    ft.PopupMenuItem("My Reservations", on_click=on_reservation_click),
                    ft.PopupMenuItem("My Orders", on_click=on_orders_click),
                    ft.PopupMenuItem("My Detail Orders", on_click=myorder_byID_page),
                    ft.PopupMenuItem("Find Us", on_click=on_find_us_click),
                ]
            ),
        ],
    )

    page.add(
        main_content,
        ft.Button("Home", bgcolor=ft.Colors.BLUE_ACCENT_700, color=ft.Colors.BLACK,on_click=go_home),
        )

ft.app(main)