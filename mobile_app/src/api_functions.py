import httpx
import flet as ft
import json

async def get_my_profile_api(page, container, my_token, host):
    endpoint = f"{host}api/my-profile/"
    headers = {"Authorization": f"Token {my_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers=headers)
        container.controls.clear()
        if 200 <= response.status_code <= 299:
            data = response.json()
            container.controls.extend([
                ft.TextField(label="Username", value=str(data["user"]["username"]), width=350, bgcolor=ft.Colors.RED_100, read_only=True),
                ft.TextField(label="First Name", value=str(data["user"]["first_name"]), width=350),
                ft.TextField(label="Last Name", value=str(data["user"]["last_name"]), width=350),
                ft.TextField(label="Email", value=str(data["user"]["email"]), width=350),
                ft.TextField(label="Phone", value=str(data["phone"]), width=350),
                ft.TextField(label="Address", value=str(data["address"]), width=350),
            ])
        else:
            container.controls.add(ft.Text("Failed to load Profile", color="red"), ft.Text(f"Error: {response}", color="red"))
        page.update()


async def update_profile_api(page, container, my_token, host):
    # Extract data from the controls based on the order they were added
    # 0:Username, 1:First Name, 2:Last Name, 3:Email, 4:Phone, 5:Address
    payload = {
        "user": {
            "first_name": container.controls[1].value,
            "last_name": container.controls[2].value,
            "email": container.controls[3].value,
        },
        "phone": container.controls[4].value,
        "address": container.controls[5].value,
    }

    endpoint = f"{host}api/upd_profile/"
    headers = {"Authorization": f"Token {my_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(endpoint, json=payload, headers=headers)
        if 200 <= response.status_code <= 299:
            page.snack_bar = ft.SnackBar(ft.Text("Profile updated successfully!"))
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Update failed: {response.status_code}"), bgcolor="red")
            page.snack_bar.open = True
        page.update()


async def delete_profile_api(page, main_content, my_token, host):
    endpoint = f"{host}api/profile/delete/"
    headers = {"Authorization": f"Token {my_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(endpoint, headers=headers)
        
        if response.status_code in [200, 204]:
            # Clear everything and show Login/Signup screen
            main_content.content = ft.Column(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="green", size=50),
                    ft.Text("Account Deleted", size=24, weight="bold"),
                    ft.Divider(),
                    ft.Text("Welcome to Saveur Moris", size=18),
                    ft.ElevatedButton("Login", width=200, on_click=lambda _: print("Go to Login")),
                    ft.OutlinedButton("Sign Up", width=200, on_click=lambda _: print("Go to Signup")),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        else:
            # Show error inside the container instead of a popup
            main_content.content.controls.append(
                ft.Text(f"Delete Failed: {response.status_code}", color="red")
            )
            
        page.update()


async def get_myreviews_api(page, container, my_token, host):
    endpoint = f"{host}api/my-reviews/"
    headers = {"Authorization": f"Token {my_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers=headers)
        container.controls.clear()
        if 200 <= response.status_code <= 299:
            data = response.json()
            for item in data:
                container.controls.append(
                    ft.Card(
                        content=ft.Container(
                            width= 350,
                            padding=5,
                            content=ft.Column([
                                ft.Text(f"Menu: {item.get('menu_name', 'General')}", weight="bold"),
                                ft.Text(f"Rating: {'⭐' * item['rating']}"),
                                ft.Text(f"Comment: {item['comment']}", italic=True),
                                ft.Text(f"Date: {item['created_at'][:10]}", size=10),
                            ])
                        )
                    )
                )
        else:
            container.controls.append(ft.Text("Failed to load reviews", color="red"), ft.Text(f"Error: {response}", color="red"))
        page.update()


async def get_myreservations_api(page, container, my_token, host):
    endpoint = f"{host}api/my-reservations/"
    headers = {"Authorization": f"Token {my_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers=headers)
    container.controls.clear()
    if 200 <= response.status_code <= 299:
        data = response.json()
        for res in data:
            container.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color="blue"),
                        title=ft.Text(f"Date: {res['reservation_date']} @ {res['reservation_time']}"),
                        subtitle=ft.Text(f"Status: {res['status'].upper()} | Size: {res['party_size']}"),
                        trailing=ft.Text(res['seating_choice']),
                    )
                )
            )
    else:
        container.controls.append(ft.Text("Failed to load reviews", color="red"), ft.Text(f"{response}", color="red"))
    page.update()


async def create_reservation_api(
    page,
    container,
    my_token,
    host,
    selected_date,
    selected_time,
    party_size,
    seating,
    allergy_info
):
    endpoint = f"{host}api/reservations/create/"
    headers = {"Authorization": f"Token {my_token}"}


    data = {
        "reservation_date": selected_date.current,
        "reservation_time": selected_time.current,
        "party_size": int(party_size.value) if party_size.value else 1,
        "seating_choice": seating.value,
        "allergy_info": allergy_info.value
    }


    if not data["reservation_date"] or not data["reservation_time"]:
        page.snack_bar = ft.SnackBar(
            ft.Text("Please select date and time"),
            bgcolor="red"
        )
        page.snack_bar.open = True
        page.update()
        return


    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            json=data,
            headers=headers
        )

    container.controls.clear()


    if 200 <= response.status_code <= 299:
        container.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=40),
                        ft.Text("Reservation Created!", size=18, weight="bold"),
                        ft.Text(f"Date: {data['reservation_date']}"),
                        ft.Text(f"Time: {data['reservation_time']}"),
                        ft.Text(f"Party Size: {data['party_size']}"),
                    ])
                )
            )
        )
    else:
        container.controls.append(
            ft.Text("Failed to create reservation", color="red"),
            ft.Text(str(response.text), size=10, color="red")
        )

    page.update()


async def get_myorders_api(page, container, my_token, host):
    endpoint = f"{host}api/my-orders/"
    headers = {"Authorization": f"Token {my_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers=headers)
        container.controls.clear()
        if 200 <= response.status_code <= 299:
            data = response.json()
            for order in data:
                container.controls.append(
                    ft.Card(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.SHOPPING_BAG, color="green"),
                            title=ft.Text(f"Order #{order['id']} - Rs {order['total_price']}"),
                            subtitle=ft.Text(f"Status: {order['status']} | Paid via: {order['payment_method']}"),
                        )
                    )
                )
        else:
            container.controls.append(ft.Text("Failed to load reviews", color="red"), ft.Text(f"{response}", color="red"))
        page.update()


async def get_myorder_byID_api(page, container, my_token, host, id_input):
    order_id = id_input.value
    endpoint = f"{host}api/orders/{order_id}/items/"
    headers = {"Authorization": f"Token {my_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers=headers)
        container.controls.clear()
        if 200 <= response.status_code <= 299:
            data = response.json()
            for item in data:
                container.controls.append(
                    ft.Container(
                        padding=10,
                        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                        border_radius=10,
                        content=ft.Row([
                            ft.Column([
                                ft.Text(item['menu_name'], weight="bold"),
                                ft.Text(f"Qty: {item['quantity']} x Rs {item['price']}"),
                            ], expand=True),
                            ft.Text(f"Rs {item['subtotal']}", weight="bold", size=16)
                        ])
                    )
                )
        else:
            container.controls.append(ft.Text("Failed to load reviews", color="red"), ft.Text(f"{response}", color="red"))
        page.update()