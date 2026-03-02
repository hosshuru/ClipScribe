import flet as ft
from app import App

def main(page: ft.Page):
    # Theme Setting
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)

    page.padding = 0
    page.spacing = 0

    page.title = "ClipScribe"

    page.render(App)

if __name__ == "__main__":
    ft.run(main)