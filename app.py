from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 내가 원하는 비밀번호 (6자리)
MY_PASSWORD = "230915"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pw = request.form.get('password')
        if pw == MY_PASSWORD:
            return redirect(url_for('success'))
        else:
            return render_template('index.html', error='비밀번호가 틀렸습니다.')
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)