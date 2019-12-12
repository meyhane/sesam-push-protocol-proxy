import os
from flask import Flask, request, Response, abort
import requests
from sesamutils import sesam_logger
from sesamutils.flask import serve
import sys

PORT = os.getenv('PORT', 5000)

app = Flask(__name__)
logger = sesam_logger('sesam-push-protocol-proxy', app=app)
SESAM_PUSH_PROTOCOL_PARAMS = ['sequence_id', 'is_full', 'request_id', 'previous_request_id', 'is_first', 'is_last']
SERVICE_PARAMS = ['ms_url', 'ms_do_skip_empty_data', 'ms_boolean_true_at_sink', 'ms_boolean_false_at_sink'] + ['ms_'+p+'_at_sink' for p in SESAM_PUSH_PROTOCOL_PARAMS]

logger.info(f'SERVICE_PARAMS: {SERVICE_PARAMS}')


@app.route("/", methods=["POST"])
def post_data():
    try:
        url = request.args.get('ms_url')
        do_verify_ssl = request.args.get('ms_do_verify_ssl','0') == "1"
        do_skip_empty_data = request.args.get('ms_do_skip_empty_data','0') == "1"
        boolean_true_at_sink = request.args.get('ms_boolean_true_at_sink')
        boolean_false_at_sink = request.args.get('ms_boolean_true_at_sink')
        args_to_forward = dict([])
        for key, value in request.args.items():
            if key in SESAM_PUSH_PROTOCOL_PARAMS:
                if  'ms_' + key + '_at_sink' in request.args:
                    if key[0:3] == 'is_' and boolean_true_at_sink and boolean_false_at_sink:
                        value = boolean_true_at_sink if request.args.get(key) == "true" else boolean_false_at_sink
                    args_to_forward[request.args.get('ms_' + key + '_at_sink')] = value
                else:
                    args_to_forward[key] = value
                continue
            if key not in SERVICE_PARAMS:
                args_to_forward[key] = value
        if do_skip_empty_data:
            data = request.get_json()
            if data == [] or data == {}:
                return Response(response="", status=200)
        response = requests.post(url=url,  params=args_to_forward, json=request.get_json(), verify=do_verify_ssl)
        return Response(response=response, status=response.status_code)
    except Exception as e:
        exception_str = '{}, at line {}'.format(sys.exc_info()[1],sys.exc_info()[2].tb_lineno)
        logger.error(exception_str)
        return abort(500, exception_str)


if __name__ == "__main__":
    serve(app, port=PORT)
