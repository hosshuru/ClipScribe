import os
import asyncio
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FFMPEG_PATH = str(BASE_DIR / "bin" / "ffmpeg.exe")
FFPROBE_PATH = str(BASE_DIR / "bin" / "ffprobe.exe")
CLIP_DIR = BASE_DIR / "data" / "clips"
CLIP_DIR.mkdir(parents=True, exist_ok=True)

async def clip_local_video(input_path: str, start: float, end: float, output_path: str):
    duration = end - start
    cmd = [
        FFMPEG_PATH, "-y",
        "-loglevel", "error", # 警告レベルを上げるなら "debug" に変更
        "-ss", f"{start:.3f}", # 小数点第3位まで指定して精度を確保
        "-i", str(input_path),
        "-t", f"{duration:.3f}",
        "-c", "copy",
        str(output_path)
    ]

    print(f"Executing: {' '.join(cmd)}") # ログに出力

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        # エラーメッセージを詳細にデコード
        error_msg = stderr.decode('utf-8', errors='ignore')
        print(f"FFmpeg Error Details:\n{error_msg}") # コンソールに詳細を出す
        raise Exception(f"FFmpeg failed with code {process.returncode}. Check console for logs.")

async def get_file_duration(path: str):
    cmd = [
        FFPROBE_PATH, "-v", 
        "error", "-show_entries", 
        "format=duration", "-of", 
        "default=noprint_wrappers=1:nokey=1", 
        path
    ]
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        # 文字列を数値(float)に変換して返す
        result = stdout.decode().strip()
        return float(result) if result else 0.0
        
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0.0