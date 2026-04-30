import flet as ft
from api_functions import *

import flet_map as ftm
import flet_geolocator as ftg


async def main(page: ft.Page):
    page.window.always_on_top = True
    page.title = "API Calls Profile - main2.py"
    page.window.width = 400
    page.window.height = 700
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    my_token = "a5842a6437612fed23a00407b72fcff384e776b7"
    host = "http://127.0.0.1:8000/"

    geo = ftg.Geolocator(
        configuration=ftg.GeolocatorConfiguration(
            accuracy=ftg.GeolocatorPositionAccuracy.HIGH
        )
    )

    result_text = ft.Text()

    home_layout = ft.Column(
        [
            ft.Text("Welcome to Saveur Moris", size=25, weight="bold"),
            ft.Text("Experience the best Mauritian cuisine", italic=True),
            ft.Image(
                src="https://flet.dev/img/pages/quick-start/flet-app-icons.png",
                width=200,
            ),
            ft.Text("Select an option from the menu to get started."),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    main_content = ft.Container(content=home_layout, expand=True)

    def go_home(e):
        main_content.content = home_layout
        page.update()

    def reset_view():
        main_content.content = ft.Column(
            [result_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()

    # ================= MENU FIX ADDED HERE =================
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

        # Fetch menu from Django API
        page.run_task(get_place_api, page, container, my_token, host)
    # ======================================================

    def on_place_click(e):
        reset_view()

        cart_container = ft.Column(spacing=10)

        main_content.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Place Order", size=20, weight="bold"),
                        ft.IconButton(
                            icon=ft.Icons.SHOPPING_CART,
                            on_click=lambda _: page.run_task(
                                get_cart_api,
                                page,
                                cart_container,
                                my_token,
                                host,
                                on_place_click,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                cart_container,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        page.update()

        page.run_task(get_place_api, page, cart_container, my_token, host)

    def on_reservation_click(e):
        reset_view()

        party_size = ft.TextField(label="Party Size", width=300)

        allergy_info = ft.TextField(
            label="Allergy Information", width=300, multiline=True
        )

        date_input = ft.TextField(label="Date (YYYY-MM-DD)", width=300)
        time_input = ft.TextField(label="Time (HH:MM)", width=300)

        seating = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(value="Indoor", label="Indoor"),
                    ft.Radio(value="Outdoor", label="Outdoor"),
                ]
            ),
            value="Indoor",
        )

        container = ft.Column(spacing=15)

        def submit_reservation(e):
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
                allergy_info,
            )

        main_content.content = ft.Column(
            controls=[
                ft.Text("Make a Reservation", size=22, weight="bold"),
                party_size,
                date_input,
                time_input,
                seating,
                allergy_info,
                ft.ElevatedButton("Create", on_click=submit_reservation),
                container,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        page.update()

    # ================= MAP =================
    def on_find_us_click(e):
        reset_view()

        state = {"user_marker": None}
        location_text = ft.Text("Click below to get your location")

        map_container = ft.Container(expand=True)

        async def get_location(e):
            pos = await geo.get_current_position()

            state["user_marker"] = ftm.MapLatitudeLongitude(
                pos.latitude, pos.longitude
            )

            location_text.value = f"{pos.latitude}, {pos.longitude}"

            map_container.content = ftm.Map(
                expand=True,
                initial_center=state["user_marker"],
                initial_zoom=14,
                layers=[
                    ftm.TileLayer(
                        url_template="https://tile.memomaps.de/tilegen/{z}/{x}/{y}.png"
                    ),
                    ftm.MarkerLayer(
                        markers=[
                            ftm.Marker(
                                coordinates=state["user_marker"],
                                content=ft.Icon(
                                    ft.Icons.MY_LOCATION,
                                    color=ft.Colors.BLUE,
                                    size=40,
                                ),
                            )
                        ]
                    ),
                ],
            )

            page.update()

        main_content.content = ft.Column(
            [
                ft.Text("Find Us", size=22, weight="bold"),
                ft.ElevatedButton(
                    "Get My Location",
                    on_click=lambda e: page.run_task(get_location, e),
                ),
                location_text,
                map_container,
            ]
        )

        page.update()

    # ================= NAVIGATION =================
    def on_nav_change(e):
        if e.control.selected_index == 0:
            on_menu_click(e)   # ✅ FIXED
        elif e.control.selected_index == 1:
            on_place_click(e)
        elif e.control.selected_index == 2:
            on_reservation_click(e)

    pagelet = ft.Pagelet(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.RESTAURANT_MENU, label="Menu"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SHOPPING_CART_CHECKOUT, label="Order"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.TABLE_BAR, label="Reservation"
                ),
            ],
            on_change=on_nav_change,
        ),
        content=ft.Container(),
        height=70,
    )

    page.add(
        pagelet,
        main_content,
        ft.Button("Home", on_click=go_home),
    )


ft.app(main)