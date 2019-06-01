from flask import Flask, render_template, redirect
from apscheduler.schedulers.blocking import BlockingScheduler
import process, model, visuals


app = Flask(__name__)


scheduler = BlockingScheduler()
scheduler.add_job(
   process.process_mains(),
   'cron',
   day_of_week='mon-fri',
   hour=9,
   minute=30, 
   end_date='2020-05-30'
   )
scheduler.start()


@app.route('/predictions')
def predict():
   return render_template('model.html')


@app.route('/live')
def live_charts():
   return render_template('live.html')


@app.route('/')
def home():
   return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)