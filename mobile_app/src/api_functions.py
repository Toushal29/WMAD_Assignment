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
            container.controls.extend([ft.Text("Failed to load reviews", color="red"), ft.Text(f"Error: {response}", color="red")])
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
        container.controls.extend([ft.Text("Failed to load reservations", color="red"), ft.Text(f"Error: {response}", color="red")])
    page.update()


async def create_reservation_api(page,container,my_token,host,selected_date,selected_time,party_size,seating,allergy_info):
    endpoint = f"{host}api/reservations/create/"
    headers = {"Authorization": f"Token {my_token}"}

    data = {
        "reservation_date": selected_date.strftime("%Y-%m-%d"),
        "reservation_time": selected_time.strftime("%H:%M:%S"),
        "party_size": int(party_size.value) if party_size.value else 1,
        "seating_choice": seating.value,
        "allergy_info": allergy_info.value
    }

    if not data["reservation_date"] or not data["reservation_time"]:
        page.snack_bar = ft.SnackBar(ft.Text("Please select date and time"),bgcolor="red")
        page.snack_bar.open = True
        page.update()
        return

    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint,json=data,headers=headers)
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
        container.controls.extend([
            ft.Text("Failed to create reservation", color="red"),
            ft.Text(str(response.text), size=10, color="red")
        ])

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


####placing order
async def add_to_cart_api(page, my_token, host, menu_id, quantity=1):##respond to send data to cart
    endpoint = f"{host}api/cart/add/"
    headers = {
        "Authorization": f"Token {my_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "menu": menu_id,
        "quantity": quantity
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(endpoint, headers=headers, json=payload)
            if 200 <= response.status_code <= 299:
                # Provide visual feedback of success
                page.snack_bar = ft.SnackBar(ft.Text("Added to cart successfully!"), bgcolor="green")
                page.snack_bar.open = True
            else:
                # Provide feedback if the request fails
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {response.status_code}"), bgcolor="red")
                page.snack_bar.open = True
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Request failed: {e}"), bgcolor="red")
            page.snack_bar.open = True
    
    page.update()

async def get_place_api(page, container, my_token, host):   ##call add to cart to send data to cart
    headers = {"Authorization": f"Token {my_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{host}api/menus/", headers=headers)
        container.controls.clear()
        if 200 <= response.status_code <= 299:
            for item in response.json():
                if item.get('available'):
                    container.controls.append(
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                width=350, # Standard card width from sources
                                content=ft.Column([
                                    # ROW: Image on left, Button on right
                                    ft.Row([
                                        ft.Image(
                                            src=f"{host}{item.get('image')}", 
                                            # Fixed width to allow button space
                                            height=150, 
                                            expand=True,
                                            fit="cover",
                                            
                                            border_radius=10
                                        ) if item.get('image') else ft.Container(width=280, height=150),
                                        
                                        # The Add to Cart Button
                                        ft.IconButton(
                                            icon=ft.Icons.ADD_SHOPPING_CART,
                                            icon_color="green",
                                            
                                            on_click=lambda e,
                                            m_id=item['id']: page.run_task(add_to_cart_api,page,my_token,host,m_id,1,)
                                                                    
                                                                                        
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                                    ft.Row([
                                        ft.Text(item['name'], weight="bold", size=16,expand=True,),
                                        ft.Text(f"Rs {item['price']}", color="green", weight="bold",expand=True,),
                                        
                                    ], alignment="spaceBetween"),
                                    
                                ])
                            )
                        )
                    )
        page.update()


async def get_cart_api(page, container, my_token, host,on_place_click):  ##get cart data from cartitem
    
    endpoint = f"{host}api/cart/get/"
    headers = {"Authorization": f"Token {my_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers=headers)
        container.controls.clear()
        
        if 200 <= response.status_code <= 299:
            data = response.json()
            total_cart_price = 0
            
            
            item_list={"items": []}
            for item in data:
                
                item_list["items"].append({
                       "menu_id": item["menu"],
                       "quantity": item["quantity"] })
        
    

                total_cart_price += item.get('subtotal', 0)

                container.controls.append(
                    ft.Container(
                        padding=10,
                        border=ft.Border.all(width=1, color=ft.Colors.OUTLINE_VARIANT),
                        border_radius=10,
                        content=ft.Row([
                            ft.Column([
                                ft.Text(item['menu_name'], weight="bold",expand= True),
                                ft.Text(f"Quantity: {item['quantity']}"),
                            ], expand=True),
                            ft.Text(f"Rs {item['subtotal']}", weight="bold",expand= True),
                            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE,icon_color="red",
                            on_click=lambda e, item_id=item['id']: page.run_task(delete_cart_item_api,page,container,my_token,host,item_id,on_place_click))
                        ],  ) 
                    )
                )

            container.controls.extend([
                ft.Divider(),
                ft.Row([
                    ft.Text("Total Amount:", size=18, weight="bold",expand=True),
                    ft.Text(f"Rs {total_cart_price}", size=18, weight="bold",expand= True, color="green"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=20),
                # Checkout button (unresponsive)
                ft.Button("Clear Cart",expand= True,width=350,bgcolor=ft.Colors.RED,on_click=lambda _: page.run_task(clear_cart_api,page, container, my_token, host,on_place_click)), 
                ft.Container(height=10,expand= True),
                ft.Button("Checkout",  width=350,expand= True,on_click= lambda _: page.run_task(show_checkout_view,page, container, my_token, host,item_list)),
                # Clear button (unresponsive) below
                ft.Container(height=20,expand= True,),
                ft.Container(height=10,expand= True),
            ])
        else:
            container.controls.append(ft.Text("Failed to load Cart", color="red"))
        
        page.update()


####
async def clear_cart_api(page, container, my_token, host,on_place_click):
    endpoint = f"{host}api/cart/clear/" 
    headers = {"Authorization": f"Token {my_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(endpoint, headers=headers)
        
        if response.status_code == 204 or response.status_code == 200:
           
            # Refresh the cart UI to show it's empty
            await get_cart_api(page, container, my_token, host,on_place_click) 
        else:
            
            page.snack_bar = ft.SnackBar(ft.Text("Failed to clear cart"))
           
            page.update()


async def delete_cart_item_api(page, container, my_token, host, cart_item_id,on_place_click):
    endpoint = f"{host}api/cart/delete/{cart_item_id}/" 
    headers = {"Authorization": f"Token {my_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(endpoint, headers=headers)
        
        if response.status_code == 204:
            # Refresh the UI to remove the specific card
            await get_cart_api(page, container, my_token, host, on_place_click)


### we use cart to extract data for order
async def show_checkout_view(page, container, my_token, host, item_list):

    print(item_list)

    container.controls.clear()
    payment_dropdown = ft.Dropdown(
    label="Select Payment Method",
    width=350,
    hint_text="Choose how you want to pay",
    options=[
        ft.dropdown.Option("juice", "MCB Juice / Transfer"),
        ft.dropdown.Option("card", "Debit/Credit Card"),
        ft.dropdown.Option("cash", "Pay on Take-away"),
    ],
    value="cash", # Default selection
)
    # Add instructions
    container.controls.extend([
        ft.Container(height=10,expand= True),
        ft.Text("Checkout Summary", size=20, weight="bold"),

        payment_dropdown, # The dropdown defined above
        
        ft.Button(
            
            "Confirm and Place Order",

            expand = True,
            icon=ft.Icons.CHECK_CIRCLE,
            on_click=lambda _: page.run_task(place_order_api,page, my_token, host, item_list,payment_dropdown.value,container)
        )
    ])
    page.update()


async def place_order_api(page, my_token, host, item_list, payment_method,container):
    endpoint = f"{host}api/orders/place/"
    endpoint1 = f"{host}api/cart/clear/" 
    headers = {
        "Authorization": f"Token {my_token}",
        "Content-Type": "application/json"
    }
    print(payment_method)
    payload= item_list
    item_list["payment_method"] = "cash"
    # The payload now includes the payment_method from the dropdown
    

    async with httpx.AsyncClient() as client:
        print("success")
        response = await client.post(endpoint, headers=headers, json=payload)
        response = await client.delete(endpoint1, headers=headers)
        await get_myorders_api(page, container, my_token, host)
