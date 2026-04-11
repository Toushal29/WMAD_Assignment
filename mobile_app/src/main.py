from flet import *
import flet as ft
import httpx
import json

async def main(page: ft.Page):
    page.title = "Profile"
    page.window.width = 400
    page.window.height = 700
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    my_token = "55242da82c27f93d95e939bdda2b49076f0672c2"

    # get_all_api_endpint = "http://127.0.0.1:8000/api/customers/"

    host = "http://127.0.0.1:8000/"

    get_my_profile_api_endpoint = f"{host}api/my-profile/"
    get_myreviews_api_endpoint = f"{host}api/my-reviews/"
    get_myreservations_api_endpoint = f"{host}api/my-reservations/"
    get_myorders_api_endpoint = f"{host}api/my-orders/"
    
    result_text = ft.Text()

    # Normal view
    main_content = ft.Container(
        content=ft.Column([result_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True
    )

    def show_main_results(e=None):
        """Resets the view back to the original result_text container"""
        main_content.content = ft.Column(
            [result_text], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.update()

    async def get_my_profile_api(e):
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Token {my_token}"}
                response = await client.get(get_my_profile_api_endpoint, headers=headers)
                if response.status_code >= 200 and response.status_code <= 299:
                    data = response.json()
                    result_text.value = data
                    result_text.color = ft.Colors.BLUE
                else:
                    result_text.value = f"Error: {response}"
                page.update()

    async def get_myreviews_api(e):
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Token {my_token}"}
                response = await client.get(get_myreviews_api_endpoint, headers=headers)
                if response.status_code >= 200 and response.status_code <= 299:
                    data = response.json()
                    result_text.value = data
                    result_text.color = ft.Colors.BLUE
                else:
                    result_text.value = f"Error: {response}"
                page.update()

    async def get_myreservations_api(e):
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Token {my_token}"}
                response = await client.get(get_myreservations_api_endpoint, headers=headers)
                if response.status_code >= 200 and response.status_code <= 299:
                    data = response.json()
                    result_text.value = data
                    result_text.color = ft.Colors.BLUE
                else:
                    result_text.value = f"Error: {response}"                
                page.update()

    async def get_myorders_api(e):
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Token {my_token}"}
                response = await client.get(get_myorders_api_endpoint, headers=headers)
                if response.status_code >= 200 and response.status_code <= 299:
                    data = response.json()
                    result_text.value = data
                    result_text.color = ft.Colors.BLUE
                else:
                    result_text.value = f"Error: {response}"
                page.update()

    async def get_myorder_byID_api(id_input_control):
            async with httpx.AsyncClient() as client:
                order_id = id_input_control.value
                get_myorder_byID_api_endpoint = f"{host}api/orders/{order_id}/items/"
                headers = {"Authorization": f"Token {my_token}"}

                response = await client.get(get_myorder_byID_api_endpoint, headers=headers)
                
                if response.status_code >= 200 and response.status_code <= 299:
                    data = response.json()
                    result_text.value = data
                    result_text.color = ft.Colors.BLUE
                    show_main_results()
                else:
                    result_text.value = f"Error: {response}"
                    result_text.color = ft.Colors.RED
                    show_main_results()
                page.update()

    def myorder_byID_page(e):
        id_input = ft.TextField(label="Order ID", width=300)
        search_button = ft.ElevatedButton(
        "Search Order", 
        on_click=lambda _: page.run_task(get_myorder_byID_api, id_input)
    )
        back_button = ft.TextButton("Back", on_click=show_main_results)
        new_view = ft.Column(
            controls=[
                ft.Text("Enter your Order ID below:", size=20, weight="bold"),
                id_input,
                search_button,
                back_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        main_content.content = new_view
        page.update()

    def app_bar():
        pagelet = ft.Pagelet(
            appbar=ft.AppBar(
                # leading=ft.Icon(ft.Icons.PALETTE),
                leading_width=40,
                title=ft.Text("Saveur Moris"),
                center_title=False,
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem("My Profile", on_click=get_my_profile_api),
                            ft.PopupMenuItem("My Reviews", on_click=get_myreviews_api),
                            ft.PopupMenuItem("My Reservations", on_click=get_myreservations_api),
                            ft.PopupMenuItem("My Orders", on_click=get_myorders_api),
                            ft.PopupMenuItem("My Detail Orders", on_click=myorder_byID_page),
                        ]
                    ),
                ],
            ),
            content=ft.Container(),
            height=200,
        )
        return pagelet

    page.add(
        app_bar(),
        main_content,)

ft.app(target=main)