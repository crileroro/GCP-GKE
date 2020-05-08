# pylint: disable=maybe-no-member
from helpers.helpers import print_title, create_private_key_json
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from pprint import pprint

import time


def create_service_account(projectId, body, credentials):
    print_title('Creating new service account')
    
    service = discovery.build('iam', 'v1', credentials=credentials)
    request = service.projects().serviceAccounts().create(name='projects/' + projectId, body=body)

    try:
        request.execute()
        print('  --> Service account created successfully.')
    except HttpError as error:
        print("  --> Error {}: {}".format(error.resp.status, error._get_reason()))


def grant_role_sa(projectId, body, credentials):

    print_title('Granting roles to service account')
    print('  --> Getting current IAM policy ...')

    current_policy = get_iam_policy(projectId=projectId, credentials=credentials)
    print('  --> IAM policy retrieved successfully.')

    current_policy['bindings'].append(body)

    policy_body = {
        'policy': current_policy
    }
    
    service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
    request = service.projects().setIamPolicy(resource=projectId, body=policy_body)
    request.execute()

    print('  --> Role successfully added to the service account.')

def get_iam_policy(projectId, credentials):
    
    service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
    request = service.projects().getIamPolicy(resource=projectId)
    response = request.execute()

    return response

def create_key_sa(resource_name, credentials, name_file):
    
    print_title('Creating service account key')
    service = discovery.build('iam', 'v1', credentials=credentials)
    request = service.projects().serviceAccounts().keys().create(name=resource_name)
    response = request.execute()

    create_private_key_json(response['privateKeyData'], name_file=name_file)


    print('  --> Key created successfully. You can find it in the root directory.')


