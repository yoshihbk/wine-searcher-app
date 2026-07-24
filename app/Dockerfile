# ベースイメージとして軽量なPython 3.12環境を使用
FROM python:3.12-slim

# コンテナ内の作業ディレクトリを /app に設定
WORKDIR /app

# MySQL接続ライブラリとC言語のコンパイルに必要なビルドツールをインストール
# キャッシュを削除してイメージサイズを軽量化
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

# Pythonのライブラリ依存関係リストをコンテナへコピー
COPY requirements.txt .

# 必要なPythonライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリのソースコード一式をコンテナへコピー
COPY . .

# 完成したイメージからコンテナ起動時に実行するコマンド
# Pythonアプリを直接起動します
CMD ["python", "src/app.py"]