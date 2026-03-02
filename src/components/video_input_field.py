import flet as ft
import asyncio
from pathlib import Path
from context import VideoContext
from services.video_handler import get_file_duration
from components.common_widgets import flash

@ft.component
def VideoInput():
    video_model = ft.use_context(VideoContext)
    has_video, set_has_video = ft.use_state(0)

    async def get_video_duration(page, path):
        if not path:
            return 0.0
        try:
            duration = await get_file_duration(path)
            return duration
        except Exception as e:
            flash(
                page,
                f"読み込み失敗: {str(e)}", 
                loading=False,
                color=ft.Colors.RED_50,
                duration=2000
                )
            return 0.0

    def handle_reset(e):
        video_model.update_source("", None, 0.0)

    async def handle_pick_files(e):
        files = await ft.FilePicker().pick_files(
            allow_multiple=False, 
            file_type=ft.FilePickerFileType.VIDEO
        )
        if files and files[0].path:
            video_duration = await get_video_duration(e.page, Path(files[0].path))
            video_model.update_source(Path(files[0].path), "LOCAL", video_duration)
        else:
            pass

    content = ft.Row([
        ft.OutlinedButton("ファイルを選択", icon=ft.Icons.FILE_OPEN, on_click=handle_pick_files),
        ft.OutlinedButton("選択を解除", icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.RED_400, on_click=handle_reset, disabled=not video_model.source_path),
    ], alignment=ft.MainAxisAlignment.START)

    return ft.Container(
        content=content,
        padding=0,
        height=50,
        alignment=ft.Alignment.CENTER
    )