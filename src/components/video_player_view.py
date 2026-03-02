import flet as ft
import flet_video as ftv
from context import VideoContext
import pathlib
import asyncio
import subprocess
from services.video_handler import get_file_duration
from components.video_widgets import LoadingView, EmptyView, VideoSpeedControl, VideoClipControl
from components.common_widgets import flash

@ft.component
def VideoDisplay():
    video_model = ft.use_context(VideoContext)
    

    is_loading, set_is_loading = ft.use_state(False)
    playback_rate, set_playback_rate = ft.use_state(1.0)
    clip_range, set_clip_range = ft.use_state((0, 60))

    video_path = pathlib.Path(video_model.source_path).as_uri() if video_model.source_path else ""

    file_picker = ft.FilePicker()

    def handle_range_change(start, end):
        if start < 0:
            start = 0

        if end >= video_model.duration:
            end = video_model.duration

        if start >= end:
            start = end

        set_clip_range((start, end))

    def change_speed(rate):
        set_playback_rate(rate)

    if not video_model.source_path:
        return EmptyView()

    if is_loading:
        return LoadingView()

    video_player = ftv.Video(
        playlist=[ftv.VideoMedia(video_path)],
        playback_rate=playback_rate,
        autoplay=True,
        show_controls=True,
        aspect_ratio=16/9,
    )

    video_speed_control = VideoSpeedControl(
        on_speed_change=change_speed,
        current_speed=playback_rate,
    )

    video_clip_control = VideoClipControl(
        on_range_change=handle_range_change,
        clip_range=clip_range
    )

    return ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=video_player, 
                expand=7,
                expand_loose=True,
                border_radius=10, 
                bgcolor="black"
            ),
            ft.Card(
                elevation=2,
                margin=0,
                expand=3,
                expand_loose=True,
                content=ft.Container(
                    padding=10, 
                    content=ft.Column([
                        video_speed_control,
                        video_clip_control,
                    ])
                ),
            )
        ]
    )