import flet as ft

def profile_page(page: ft.Page, my_token, host):
    """Display user profile"""
    
    # Container for profile data
    profile_container = ft.Column(spacing=15)
    
    # Loading indicator
    loading = ft.ProgressRing()
    
    # Function to load profile
    def load_profile():
        profile_container.controls.clear()
        profile_container.controls.append(loading)
        page.update()
        
        # Call API to get profile
        # For now, show placeholder
        profile_container.controls.clear()
        profile_container.controls.extend([
            ft.Text("Profile Information", size=20, weight="bold"),
            ft.Text(f"Username: {page.session.get('username', 'User')}"),
            ft.Text("Email: user@example.com"),
            ft.Text("Phone: Not provided"),
            ft.Text("Address: Not provided"),
            ft.Divider(),
            ft.ElevatedButton("Edit Profile", bgcolor=ft.Colors.BLUE_300),
            ft.ElevatedButton("Change Password", bgcolor=ft.Colors.ORANGE_300),
        ])
        page.update()
    
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