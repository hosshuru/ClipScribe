# ClipScribe 🎞️

動画の切り抜き・文字起こし支援ツールです。
言語はPython、GUIはFletを使用し、`FFmpeg` `FFprobe`の外部呼出しによって動画を操作します。
ローカルでの音声解析（文字起こし等）機能も統合予定です。
本アプリケーションは**開発中です。**

---

## ✨ 主な機能

- **動画のプレビュー**: 操作画面で切り抜き・文字起こし対象の動画を閲覧できます。
- **直感的なレンジ選択**: スライダーを使用して、抽出したい範囲（開始/終了時間）をで正確に指定。
- **切り抜き**: `FFmpeg` を使用し、高品質な切り抜きを実現。
- **切り抜き履歴**: 処理したローカルメディアを自動記録。文字起こし等にスムーズに移行できます。
---

## 🛠 技術スタック

| カテゴリ | 使用技術 |
| :--- | :--- |
| **Language** | Python 3.12+ |
| **GUI Framework** | [Flet](https://flet.dev/) (Flutter based) |
| **Core Engine** | [FFmpeg・FFprobe](https://ffmpeg.org/) |
| **Package Manager** | [uv](https://github.com/astral-sh/uv) |

---

## 🚀 セットアップ

### 1. 依存ソフトウェア
このツールはメディア処理と内部プロセスの実行に `FFmpeg`を使用します。実行前に以下の準備をお願いします。

- **FFmpeg**
  - [FFmpeg 公式サイト](https://ffmpeg.org/download.html) 等から OS に合わせたバイナリをダウンロードします。
  - プロジェクト内の `bin/ffmpeg.exe` に実行ファイルを配置してください。

### 2. 環境構築
`uv` を使用して、一瞬で独立した環境を構築できます。

```bash
# リポジトリのクローン
git clone [https://github.com/hosshuru/media-extractor-gui.git](https://github.com/hosshuru/media-extractor-gui.git)
cd media-extractor-gui

# 依存関係の同期
uv sync
```

---

## 💻 使い方
```bash
uv run src/main.py
```
- 動画選択: 切り抜き・文字起こしする動画を選択。
- 範囲指定: プレビュー下のスライダー、または数値入力で開始・終了時間を設定。
- 切り抜き: 「この範囲で切り抜いて保存」をクリック。画面下部のバーが進捗をお知らせします。
- 切り抜き履歴: 右サイドバーの「切り抜き履歴」から切り抜いた動画を確認、文字起こしへの移行が可能です。

---

## ⚖️ 免責事項とライセンス (Disclaimer & Licenses)

### ソフトウェア・ライセンス
- **本ツール**: [MIT License](LICENSE)
- **FFmpeg**: [LGPL v2.1 / GPL v2~](https://ffmpeg.org/legal.html)
    - 本ツールは FFmpeg プロジェクトのライブラリ（バイナリ）を外部呼出しにて使用しています。
    - 作者は FFmpeg のコードを所有しておらず、FFmpeg の著作権は [FFmpeg プロジェクト](https://ffmpeg.org) に帰属します。
- **flet**: [Apache 2.0 License](https://github.com/flet-dev/flet/blob/main/LICENSE)

### 免責事項
- 本ツールは、ユーザーが正当な権利を持つコンテンツ（自身の配信動画のバックアップ等）や、オープンライセンス（パブリックドメイン等）のメディアを処理・アーカイブすることを目的として開発されています。
- 各配信サイトの利用規約や著作権法を遵守し、ユーザー自身の責任においてご利用ください。
- 本ツールの利用により生じたいかなる損害や法的なトラブルについても、開発者は一切の責任を負いません。
---