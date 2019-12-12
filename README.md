[![Build Status](https://travis-ci.org/sesam-community/sesam-push-protocol-proxy.svg?branch=master)](https://travis-ci.org/sesam-community/sesam-push-protocol-proxy)

# sesam-push-protocol-proxy
proxy microservice that unimplements [SESAM json push protocol](https://docs.sesam.io/json-push.html)

can be used to:
 * skip the empty batch, as sent as the last batch in a full run
 * map query parameters of SESAM json push protocol to that of sink system's


### Environment Parameters

| CONFIG_NAME        | DESCRIPTION           | IS_REQUIRED  |DEFAULT_VALUE|
| -------------------|---------------------|:------------:|:-----------:|
| LOG_LEVEL | Logging level. | no | INFO |
| PORT |  the port that the service will run on | no | 5000 |


### Query Parameters

Query parameters that the service supports can be divided into three groups as described below.

#### 1. query parameters after SESAM json push protocol
These parameters are supported due to SESAM json push protocol. Note that these parameters are sent implicitly by the SESAM.

See [SESAM json push protocol](https://docs.sesam.io/json-push.html#id1)

#### 2. query parameters after proxy service:
There are the parameters that effect the way this microservice works. They are all prefixed with "ms_".


| CONFIG_NAME        | DESCRIPTION           | IS_REQUIRED  |DEFAULT_VALUE|
| -------------------|---------------------|:------------:|:-----------:|
| ms_url | the url that the data will be forwarded to | yes | n/a |
| ms_do_verify_ssl | (true|false) flag for ssl verification on the url | no | false |
| ms_do_skip_empty_data | 0/1 flag to indicate if the requests with empty data will be skipped or not | no | 0 |
| ¹ms_sequence_id_at_sink | query param at the sink system that corresponds to 'sequence_id' param of SESAM json push protocol.| no | n/a |
| ¹ms_is_full_at_sink | query param at the sink system that corresponds to 'is_full' param of SESAM json push protocol.| no | n/a |
| ¹ms_request_id_at_sink | query param at the sink system that corresponds to 'request_id' param of SESAM json push protocol.| no | n/a |
| ¹ms_previous_request_id_at_sink | query param at the sink system that corresponds to 'previous_request_id' param of SESAM json push protocol.| no | n/a |
| ¹ms_is_first_at_sink | query param at the sink system that corresponds to 'is_first' param of SESAM json push protocol.| no | n/a |
| ¹ms_is_last_at_sink | query param at the sink system that corresponds to 'is_last' param of SESAM json push protocol.| no | n/a |
| ¹²ms_boolean_true_at_sink | the value that sink accepts as boolean 'true'. Boolean params of SESAM json push protocol will be forwarded accordingly .| no | n/a |
| ¹²ms_boolean_false_at_sink | the value that sink accepts as boolean 'false'. Boolean params of SESAM json push protocol will be forwarded accordingly. | no | n/a |

¹: effective only if SESAM json push protocol's parameter is supplied in the request
²: effective only if both ms_boolean_true_at_sink and ms_boolean_false_at_sink are specified


#### 3. query parameters after the Source system
There are the parameters that are passed over to the source system.


### An example of system config:

system:
```json
{
    "_id": "myfinalsystem",
    "type": "system:url",
    "connect_timeout": 60,
    "url_pattern": "http://myfinalsystemurl/%s"
}

```
system and pipe
```json
{
  "_id": "my-sesam-push-protocol-proxy",
  "type": "system:microservice",
  "connect_timeout": 60,
  "docker": {
    "environment": {
    },
    "image": "sesamcommunity/sesam-push-protocol-proxy:x.y.z",
    "port": 5000
  },
  "read_timeout": 7200,
}

{
  "_id": "my-pipe-id",
  "type": "pipe",
  "sink": {
    "type": "json",
    "system": "my-sesam-push-protocol-proxy",
    "url": "/?ms_do_skip_empty_data=1&ms_url=http://myfinalsystem:5000/"
  },
  "transform":  [...]
}

```
