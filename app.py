from flask import Flask, render_template, redirect, url_for, request
import psutil
import datetime
import view.water
import os

app = Flask(__name__, template_folder='template')
print (__name__)

def template(title="SelfPlanter", text=""):
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


@app.route("/water", methods=['GET'])
def manual_trigger():
#     import pdb; pdb.set_trace()
    cycle = request.args.get('cycle')
    try:
        if cycle.isnumeric():
            cycle = int(cycle)
            view.water.pump_on(cycle)
        else:
            view.water.pump_on()
    except():
        print("ERROR: reading request parameter")
    template_data = template(text="Watered "+str(cycle)+" times")
    return render_template('main.html', **template_data)


@app.route("/motor1", methods=['GET'])
def motor1():
    view.water.pump_on(pump_number = 1)
    template_data = template(text="Motor 1 ran")
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
            os.system("python auto_water.py&")
    else:
        template_data = template(text="Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **template_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
