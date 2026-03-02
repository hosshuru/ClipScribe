import flet as ft

def TranscriptionView(clip, on_back):
    if clip is None:
        return ft.Column([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: on_back()),
            ft.Text("クリップが選択されていません。サイドバーから選択してください。")
        ])

    return ft.Column([
        ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: on_back()),
            ft.Text(f"文字起こし: {clip['name']}", size=20, weight="bold"),
        ]),
        ft.Container(
            content=ft.Column([
                ft.Text("ここに文字起こし結果が表示されます"),
                ft.ElevatedButton("文字起こし開始 (Whisper等)"),
                ft.TextField(multiline=True, min_lines=10, expand=True),
            ]),
            expand=True,
        )
    ], expand=True)