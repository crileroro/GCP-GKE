# pylint: disable=maybe-no-member
from helpers.helpers import print_title
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from pprint import pprint

import time

def create_k8s(body, projectId, zone, credentials):

    print_title('Creating k8s cluster')
    service = discovery.build('container', 'v1', credentials=credentials)
    request = service.projects().zones().clusters().create(projectId=projectId, zone='europe-west2-a', body=body)
    response = request.execute()

    while True:
            request = service.projects().zones().operations().get(
                projectId=projectId, 
                zone=zone, 
                operationId=response['name'])

            response = request.execute()

            if response['status'] == 'DONE':
                if 'statusMessage' in response:
                    print('  --> Error creating cluster: {}'.format(response['statusMessage']))
                else:
                    print('  --> Cluster successfully created and configured.')
                    
                return

            if 'detail' in response:
                print('  --> {}'.format(response['detail']))
            
            time.sleep(2)
