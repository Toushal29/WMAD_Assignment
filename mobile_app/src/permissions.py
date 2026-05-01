import flet as ft
from flet_permission_handler import Permission, PermissionHandler, PermissionStatus


def build_permission_handler():
    return PermissionHandler()


def _show_permission_message(page, message, open_settings=None):
    page.snack_bar = ft.SnackBar(
        ft.Text(message),
        action=ft.SnackBarAction(
            "Settings",
            on_click=lambda _: page.run_task(open_settings),
        )
        if open_settings
        else None,
        bgcolor=ft.Colors.RED_300,
    )
    page.snack_bar.open = True
    page.update()


async def request_permission(page, permission_handler, permission, feature_name):
    status = await permission_handler.get_status(permission)

    if status == PermissionStatus.GRANTED:
        return True

    status = await permission_handler.request(permission)
    if status == PermissionStatus.GRANTED:
        return True

    if status == PermissionStatus.PERMANENTLY_DENIED:
        _show_permission_message(
            page,
            f"{feature_name} permission is blocked. Enable it in app settings.",
            permission_handler.open_app_settings,
        )
    else:
        _show_permission_message(
            page,
            f"{feature_name} permission is needed to use this feature.",
        )

    return False


async def request_location_permission(page, permission_handler):
    return await request_permission(
        page,
        permission_handler,
        Permission.LOCATION_WHEN_IN_USE,
        "Location",
    )


async def request_camera_permission(page, permission_handler):
    return await request_permission(
        page,
        permission_handler,
        Permission.CAMERA,
        "Camera",
    )


async def request_microphone_permission(page, permission_handler):
    return await request_permission(
        page,
        permission_handler,
        Permission.MICROPHONE,
        "Microphone",
    )


async def request_storage_permission(page, permission_handler):
    return await request_permission(
        page,
        permission_handler,
        Permission.STORAGE,
        "Storage",
    )


async def request_notification_permission(page, permission_handler):
    return await request_permission(
        page,
        permission_handler,
        Permission.NOTIFICATION,
        "Notification",
    )


async def request_sensor_permission(page, permission_handler):
    return await request_permission(
        page,
        permission_handler,
        Permission.SENSORS,
        "Sensor",
    )
