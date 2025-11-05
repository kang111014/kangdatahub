from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import date
import json

app = Flask(__name__)

# --- 資料庫連線設定 ---
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',          # 您的資料庫主機
        user='root',               # 您的資料庫使用者名稱
        password='0000',  # 您的資料庫密碼
        database='mood_tracker'    # 您的資料庫名稱
    )
    return connection

# --- 主頁面：顯示表單、所有心情紀錄和圖表 ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # 處理表單提交
    if request.method == 'POST':
        age = request.form['age']
        mood_score = request.form['mood_score']
        nickname = request.form['nickname']
        daily_message = request.form['daily_message']
        entry_date = date.today()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO mood_entries (age, mood_score, nickname, daily_message, entry_date) VALUES (%s, %s, %s, %s, %s)',
            (age, mood_score, nickname, daily_message, entry_date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    # 獲取所有心情紀錄
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM mood_entries ORDER BY id DESC')
    entries = cursor.fetchall()
    cursor.close()
    conn.close()

    # 準備圖表數據
    chart_data = get_chart_data()

    return render_template('index.html', entries=entries, chart_data=json.dumps(chart_data))

# --- 圖表數據處理 ---
def get_chart_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 只獲取折線圖數據 (每日平均心情分數)
    cursor.execute("SELECT entry_date, AVG(mood_score) as avg_mood FROM mood_entries GROUP BY entry_date ORDER BY entry_date")
    line_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # 準備圖表數據
    chart_data = {
        'line_labels': [item['entry_date'].strftime('%Y-%m-%d') for item in line_data],
        'line_values': [float(item['avg_mood']) for item in line_data]
    }
    return chart_data

if __name__ == '__main__':
    app.run(debug=True)