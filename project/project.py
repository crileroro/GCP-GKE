# pylint: disable=maybe-no-member
from helpers.helpers import print_title
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from pprint import pprint

import time


def create_project(project_body, credentials):

    print_title('Creating {} project'.format(project_body['projectId']))
    service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

    try:
        request = service.projects().create(body=project_body)
        request.execute()
        print('  --> Project is being created.')
    except HttpError as error:
        print("  --> Error {}: {}".format(error.resp.status, error._get_reason()))


def enable_service(service_to_enable, credentials, enable_service_body):

    for svc in service_to_enable:
        print_title('Enabling service {}.'.format(svc))

        service = discovery.build('servicemanagement', 'v1', credentials=credentials)
        request = service.services().enable(serviceName=svc, body=enable_service_body)
        response = request.execute()


        while True:
            request = service.operations().get(name=response['name'])
            response = request.execute()

            if 'done' in response and response['done']:
                print('  --> Service {} enabled successfully'.format(svc))
                break
            else:
                print('  --> Waiting for service {} to be enabled...'.format(svc))

            time.sleep(2)