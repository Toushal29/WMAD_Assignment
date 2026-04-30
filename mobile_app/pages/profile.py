import flet as ft
import httpx

def profile_page(page: ft.Page, my_token, host):
    """Display user profile from API"""
    
    # Container for profile data
    profile_container = ft.Column(spacing=15)
    
    # Loading indicator
    loading = ft.ProgressRing()
    
    # Track edit mode
    edit_mode = False
    current_data = {}
    
    # Form fields (will be created dynamically)
    first_name_field = None
    last_name_field = None
    email_field = None
    phone_field = None
    address_field = None
    
    def load_profile():
        """Fetch profile data from API"""
        nonlocal current_data
        profile_container.controls.clear()
        profile_container.controls.append(loading)
        page.update()
        
        try:
            # Make API call to get profile (correct endpoint)
            response = httpx.get(
                f"{host}api/my-profile/",  # ← UPDATED: correct API path
                headers={"Authorization": f"Token {my_token}"}
            )
            
            profile_container.controls.clear()
            
            if response.status_code == 200:
                current_data = response.json()
                
                # Create display mode
                if not edit_mode:
                    profile_container.controls.extend([
                        ft.Text("Profile Information", size=20, weight="bold"),
                        ft.Divider(),
                        ft.Text(f"Username: {current_data.get('user', {}).get('username', 'N/A')}"),
                        ft.Text(f"First Name: {current_data.get('user', {}).get('first_name', 'Not set')}"),
                        ft.Text(f"Last Name: {current_data.get('user', {}).get('last_name', 'Not set')}"),
                        ft.Text(f"Email: {current_data.get('user', {}).get('email', 'Not set')}"),
                        ft.Text(f"Phone: {current_data.get('phone', 'Not set')}"),
                        ft.Text(f"Address: {current_data.get('address', 'Not set')}"),
                        ft.Divider(),
                        ft.Row([
                            ft.ElevatedButton("Edit Profile", on_click=toggle_edit, bgcolor=ft.Colors.BLUE_300),
                            ft.ElevatedButton("Refresh", on_click=lambda e: load_profile(), bgcolor=ft.Colors.GREEN_300),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    ])
                else:
                    # Edit mode - show form fields
                    user_data = current_data.get('user', {})
                    first_name_field = ft.TextField(label="First Name", value=user_data.get('first_name', ''), width=300)
                    last_name_field = ft.TextField(label="Last Name", value=user_data.get('last_name', ''), width=300)
                    email_field = ft.TextField(label="Email", value=user_data.get('email', ''), width=300)
                    phone_field = ft.TextField(label="Phone", value=current_data.get('phone', ''), width=300)
                    address_field = ft.TextField(label="Address", value=current_data.get('address', ''), width=300, multiline=True)
                    
                    profile_container.controls.extend([
                        ft.Text("Edit Profile", size=20, weight="bold"),
                        ft.Divider(),
                        first_name_field,
                        last_name_field,
                        email_field,
                        phone_field,
                        address_field,
                        ft.Divider(),
                        ft.Row([
                            ft.ElevatedButton("Save", on_click=lambda e: save_profile(), bgcolor=ft.Colors.GREEN_300),
                            ft.ElevatedButton("Cancel", on_click=toggle_edit, bgcolor=ft.Colors.RED_300),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    ])
                    
                    # Store references for save function
                    page._first_name_field = first_name_field
                    page._last_name_field = last_name_field
                    page._email_field = email_field
                    page._phone_field = phone_field
                    page._address_field = address_field
            else:
                profile_container.controls.append(
                    ft.Text(f"Error loading profile: {response.status_code}", color=ft.Colors.RED)
                )
                profile_container.controls.append(
                    ft.ElevatedButton("Retry", on_click=lambda e: load_profile())
                )
        except Exception as e:
            profile_container.controls.clear()
            profile_container.controls.append(
                ft.Text(f"Connection error: {e}", color=ft.Colors.RED)
            )
            profile_container.controls.append(
                ft.ElevatedButton("Retry", on_click=lambda e: load_profile())
            )
        
        page.update()
    
    def save_profile():
        """Save updated profile data"""
        try:
            # Prepare update data
            update_data = {
                "user": {
                    "first_name": page._first_name_field.value,
                    "last_name": page._last_name_field.value,
                    "email": page._email_field.value,
                },
                "phone": page._phone_field.value,
                "address": page._address_field.value,
            }
            
            # Make API call to update profile (correct endpoint)
            response = httpx.put(
                f"{host}api/upd_profile/",  # ← UPDATED: correct API path
                json=update_data,
                headers={"Authorization": f"Token {my_token}"}
            )
            
            if response.status_code in [200, 201]:
                # Show success message
                page.snack_bar = ft.SnackBar(
                    ft.Text("Profile updated successfully!"),
                    bgcolor=ft.Colors.GREEN
                )
                page.snack_bar.open = True
                
                # Exit edit mode and reload
                nonlocal edit_mode
                edit_mode = False
                load_profile()
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Update failed: {response.status_code}"),
                    bgcolor=ft.Colors.RED
                )
                page.snack_bar.open = True
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {e}"),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
        
        page.update()
    
    def toggle_edit(e):
        nonlocal edit_mode
        edit_mode = not edit_mode
        load_profile()
    
    # Load profile when page opens
    load_profile()
    
    return ft.View(
        "/profile",
        controls=[
            ft.AppBar(title=ft.Text("My Profile"), bgcolor=ft.Colors.ORANGE_100),
            ft.Container(
                content=profile_container,
                padding=20,
                expand=True,
            ),
        ],
    )