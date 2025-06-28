import calendar
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

MY_PASSWORD = "230915"

def get_calendar(year, events):
    """
    기본 연간 달력 생성 + 각 날짜에 일정 있는 날짜만 표시용 딕셔너리 반환
    """
    cal = calendar.HTMLCalendar(calendar.MONDAY)
    cal_html = cal.formatyear(year)
    return cal_html

def get_events():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  event TEXT)''')
    c.execute('SELECT date, event FROM events ORDER BY date')
    events = c.fetchall()
    conn.close()
    return events

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pw = request.form.get('password')
        if pw == MY_PASSWORD:
            return redirect(url_for('success'))
        else:
            return render_template('index.html', error='비밀번호가 틀렸습니다.')
    return render_template('index.html')

@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        date = request.form['date']
        event = request.form['event']
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute('INSERT INTO events (date, event) VALUES (?, ?)', (date, event))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))

    now = datetime.now()
    year = now.year
    events = get_events()
    cal_html = get_calendar(year, events)
    return render_template('success.html', calendar=cal_html, events=events, now=now)

if __name__ == '__main__':
    app.run(debug=True)