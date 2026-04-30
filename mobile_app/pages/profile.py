import flet as ft
import httpx

def profile_page(page: ft.Page, my_token, host):
    """Display user profile from API"""
    
    # Container for profile data
    profile_container = ft.Column(spacing=15)
    
    # Loading indicator
    loading = ft.ProgressRing()
    
    # Form fields for editing
    edit_mode = False
    original_data = {}
    
    # Function to load profile from API
    def load_profile():
        profile_container.controls.clear()
        profile_container.controls.append(loading)
        page.update()
        
        try:
            # Make API call
            response = httpx.get(
                f"{host}api/my-profile/",
                headers={"Authorization": f"Token {my_token}"}
            )
            
            profile_container.controls.clear()
            
            if response.status_code == 200:
                data = response.json()
                original_data = data
                
                # Display profile info
                profile_container.controls.extend([
                    ft.Text("Profile Information", size=20, weight="bold"),
                    ft.Text(f"Username: {data.get('user', {}).get('username', 'N/A')}"),
                    ft.TextField(label="First Name", value=data.get('user', {}).get('first_name', ''), width=300),
                    ft.TextField(label="Last Name", value=data.get('user', {}).get('last_name', ''), width=300),
                    ft.TextField(label="Email", value=data.get('user', {}).get('email', ''), width=300),
                    ft.TextField(label="Phone", value=data.get('phone', ''), width=300),
                    ft.TextField(label="Address", value=data.get('address', ''), width=300, multiline=True),
                    ft.Divider(),
                    ft.Row([
                        ft.ElevatedButton("Edit", on_click=toggle_edit, bgcolor=ft.Colors.BLUE_300),
                        ft.ElevatedButton("Refresh", on_click=lambda e: load_profile(), bgcolor=ft.Colors.GREEN_300),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ])
            else:
                profile_container.controls.append(ft.Text(f"Error loading profile: {response.status_code}", color=ft.Colors.RED))
        except Exception as e:
            profile_container.controls.clear()
            profile_container.controls.append(ft.Text(f"Connection error: {e}", color=ft.Colors.RED))
        
        page.update()
    
    def toggle_edit(e):
        nonlocal edit_mode
        edit_mode = not edit_mode
        
        # Refresh profile to show/hide edit buttons
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