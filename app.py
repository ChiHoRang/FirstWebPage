import calendar
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
MY_PASSWORD = "230915"

def get_calendar(year, month, events):
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    cal_html = cal.formatmonth(year, month)
    return cal_html

def get_events():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  event TEXT)''')
    c.execute('SELECT id, date, event FROM events ORDER BY date')
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
            return render_template('index.html', error='Incorrect password.')
    return render_template('index.html')

@app.route('/success', methods=['GET', 'POST'])
def success():
    # URL 파라미터에서 연도/월 가져오기
    now = datetime.now()
    year = request.args.get('year', default=now.year, type=int)
    month = request.args.get('month', default=now.month, type=int)

    if request.method == 'POST':
        date = request.form['date']
        event = request.form['event']
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute('INSERT INTO events (date, event) VALUES (?, ?)', (date, event))
        conn.commit()
        conn.close()
        return redirect(url_for('success', year=year, month=month))

    events = get_events()
    cal_html = get_calendar(year, month, events)

    # 이전/다음 달 계산
    prev_year = year
    prev_month = month - 1
    next_year = year
    next_month = month + 1

    if prev_month < 1:
        prev_month = 12
        prev_year -= 1

    if next_month > 12:
        next_month = 1
        next_year += 1

    return render_template(
        'success.html',
        calendar=cal_html,
        events=events,
        now=now,
        year=year,
        month=month,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month
    )

@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('success'))

if __name__ == '__main__':
    app.run(debug=True)
