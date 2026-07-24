import os
import pymysql
import sys
# 環境変数からデータベース接続情報を取得
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__,
            template_folder="/app/templates",
            static_folder="/app/static")
# app = Flask(__name__, template_folder='../src/templates')

app.secret_key = 'your_secret_key'  # CSRF保護のためのキー

# ひな形画像のパス（staticフォルダからの相対パス）
DEFAULT_IMAGE = "images/default.jpg"

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME", "wineapp")

import time
def get_db_connection():
  max_retries = 5  # [追加] 最大試行回数
  retry_interval = 3  # [追加] 待機秒数

  for i in range(max_retries):  # [変更] ループ処理に変更
        try:
            return pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD or "",
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            # [変更] 失敗時にログを出して待機
            print(f"DB接続待機中... ({i+1}/{max_retries}): {e}", file=sys.stderr)
            time.sleep(retry_interval)

        return None  # 全回数失敗した場合にNoneを返す


@app.route("/")
def index():
    # 本日の日付
    today = datetime.now().strftime("%Y年%m月%d日")
    # データベース接続の確認
    connection = get_db_connection()
    if not connection:
        return "Database Connection Failed", 500
    connection.close()
    # データベース接続が成功した場合、ホームページを表示
    return render_template("home.html", today=today)

@app.route("/wines", methods=["GET"])
def get_wines():
    q = request.args.get("q", "")
    cat = request.args.get("cat", "")
    
    connection = get_db_connection()
    if not connection:
        return "Database Connection Failed", 500
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM wines where 1=1"
            params = []
            if q:
                sql += " AND (name LIKE %s OR country LIKE %s)"
                params.extend([f"%{q}%", f"%{q}%"])
            # catが空文字ではない場合のみ追加する
            if cat is not None and cat != "":
                sql += " AND color= %s"
                params.append(cat)
            else:
                print("DEBUG: ALLが選択されたため条件を追加しませんでした", file=sys.stderr)
            cursor.execute(sql, params)
            wines = cursor.fetchall()
            for wine in wines:
                if not wine.get('label_image_url'):
                    wine['label_image_url'] = DEFAULT_IMAGE
            # 利益と利益率の計算
            for wine in wines:
                cost = wine['cost_price']
                sell = wine['selling_price']
                profit_value = sell - cost
                wine['profit'] = f"{profit_value:,}"
                wine['margin_rate'] = round(float(profit_value) / float(sell) * 100, 2) if sell > 0 else 0
        return render_template('index.html', wines=wines, search_query=q, current_color=cat, next_no=len(wines) + 1)
    finally:
        connection.close()


@app.route("/add", methods=["POST"])
def add_wine():
    def get_val(key, cast_func=None):
        val = request.form.get(key)
        if val == "" or val is None:
            return None
        return cast_func(val) if cast_func else val
    # フォームからデータを取得
    name = get_val("name")
    country = get_val("country")
    region = get_val("region")
    district = get_val("district")
    vintage = get_val("vintage", int)  # ここでint変換
    color = get_val("color")
    quantity = get_val("quantity", int)
    cost_price = get_val("cost_price", int)
    selling_price = get_val("selling_price", int)
    description = get_val("description")
    grape_variety = get_val("grape_variety")
    pairing = get_val("pairing")
    label_image = get_val("label_image")
    if not label_image:
        label_image = DEFAULT_IMAGE

    
    if not name or not country or not color or quantity is None or cost_price is None or selling_price is None:
        flash("銘柄、産地、カテゴリ、在庫数、仕入れ値、売値は必須です。", "danger")
        return redirect(url_for('get_wines'))
        
    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            # データベースには、取れなかった値は None として入る
            sql = """INSERT INTO wines (name, country, region, district, vintage, color, quantity, cost_price, selling_price, description, grape_variety, pairing, label_image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (name, country, region, district, vintage, color, quantity,cost_price, selling_price, description, grape_variety, pairing, label_image))
        connection.commit()
        connection.close()

    flash("ワインを追加しました。", "success")
    return redirect(url_for('get_wines'))


@app.route("/edit/<int:wine_id>", methods=["POST"])
def edit_wine(wine_id):
    # フォームから取得し、空文字ならNoneにする（整数カラム用）
    def get_val(key, cast_func=None):
        val = request.form.get(key)
        if val == '':
            return None
        return cast_func(val) if cast_func else val

    name = get_val("name")
    country = get_val("country")
    region = get_val("region")
    district = get_val("district")
    vintage = get_val("vintage", int)  # 空ならNone、そうでなければint変換
    color = get_val("color")
    quantity = get_val("quantity", int)
    cost_price = get_val("cost_price", int)
    selling_price = get_val("selling_price", int)
    description = get_val("description")
    grape_variety = get_val("grape_variety")
    pairing = get_val("pairing")
    label_image = get_val("label_image_url")
    if not label_image:
        label_image = DEFAULT_IMAGE

    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            sql = """UPDATE wines SET name=%s, country=%s, region=%s, district=%s, vintage=%s, color=%s, quantity=%s, cost_price=%s, selling_price=%s, description=%s, grape_variety=%s, pairing=%s, label_image_url=%s WHERE id=%s"""
            cursor.execute(sql, (name, country, region, district, vintage, color,quantity, cost_price, selling_price, description, grape_variety, pairing, label_image, wine_id))
        connection.commit()
        connection.close()
    return redirect(url_for('confirm_update'))


@app.route("/confirm_update")
def confirm_update():
    return '''
    <div style="text-align:center; padding:50px; font-family:sans-serif;">
        <h1>更新完了</h1>
        <p>ワイン情報を更新しました。</p>
        <br>
        <a href="/wines" style="padding:10px 20px; background:#4CAF50; color:white; text-decoration:none; border-radius:5px;">一覧に戻る</a>
    </div>
    '''

# 新規追加：編集ページを表示する関数
@app.route("/edit_page/<int:wine_id>")
def edit_page(wine_id):
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM wines WHERE id = %s", (wine_id,))
                wine = cursor.fetchone()
                if wine and not wine.get('label_image_url'):
                    wine['label_image_url'] = DEFAULT_IMAGE
                
            connection.close()
            return render_template('edit.html', wine=wine)
        except Exception as e:
            print(f"Error: {e}")
            return "データの取得中にエラーが発生しました", 500
    else:
        return "データベース接続に失敗しました", 500
    

@app.route("/wine/<int:wine_id>")
def wine_detail(wine_id):
    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM wines WHERE id = %s", (wine_id,))
            wine = cursor.fetchone()
            if wine and not wine.get('label_image_url'):
                wine['label_image_url'] = DEFAULT_IMAGE
        connection.close()
        # ここで detail.html を呼び出します
        return render_template('detail.html', wine=wine)
    return "DB接続エラー", 500


@app.route("/delete/<int:wine_id>", methods=["POST"])
def delete_wine(wine_id):
    connection = get_db_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM wines WHERE id = %s", (wine_id,))
        connection.commit()
        connection.close()
    flash(f"ID {wine_id} のワインが削除されました。", "success")
    return render_template('deleted.html', wine_id=wine_id)  
    # 削除後のページを表示するために、削除されたワインのIDを渡してテンプレートをレンダリングします.



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
