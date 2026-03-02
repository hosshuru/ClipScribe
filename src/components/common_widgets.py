import flet as ft
from context import ClipContext
from pathlib import Path

@ft.component
def ClipSidebar(on_clip_select):
    clip_model = ft.use_context(ClipContext)

    clip_controls = []
    for path_str in clip_model.path_list:
        print(Path(path_str))
        name = str(Path(path_str).name)
        clip_controls.append(
            ft.ListTile(
                leading=ft.Icon(ft.Icons.VIDEO_FILE, color=ft.Colors.BLUE_400),
                title=ft.Text(name, size=12, weight=ft.FontWeight.W_500),
                #subtitle=ft.Text("ローカル動画", size=10),
                on_click=lambda _, p=path_str: on_clip_select(p),
                hover_color=ft.Colors.BLUE_50,
                dense=True,
            )
        )

    return ft.Column([
        ft.Container(
            content=ft.Text("切り抜き履歴", weight="bold", size=14),
            padding=ft.padding.only(left=15, top=20, bottom=5),
        ),
        ft.Divider(height=1, thickness=1),
        ft.ListView(
            expand=True,
            spacing=0,
            controls=clip_controls if clip_controls else [
                ft.Container(
                    content=ft.Text("履歴はありません", color=ft.Colors.GREY_400, size=12),
                    padding=20,
                    alignment=ft.Alignment.CENTER
                )
            ]
        )
    ], spacing=0)

def flash(
    page: ft.Page,
    message: str,
    loading: bool = False,
    color: str | None = None,
    duration: int = 2000,
):
    if loading:
        content = ft.Row(
            [
                ft.ProgressRing(width=16, height=16),
                ft.Text(
                    message,
                    style=ft.TextStyle(
                        color=ft.Colors.BLACK
                    )),
            ],
            spacing=10,
        )
        duration = 0
    else:
        content = ft.Text(
            message,
            style=ft.TextStyle(
                color=ft.Colors.BLACK
            )
        )

    snack_bar = ft.SnackBar(
        content=content,
        bgcolor=color,
        duration=duration,
    )

    page.show_dialog(snack_bar)