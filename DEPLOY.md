# PDF分割・結合アプリ デプロイ手順（PythonAnywhere）

## アプリ概要

- `split_pdf_pages.py` — PDFをページごとに分割するCLIスクリプト（PDF/PNG選択可）
- `png_to_pdf.py` — 複数PNGを1つのPDFに結合するCLIスクリプト
- `app.py` — 上記2機能をWeb UIで使えるFlaskアプリ
  - `/split` — PDFアップロード→ページ分割→zipダウンロード
  - `/merge` — PNG複数アップロード→結合PDFダウンロード
- `templates/index.html` — アップロードフォーム1ページUI

使用ライブラリ: Flask, PyPDF2, PyMuPDF(`fitz`), Pillow（`requirements.txt`参照）

## GitHubリポジトリ

`split_pdf_pages/` フォルダのみを独立リポジトリとしてpush済み。

- リポジトリ: https://github.com/acky45/split-pdf-pages-app
- ブランチ: `main`
- `input/`, `output/` は `.gitignore` で除外（生成物・サンプルファイルのため）

## PythonAnywhereでの設定手順

### 1. コード取得（Bashコンソール）

```bash
git clone https://github.com/acky45/split-pdf-pages-app.git
mkvirtualenv myenv --python=python3.10
cd split-pdf-pages-app
pip install -r requirements.txt
```

### 2. Webアプリ作成（Webタブ）

1. 「Add a new web app」→ Next
2. 「Manual configuration」を選択
3. Python 3.10 を選択

### 3. WSGIファイル編集

「Web」タブ → 「WSGI configuration file」のリンクを開き、内容を以下に置き換えて保存：

```python
import sys

path = '/home/acky45/split-pdf-pages-app'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 4. Web タブの設定項目

| 項目 | 値 |
|---|---|
| Source code | `/home/acky45/split-pdf-pages-app` |
| Virtualenv | `/home/acky45/.virtualenvs/myenv` |

### 5. Reload

「Web」タブ上部の緑色「Reload acky45.pythonanywhere.com」ボタンを押して反映。

公開URL: https://acky45.pythonanywhere.com/

## 現在のステータス

WSGIファイル保存済み。Source code / Virtualenv 設定確認 → Reload待ち（最終確認中）。

## 今後の注意点（無料プラン）

- 1ヶ月に1回ログインして「Run until 1 month from today」を押さないとサイトが無効化される（次回期限: 2026-07-23）
- アップロードファイルサイズ上限は `app.py` 側に未設定 → 大きいPDFで問題が出たら `MAX_CONTENT_LENGTH` を追加検討
