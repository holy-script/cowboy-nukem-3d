from appwrite.client import Client
from appwrite.services.functions import Functions

client = Client()

(client
 .set_endpoint('http://20.111.63.26/v1')
 .set_project('6349a6246bff99b4f66d')
 .set_key('dff24acc21322487fb6586afff8a5bfcea278cf44a69effb6e7c76b2d8afcc7de599061d44623bae34ebdb429df3863bcf9514d1c5cbc65dcc21c3c4ca3f65f7d79f6edd4212105ae0c0c69d2bfaed6d133c3123067ccfde60645ea440d691e6351c1f50c5d3597c4be4fb8e82392c69048271d4504416b23a3af952de86decc')
 )

functions = Functions(client)

inputs = {
    'email': '',
    'pwd': '',
    'otp': '',
    'phone': '',
}


def ping():
    return functions.create_execution('634a5f1de438f3bf594b')
