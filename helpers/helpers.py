# pylint: disable=maybe-no-member
from oauth2client.client import GoogleCredentials
from googleapiclient.errors import HttpError
from googleapiclient import discovery
from pprint import pprint
import base64


def create_credentials():
    credentials = GoogleCredentials.get_application_default()
    return credentials


def print_title(message):
    print('\n' + '*'*len(message) + '\n' + message + '\n' + '*'*len(message))

def create_private_key_json(message, name_file):
    base64_bytes = message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    f = open(name_file, 'w+')
    f.write(message)
    f.close()


def wait_operation(serviceName, version, credentials, project_id, timeout=3600):
    service = discovery.build(serviceName=serviceName, version=version, credentials=credentials)
    limit_time = 0

    while limit_time != timeout:
        try:
            request = service.projects().get(projectId=project_id)
            response = request.execute()

            if response['lifecycleState'] == 'ACTIVE':
                print('  --> Project present and ACTIVE.')
            else: 
                print("  --> Project is in state {}".format(response['lifecycleState']))
            
            return

        except HttpError as error:
            print('  --> {}s: Code error {}. {}'.format(limit_time, error.resp.status, error._get_reason()))

        limit_time += 1

    print('  --> Project not created.')


