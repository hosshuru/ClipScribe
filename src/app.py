import flet as ft
from model import VideoModel, ClipModel
from components.video_input_field import VideoInput
from components.video_player_view import VideoDisplay
from components.transcription_view import TranscriptionView
from components.common_widgets import ClipSidebar
from context import VideoContext, ClipContext

@ft.component
def Layout():
    view_mode, set_view_mode = ft.use_state("edit")
    selected_clip, set_selected_clip = ft.use_state(None)
    nav_extended, set_nav_extended = ft.use_state(False)

    def toggle_nav(e):
        set_nav_extended(not nav_extended)

    def get_main_content():
        if view_mode == "edit":
            return ft.Column([
                VideoInput(),
                VideoDisplay(),
            ], expand=True)
        else:
            return TranscriptionView(selected_clip, on_back=lambda: set_view_mode("edit"))

    return ft.Row([
        ft.NavigationRail(
            selected_index=0 if view_mode == "edit" else 1,
            extended=False,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=80,
            group_alignment=-0.8,
            bgcolor=ft.Colors.GREEN_200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.VIDEO_SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.VIDEO_SETTINGS,
                    label="切り抜き",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.TEXT_FIELDS_OUTLINED,
                    selected_icon=ft.Icons.TEXT_FIELDS,
                    label="文字起こし",
                ),
            ],
            on_change=lambda e: set_view_mode("edit" if e.control.selected_index == 0 else "transcribe"),
        ),
        ft.VerticalDivider(width=1),
        ft.Container(
            content=get_main_content(),
            expand=30,
            padding=30,
            bgcolor=ft.Colors.WHITE,
        ),
        ft.VerticalDivider(width=1),
        ft.Container(
            content=ClipSidebar(on_clip_select=lambda clip: (set_selected_clip(clip), set_view_mode("transcribe"))),
            expand=8,
            width=250,
            bgcolor=ft.Colors.GREY_50,
        )
    ], expand=True, spacing=0)

@ft.component
def App():
    video_model, _ = ft.use_state(VideoModel())
    clip_model, _ = ft.use_state(ClipModel())

    return ClipContext(
        clip_model,
        lambda: VideoContext(
            video_model,
            Layout
        )
    )