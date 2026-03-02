import flet as ft
from context import VideoContext, ClipContext
from services.video_handler import clip_local_video
from components.common_widgets import flash
from pathlib import Path
import asyncio

def VideoBaseContainer(content):
    return ft.Container(
        content=content,
        aspect_ratio=16/9,
        expand=True,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=10,
    )

def LoadingView():
    return VideoBaseContainer(
        ft.Column([
            ft.ProgressRing(),
            ft.Text("メディア情報を取得中...")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

def EmptyView():
    return VideoBaseContainer(
        ft.Text("動画を選択してください", color=ft.Colors.GREY_400)
    )

def VideoSpeedControl(
    on_speed_change,
    current_speed,
):
    video_model = ft.use_context(VideoContext)
    return ft.Row([
        ft.Icon(ft.Icons.SPEED, size=20),
        ft.Text("再生速度:"),
        *[ft.TextButton(
            f"{s}x", 
            on_click=lambda _, s=s: on_speed_change(s),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_ACCENT if s==current_speed else None,
                color=ft.Colors.WHITE if s==current_speed else ft.Colors.BLUE,
                shape=ft.RoundedRectangleBorder(radius=8),
            )) 
        for s in [0.5, 1.0, 1.5, 2.0]],
    ], alignment=ft.MainAxisAlignment.CENTER)

@ft.component
def VideoClipControl(
    on_range_change,
    clip_range
):
    video_model = ft.use_context(VideoContext)
    clip_model = ft.use_context(ClipContext)

    start_parent_sec, end_parent_sec = clip_range
    start_min, start_sec = divmod(int(clip_range[0]), 60)
    end_min, end_sec = divmod(int(clip_range[1]), 60)

    async def on_clip_click(e):
        page = e.page
        path = await ft.FilePicker().save_file(
            file_name=f"clip_{int(clip_range[0])}.mp4",
            allowed_extensions=["mp4"]
        )
        path = str(Path(path))
        if not path:
            return
        if not path.lower().endswith(".mp4"):
            path += ".mp4"

        async def process_save(path):
            try:
                flash(
                    e.page,
                    "動画を保存中...",
                    loading=True,
                    color=ft.Colors.BLUE_50,
                    duration=0
                )

                start, end = clip_range
                if video_model.source_type == "LOCAL":
                    await clip_local_video(video_model.source_path, start, end, path)
                clip_model.append_source(str(path))
                flash(
                    e.page,
                    f"✅ 保存完了！: {path}",
                    loading=False,
                    color=ft.Colors.GREEN_50,
                    duration=2000
                )
            except Exception as ex:
                flash(
                    e.page,
                f"❌ 保存失敗！: {path}",
                loading=False,
                color=ft.Colors.RED_50,
                duration=2000)

        asyncio.create_task(process_save(path))

    text_range_input = ft.Row([
        ft.Text("開始:"),
        ft.TextField(
            value=str(start_min), 
            width=40, 
            content_padding=5,
            text_align=ft.TextAlign.CENTER,
            dense=True, 
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=lambda e: on_range_change(int(e.data or 0)*60 + (int(clip_range[0])%60), clip_range[1]),
        ),
        ft.Text("分"),
        ft.TextField(
            value=str(start_sec), 
            width=40, 
            content_padding=5,
            text_align=ft.TextAlign.CENTER,
            dense=True, 
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=lambda e: on_range_change((int(clip_range[0])//60)*60 + int(e.data or 0), clip_range[1])
        ),
        ft.Text(" 〜 終了:"),
        ft.TextField(
            value=str(end_min), 
            width=40, 
            content_padding=5,
            text_align=ft.TextAlign.CENTER,
            dense=True, 
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=lambda e: on_range_change(clip_range[0], int(e.data or 0)*60 + (int(clip_range[1])%60))
        ),
        ft.Text("分"),
        ft.TextField(
            value=str(end_sec), 
            width=40, 
            content_padding=5,
            text_align=ft.TextAlign.CENTER,
            dense=True, 
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=lambda e: on_range_change(clip_range[0], (int(clip_range[1])//60)*60 + int(e.data or 0))
        ),
        ft.Text("秒"),
    ], alignment=ft.MainAxisAlignment.CENTER)

    range_slider = ft.RangeSlider(
        min=0, 
        max=max(video_model.duration, end_parent_sec, 1),
        start_value=start_parent_sec, 
        end_value=end_parent_sec,
        on_change=lambda e: on_range_change(e.control.start_value, e.control.end_value),
    )

    return ft.Container(
        padding=15,
        content=ft.Column([
            text_range_input,
            range_slider,
            ft.ElevatedButton(
                "この範囲で切り抜いて保存", 
                icon=ft.Icons.CONTENT_CUT,
                on_click=on_clip_click,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.Alignment.CENTER,
    )