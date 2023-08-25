from lambda_function import *
import json

body = {
    "something": "something",
}
body = json.dumps(body)
event = {
    "Records": [
        {
            "body": body
        }
    ]
}
lambda_handler(event, None)
