from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import view.water
import os

app = Flask(__name__)


def template(title="HELLO!", text=""):
    now = datetime.datetime.now()
    time_string = now
    template_date = {
        'title': title,
        'time': time_string,
        'text': text
    }
    return template_date


@app.route("/")
def hello():
    template_data = template()
    return render_template('main.html', **template_data)


@app.route("/last_watered")
def check_last_watered():
    template_data = template(text=view.water.get_last_watered())
    return render_template('main.html', **template_data)


@app.route("/sensor")
def action():
    status = view.water.get_status()
    if status == 1:
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    template_data = template(text=message)
    return render_template('main.html', **template_data)


@app.route("/water")
def action2():
    view.water.pump_on(2, 1)
    template_data = template(text="Watered Once")
    return render_template('main.html', **template_data)


@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        template_data = template(text="Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    template_data = template(text="Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3.4 auto_water.py&")
    else:
        template_data = template(text="Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **template_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
