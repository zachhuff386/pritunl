from pritunl.constants import *
from pritunl.event import Event
import pritunl.utils as utils
from pritunl import app_server
import time
import uuid
import flask

@app_server.app.route('/event', methods=['GET'])
@app_server.app.route('/event/<cursor>', methods=['GET'])
@app_server.auth
def event_get(cursor=None):
    if app_server.interrupt:
        return flask.abort(503)

    if not cursor:
        event = Event.get_last_row()
        if event:
            cursor = event.id

    events = []
    for event in Event.get_events(cursor):
        events.append({
            'id': event.id,
            'type': event.type,
            'resource_id': event.resource_id,
            'time': event.time,
        })

    return utils.jsonify(events)
