# -*- coding: utf-8 -*-
from flask import Flask, request, abort, send_file
from redis import Redis
from rq import Queue
from merge import do_merge


app = Flask(__name__)
app.config.from_object('mergic_merge_config')

queue = Queue(connection=Redis())


@app.route('/request_merge_task', methods=['POST'])
def request_merge_task():
    #	skey = request.form['MERGESVR_SECRET_KEY']
    # if skey != app.config['MERGESVR_SECRET_KEY']:
    #		abort(404)

    music_id = request.form['music_id']
    plays = request.form['plays'].split(';')

    queue.enqueue(do_merge, music_id, plays)

    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3584, debug=True)
