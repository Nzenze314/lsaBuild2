import flet as ft

# Base colors
PRIMARY_COLOR = "#740BF4"
SECONDARY_COLOR = "#9747FF"

def get_light_theme():
    return ft.Theme(
        color_scheme_seed=PRIMARY_COLOR,
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            primary_container=SECONDARY_COLOR,
            secondary=SECONDARY_COLOR,
            background="#FFFFFF",
            on_background="#000000",
            surface="#F4F4F4",
            on_surface="#000000",
            surface_tint=PRIMARY_COLOR,
            on_primary="#222222", # text color on primary
            on_secondary="#F0F0F0",
            on_primary_container="#FFFFFF",
            on_secondary_container="#FFFFFF",
        ),
        visual_density=ft.VisualDensity.COMFORTABLE, 
        use_material3=True,
    )

def get_dark_theme():
    return ft.Theme(
        color_scheme_seed=PRIMARY_COLOR,
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            primary_container=SECONDARY_COLOR,
            secondary=SECONDARY_COLOR,
            background="#000000",
            on_background="#FFFFFF",
            surface="#121212",
            on_surface="#FFFFFF",
            surface_tint=PRIMARY_COLOR,
            on_primary="#FFFFFF",
            on_secondary="#FFFFFF",
            on_primary_container="#FFFFFF",
            on_secondary_container="#FFFFFF",
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
        use_material3=True,
    )
