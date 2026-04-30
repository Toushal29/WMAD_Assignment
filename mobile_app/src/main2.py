import flet as ft
# Import your function from the api folder
from api_functions import *

import flet_map as ftm        #Imports for the map feature
import flet_geolocator as ftg #Imports to get user location

async def main(page: ft.Page):
    page.window.always_on_top = True
    page.title = "API Calls Profile - main2.py"
    page.window.width = 400
    page.window.height = 700
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    
    
    
    # Configuration
    
    my_token = "a5842a6437612fed23a00407b72fcff384e776b7"
    host = "http://127.0.0.1:8000/"

    geo = ftg.Geolocator(
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.HIGH
        )
    ) 
    
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

    #======================== Reservation sections =========================

    def on_reservation_click(e):
        reset_view()

    

        #Fields for user input
        #Field for party size
        party_size = ft.TextField(
            label="Party Size",
            width=300,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        #field for allergy information
        allergy_info = ft.TextField(
            label="Allergy Information (optional)",
            width=300,
            multiline=True
        )

        # Simple date input (YYYY-MM-DD)
        date_input = ft.TextField(
            label="Reservation Date (YYYY-MM-DD)",
            width=300
        )

        # Simple time input (HH:MM)
        time_input = ft.TextField(
            label="Reservation Time (HH:MM)",
            width=300
        )


        #Radio buttons for seating choice
        seating = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="Indoor", label="Indoor"),
                ft.Radio(value="Outdoor", label="Outdoor"),
            ]),
            value="Indoor"
        )

        
        container = ft.Column(spacing=15)

        # creation apis
        def submit_reservation(e):

            if not date_input.value or not time_input.value:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Please select both date and time"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                return

            page.run_task(
                create_reservation_api,
                page,
                container,
                my_token,
                host,
                date_input.value,
                time_input.value,
                party_size,
                seating,
                allergy_info
            )
        
        main_content.content = ft.Column(
            controls=[
                ft.Text("Make a Reservation", size=22, weight="bold"),

                party_size,

                date_input,
                time_input,

                ft.Text("Seating Choice"),
                seating,

                allergy_info,

                ft.ElevatedButton(
                    "Create Reservation",
                    bgcolor=ft.Colors.GREEN,
                    on_click=submit_reservation
                ),

                container
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.update()

    #=======================================================================


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

        # Store user location
        state = {"user_marker": None}

        location_text = ft.Text("Click below to get your location")

        
        def build_map():
            markers = [
                # Restaurant marker
                ftm.Marker(
                    coordinates=ftm.MapLatitudeLongitude(
                        -20.160980262121928,
                        57.50049775736102
                    ),
                    content=ft.Icon(
                        ft.Icons.LOCATION_ON,
                        color=ft.Colors.RED,
                        size=40
                    ),
                )
            ]

            #Marker for user location 
            if state["user_marker"]:
                markers.append(
                    ftm.Marker(
                        coordinates=state["user_marker"],
                        content=ft.Icon(
                            ft.Icons.MY_LOCATION,
                            color=ft.Colors.BLUE,
                            size=40
                        ),
                    )
                )

            return ftm.Map(
                expand=True,
                initial_center=state["user_marker"]
                if state["user_marker"]
                else ftm.MapLatitudeLongitude(-20.1609, 57.5005),
                initial_zoom=14,
                layers=[
                    ftm.TileLayer(
                        url_template="https://tile.memomaps.de/tilegen/{z}/{x}/{y}.png",
                    ),
                    ftm.MarkerLayer(markers=markers),
                ],
            )

        
        map_container = ft.Container(expand=True)

        #Code for getting the location 
        async def get_location(e):
            try:
                print("Getting location...")

                await geo.request_permission()
                pos = await geo.get_current_position()

                
                if not pos:
                    print("GPS failed → using fallback")
                    pos = type("obj", (), {
                        "latitude": -20.1609,
                        "longitude": 57.5005
                    })

                print("FINAL POS:", pos.latitude, pos.longitude)

                state["user_marker"] = ftm.MapLatitudeLongitude(
                    pos.latitude,
                    pos.longitude
                )

                location_text.value = f"Your Location: {pos.latitude}, {pos.longitude}"

                map_container.content = build_map()
                map_container.update()

            except Exception as ex:
                print("ERROR:", ex)
                location_text.value = f"Error: {ex}"
                page.update()

        
        map_container.content = build_map()

        
        map_view = ft.Column(
            controls=[
                ft.Text("Find Us", size=22, weight="bold"),

                ft.ElevatedButton(
                    "Get My Location",
                    on_click=lambda e: page.run_task(get_location, e)
                ),

                location_text,

                map_container
            ],
            expand=True
        )

        main_content.content = map_view
        page.update()
   

    #=======================================================================

    
    def on_place_click(e):
    # 1. Clear previous views
      reset_view()
    
    # 2. Create the container where menu items will be injected
      cart_container = ft.Column(spacing=10)
    
    # 3. Set the UI layout for the Menu section
      main_content.content = ft.Column(
          controls=[ft.Row(controls=[
            ft.Text("Place Order", size=20, weight="bold"),
            ft.IconButton(
                icon=ft.Icons.SHOPPING_CART, 
                
                on_click=lambda _: page.run_task(get_cart_api,page, cart_container, my_token, host,on_place_click)
            ),],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
             ) 
            ,
            cart_container],
                
            scroll=ft.ScrollMode.ADAPTIVE ,
                                           )
                 
              
      page.update()
   
       
    
    # Run the asynchronous task to fetch and display the menu data
      page.run_task(get_place_api, page, cart_container, my_token, host)

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
    def on_nav_change(e):
       
        if e.control.selected_index == 0:
            print("Menu clicked")
        elif e.control.selected_index == 1:
            on_place_click(e)
           
        elif e.control.selected_index == 2:
            on_reservation_click(e)  

    pagelet = ft.Pagelet(

        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.RESTAURANT_MENU, label="Menu"),
                ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART_CHECKOUT, label="Order"),
                ft.NavigationBarDestination(icon=ft.Icons.TABLE_BAR, label="Reservation")],
                on_change=on_nav_change
                    
                ),
            
       
        content=ft.Container(),
        height=70,
    )

    page.add(
        pagelet,
        main_content,
        ft.Button("Home", bgcolor=ft.Colors.BLUE_ACCENT_700, color=ft.Colors.BLACK,on_click=go_home),
        )

ft.app(main)