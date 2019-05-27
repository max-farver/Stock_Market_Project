from flask import Flask, render_template, redirect
# from apscheduler.schedulers.blocking import BlockingScheduler
import process, model, visuals


app = Flask(__name__)


# def update_all():
#     process.retrieve_mains()
#     visuals.create_mains()
#     model.predict_mains()


# scheduler = BlockingScheduler()
# scheduler.add_job(update_all(), 'interval', hours=2)
# scheduler.start()


@app.route('/predictions')
def predict():
   return render_template('model.html')


@app.route('/live')
def live_charts():
   return render_template('live.html')


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()