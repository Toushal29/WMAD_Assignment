import datetime

import flet as ft
# Import your function from the api folder
from api_functions import *
from permissions import build_permission_handler, request_location_permission

import flet_map as ftm        #Imports for the map feature
import flet_geolocator as ftg #Imports to get user location

async def main(page: ft.Page):
    auth_token = None

    page.window.always_on_top = True
    page.title = "Saveur Moris"
    page.window.width = 400
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    
        
    # Configuration
    host = "http://127.0.0.1:8000/"

    geo = ftg.Geolocator(
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.HIGH
        )
    ) 
    permission_handler = build_permission_handler()
    page.services = [geo, permission_handler]
    
    result_text = ft.Text()
    auth_screen = ft.Container(expand=True, padding=24)

    def set_auth_screen(content):
        auth_screen.content = content
        page.controls = [auth_screen]
        page.appbar = None
        page.update()

    def show_message(text, error_text, loading=None):
        if loading:
            loading.visible = False
        error_text.value = text
        page.update()

    def show_login():
        username_field = ft.TextField(
            label="Username",
            width=320,
            prefix_icon=ft.Icons.PERSON,
            border_color=ft.Colors.ORANGE_700,
            focused_border_color=ft.Colors.ORANGE,
        )
        password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=320,
            prefix_icon=ft.Icons.LOCK,
            border_color=ft.Colors.ORANGE_700,
            focused_border_color=ft.Colors.ORANGE,
        )
        error_text = ft.Text("", color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)
        loading = ft.ProgressRing(visible=False)

        def submit_login(e):
            nonlocal auth_token
            username = (username_field.value or "").strip()
            password = password_field.value or ""

            if not username or not password:
                show_message("Please enter username and password.", error_text)
                return

            error_text.value = ""
            loading.visible = True
            page.update()

            success, result = login_api(host, username, password)
            if success:
                auth_token = result
                show_app()
            else:
                show_message(result, error_text, loading)

        set_auth_screen(
            ft.Column(
                controls=[
                    ft.Icon(ft.Icons.RESTAURANT_MENU, size=72, color=ft.Colors.ORANGE),
                    ft.Text("Saveur Moris", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Login to continue", size=16, color=ft.Colors.GREY_700),
                    username_field,
                    password_field,
                    loading,
                    error_text,
                    ft.Button(
                        "Login",
                        icon=ft.Icons.LOGIN,
                        width=320,
                        bgcolor=ft.Colors.ORANGE,
                        color=ft.Colors.WHITE,
                        on_click=submit_login,
                    ),
                    ft.TextButton(
                        "Create an account",
                        style=ft.ButtonStyle(color=ft.Colors.ORANGE),
                        on_click=lambda e: show_register(),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=14,
            )
        )

    def show_register():
        username_field = ft.TextField(label="Username", width=320, prefix_icon=ft.Icons.PERSON)
        first_name_field = ft.TextField(label="First Name", width=320, prefix_icon=ft.Icons.BADGE)
        last_name_field = ft.TextField(label="Last Name", width=320, prefix_icon=ft.Icons.BADGE_OUTLINED)
        email_field = ft.TextField(label="Email", width=320, prefix_icon=ft.Icons.EMAIL)
        phone_field = ft.TextField(label="Phone Number", width=320, prefix_icon=ft.Icons.PHONE)
        address_field = ft.TextField(label="Address", width=320, prefix_icon=ft.Icons.HOME)
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=320, prefix_icon=ft.Icons.LOCK)
        confirm_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=320, prefix_icon=ft.Icons.LOCK_OUTLINE)
        error_text = ft.Text("", color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)
        loading = ft.ProgressRing(visible=False)

        def submit_register(e):
            nonlocal auth_token
            username = (username_field.value or "").strip()
            first_name = (first_name_field.value or "").strip()
            last_name = (last_name_field.value or "").strip()
            email = (email_field.value or "").strip()
            phone = (phone_field.value or "").strip()
            address = (address_field.value or "").strip()
            password = password_field.value or ""
            confirm = confirm_field.value or ""

            if not all([username, first_name, last_name, email, phone, address, password, confirm]):
                show_message("Please fill all fields.", error_text)
                return
            if password != confirm:
                show_message("Passwords do not match.", error_text)
                return

            error_text.value = ""
            loading.visible = True
            page.update()

            success, result = register_api(
                host, username, password, first_name, last_name, email, phone, address
            )
            if success:
                auth_token = result.get("token") if isinstance(result, dict) else None
                if auth_token:
                    show_app()
                else:
                    show_login()
            else:
                show_message(result, error_text, loading)

        set_auth_screen(
            ft.Column(
                controls=[
                    ft.Text("Create Account", size=28, weight=ft.FontWeight.BOLD),
                    username_field,
                    first_name_field,
                    last_name_field,
                    email_field,
                    phone_field,
                    address_field,
                    password_field,
                    confirm_field,
                    loading,
                    error_text,
                    ft.Button(
                        "Register",
                        icon=ft.Icons.PERSON_ADD,
                        width=320,
                        bgcolor=ft.Colors.ORANGE,
                        color=ft.Colors.WHITE,
                        on_click=submit_register,
                    ),
                    ft.TextButton(
                        "Back to login",
                        style=ft.ButtonStyle(color=ft.Colors.ORANGE),
                        on_click=lambda e: show_login(),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
            )
        )

    def on_logout_click(e):
        nonlocal auth_token
        success, result = logout_api(host, auth_token)
        if success:
            auth_token = None
            show_login()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(result), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    home_layout = ft.Column(
                controls=[
                        # todays special
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Today's Special", size=22, weight="bold",),
                                ft.Text("Chicken Biryani", weight="bold"),
                                ft.Image(src="biryani.jpg",width=250,height=180,fit="cover",border_radius=10),
                                ft.Text("Fragrant rice cooked with tender chicken."),
                                ft.Text("Available Daily", size=10),
                                ft.Text("Rs 250", color="green", weight="bold"),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ),
                        # popular dishes
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Popular Dishes", size=22, weight="bold"),
                                ft.Row([
                                        ft.Column([
                                            ft.Image(src="farata_curry.png",width=150,height=120,fit="cover",border_radius=10),
                                            ft.Text("Farata & Curry", text_align="center")
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        ft.Column([
                                            ft.Image(src="mine_frite.png",width=150,height=120,fit="cover",border_radius=10),
                                            ft.Text("Mine Frite", text_align="center")
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        ft.Column([
                                            ft.Image(src="chicken_curry.png",width=150,height=120,fit="cover",border_radius=10),
                                            ft.Text("Chicken Curry", text_align="center")
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    ],
                                    scroll=ft.ScrollMode.HIDDEN,
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=10
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    '"Delicious food, warm atmosphere. Always coming back!"',
                                    italic=True,
                                    text_align="center"
                                ),
                                ft.Text("- A Happy Customer", size=12)
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=10,
                            bgcolor=ft.Colors.LIGHT_GREEN_100,
                        ),
                ],
                scroll=ft.ScrollMode.HIDDEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )


    #Normal view
    main_content = ft.Container(
        content=home_layout,
        expand=True,
    )

    #function to return home
    def go_home(e):
        main_content.content = home_layout
        page.update()
    
    #reset the view to remove what orderId added
    def reset_view():
        main_content.content = ft.Column([result_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()


## USER PROFILE line 58-174 {no changes}
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
        page.run_task(get_my_profile_api, page, container, auth_token, host)

    # update profile
    def update_profile_click(e):
        # We find the container within our main_content: main_content.content.controls[1] is the 'container' Column
        profile_container = main_content.content.controls[1]
        page.run_task(update_profile_api, page, profile_container, auth_token, host)

    # delete profile
    def delete_profile_click(e):
        async def confirm_delete_profile(e):
            nonlocal auth_token
            success, result = await delete_profile_api(auth_token, host)
            if success:
                auth_token = None
                page.snack_bar = ft.SnackBar(ft.Text("Account deleted successfully."))
                page.snack_bar.open = True
                show_login()
                return

            page.snack_bar = ft.SnackBar(ft.Text(result), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

        confirmation_view = ft.Column(
            controls=[
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="red", size=50),
                ft.Text("Confirm Account Deletion", size=20, weight="bold"),
                ft.Text("Are you absolutely sure? This cannot be undone.", text_align="center"),
                ft.Row([
                    ft.Button(
                        "YES, DELETE", 
                        bgcolor=ft.Colors.RED_400, 
                        color="white",
                        on_click=lambda e: page.run_task(confirm_delete_profile, e)
                    ),
                    ft.TextButton("Cancel", on_click=on_profile_click)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        main_content.content = confirmation_view
        page.update()

    # user review page
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
        page.run_task(get_myreviews_api, page, container, auth_token, host)

    # usuer reservation
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
        page.run_task(get_myreservations_api, page, container, auth_token, host)

    ##user order
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
        page.run_task(get_myorders_api, page, container, auth_token, host)

    # user order details
    def myorder_byID_page(e):
        reset_view()
        id_input = ft.TextField(label="Order ID", width=300)
        container = ft.Column(spacing=10)
        new_view = ft.Column(
            controls=[
                ft.Text("Enter your Order ID below:", size=20, weight="bold"),
                id_input,
                ft.Button("Search Order", on_click=lambda _: page.run_task(get_myorder_byID_api, page, container, auth_token, host, id_input)),
                container,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        main_content.content = new_view
        page.update()

## ======================user profile end==================

    def on_menu_click(e):
        reset_view()
        container = ft.Column(spacing=10)
        main_content.content = ft.Column(
            controls=[
                ft.Text("Menu", size=20, weight="bold"),
                container,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.update()
        page.run_task(get_menu_display_api, page, container, auth_token, host)


    ##Reservation page
    def make_reservation(e):
        reset_view()

        selected_date = None
        selected_time = None

        def on_date_change(e):
            nonlocal selected_date
            selected_date = e.control.value
            date_input.text = f"{selected_date.date()}"
            page.update()

        def on_time_change(e):
            nonlocal selected_time
            selected_time = e.control.value
            time_input.text = f"{selected_time}"
            page.update()

        #Field for party size
        party_size = ft.TextField(label="Party Size",width=300,keyboard_type=ft.KeyboardType.NUMBER)
        #field for allergy information
        allergy_info = ft.TextField(label="Allergy Information (optional)",width=300,multiline=True)

        #date input
        date_input = ft.Button(
                        "Pick date",
                        icon=ft.Icons.CALENDAR_MONTH,
                        on_click=lambda e: e.control.page.show_dialog(
                            ft.DatePicker(
                                first_date=datetime.datetime(2023, 10, 1),
                                last_date=datetime.datetime(2026, 12, 1),
                                on_change=on_date_change,
                            )
                        ),
                    )

        #time input
        time_input = ft.Button(
                        "Pick time",
                        icon=ft.Icons.ACCESS_TIME,
                        on_click=lambda e: e.control.page.show_dialog(
                            ft.TimePicker(
                                confirm_text="Confirm",
                                on_change=on_time_change,
                            )
                        ),
                    )

        #Radio buttons for seating choice
        seating = ft.RadioGroup(
                content=ft.Row(
                    controls=[
                        ft.Radio(value="Indoor", label="Indoor"),
                        ft.Radio(value="Outdoor", label="Outdoor"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                value="Indoor",
            )

        container = ft.Column(spacing=15)

        def submit_reservation(e):
            if not selected_date or not selected_time:
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
                auth_token,
                host,
                selected_date,
                selected_time,
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
                ft.Text("Seating Choice", weight="bold",),
                seating,
                allergy_info,
                ft.Button(
                    "Create Reservation",
                    bgcolor=ft.Colors.GREEN,
                    on_click=submit_reservation
                ),
                container
            ],
            spacing=20,
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()


    ## map page
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
                has_permission = await request_location_permission(page, permission_handler)
                if not has_permission:
                    location_text.value = "Location permission is required."
                    page.update()
                    return

                service_enabled = await geo.is_location_service_enabled()
                if not service_enabled:
                    location_text.value = "Please enable location services/GPS."
                    page.update()
                    return

                pos = await geo.get_current_position()
                if not pos:
                    location_text.value = "Could not get location. Please enable GPS."
                    page.update()
                    return

                state["user_marker"] = ftm.MapLatitudeLongitude(
                    pos.latitude,
                    pos.longitude
                )

                location_text.value = f"Your Location: {pos.latitude}, {pos.longitude}"
                map_container.content = build_map()
                page.update()
                
            except Exception as ex:
                location_text.value = f"Error: {ex}"
                page.update()

        map_container.content = build_map()

        map_view = ft.Column(
            controls=[
                ft.Text("Find Us", size=22, weight="bold"),
                ft.Button("Get My Location",on_click=lambda e: page.run_task(get_location, e)),
                location_text,
                map_container
            ],
            expand=True
        )

        main_content.content = map_view
        page.update()


    ## Cart Handler
    def on_place_click(e):
        reset_view()
        cart_container = ft.Column(spacing=10)
    
        main_content.content = ft.Column(
            controls=[ft.Row(controls=[
            ft.Text("Place Order", size=20, weight="bold"),
            ft.IconButton(
                icon=ft.Icons.SHOPPING_CART, 
                
                on_click=lambda _: page.run_task(get_cart_api,page, cart_container, auth_token, host,on_place_click)
            ),],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,) ,
            cart_container],
            scroll=ft.ScrollMode.ADAPTIVE ,)
        
        page.update()
        page.run_task(get_place_api, page, cart_container, auth_token, host)

    def build_app_bar():
        return ft.AppBar(
            leading=ft.Icon(ft.Icons.RESTAURANT),
            # leading_width=40,
            title=ft.Text("Saveur Moris", weight="bold", size=22),
            center_title=False,
            bgcolor=ft.Colors.PINK_ACCENT,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem("My Profile", on_click=on_profile_click),
                        ft.PopupMenuItem("My Reviews", on_click=on_review_click),
                        ft.PopupMenuItem("My Reservations", on_click=on_reservation_click),
                        ft.PopupMenuItem("My Orders", on_click=on_orders_click),
                        ft.PopupMenuItem("My Detail Orders", on_click=myorder_byID_page),
                        ft.PopupMenuItem("Logout", on_click=on_logout_click),
                    ]
                ),
            ],
        )

    # navigations bar control
    def on_nav_change(e):
        if e.control.selected_index == 0:
            go_home(e)
        elif e.control.selected_index == 1:
            on_menu_click(e)
        elif e.control.selected_index == 2:
            on_place_click(e)
        elif e.control.selected_index == 3:
            make_reservation(e)
        elif e.control.selected_index == 4:
            on_find_us_click(e)  

    pagelet = ft.Pagelet(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.RESTAURANT_MENU, label="Menu"),
                ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART_CHECKOUT, label="Order"),
                ft.NavigationBarDestination(icon=ft.Icons.TABLE_BAR, label="Reservation"),
                ft.NavigationBarDestination(icon=ft.Icons.NAVIGATION, label="Find Us")],
                on_change=on_nav_change
                ),
        content=ft.Container(),
        height=120,
    )

    def show_app():
        main_content.content = home_layout
        pagelet.navigation_bar.selected_index = 0
        page.controls = [main_content, pagelet]
        page.appbar = build_app_bar()
        page.update()

    show_login()

ft.run(main, assets_dir="src/assets")
