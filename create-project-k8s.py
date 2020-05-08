# pylint: disable=maybe-no-member
from googleapiclient import discovery
from googleapiclient.errors import HttpError

from helpers.helpers import create_credentials, print_title, wait_operation
from project.project import create_project, enable_service
from project.project_admin import enable_billing
from container_api.kubernetes import create_k8s
from iam.service_account import create_service_account, grant_role_sa, get_iam_policy, create_key_sa

project_body = {
        'projectId': 'k8s-cluster-shoppingapp',
        'name': 'prd-shopping-app',
        'labels': {
        'type-project': 'k8s-cluster',
        'app': 'shopping-app'
        }
    }

billing_body = {
    'projectId': project_body['projectId'],
    'billingAccountName': 'billingAccounts/01C45D-21C242-BD0FAB',
    'billingEnabled': True,
    'name': 'projects/{}/billingInfo'.format(project_body['projectId'])

}

enable_service_body = {
    'consumerId': 'project:{}'.format(project_body['projectId'])
}


k8s_body = {
  'parent': 'projects/{}/locations/europe-west2-a'.format(project_body['projectId']),
  'cluster': {
    'name': 'multi-cluster-k8s-shoppingapp',
    'masterAuth': {
      'clientCertificateConfig': {}
    },
    'network': 'projects/k8s-cluster-shoppingapp/global/networks/default',
    'addonsConfig': {
      'httpLoadBalancing': {},
      'horizontalPodAutoscaling': {},
      'kubernetesDashboard': {
        'disabled': 'true'
      }
    },
    'subnetwork': 'projects/k8s-cluster-shoppingapp/regions/europe-west2/subnetworks/default',
    'nodePools': [
      {
        'name': 'node-pool-1',
        'config': {
          'machineType': 'n1-standard-1',
          'diskSizeGb': 100,
          'oauthScopes': [
            'https://www.googleapis.com/auth/devstorage.read_only',
            'https://www.googleapis.com/auth/logging.write',
            'https://www.googleapis.com/auth/monitoring',
            'https://www.googleapis.com/auth/servicecontrol',
            'https://www.googleapis.com/auth/service.management.readonly',
            'https://www.googleapis.com/auth/trace.append'
          ],
          'metadata': {
            'disable-legacy-endpoints': 'true'
          },
          'imageType': 'COS_CONTAINERD',
          'labels': {
            'node': 'shopping-app'
          },
          'diskType': 'pd-standard'
        },
        'initialNodeCount': 3,
        'autoscaling': {},
        'management': {
          'autoUpgrade': 'true',
          'autoRepair': 'true'
        },
        'version': '1.14.10-gke.27'
      }
    ],
    'resourceLabels': {
      'cluster-type': 'test-shoppingapp'
    },
    'networkPolicy': {},
    'ipAllocationPolicy': {
      'useIpAliases': 'true'
    },
    'masterAuthorizedNetworksConfig': {},
    'defaultMaxPodsConstraint': {
      'maxPodsPerNode': '110'
    },
    'authenticatorGroupsConfig': {},
    'privateClusterConfig': {},
    'databaseEncryption': {
      'state': 'DECRYPTED'
    },
    'initialClusterVersion': '1.14.10-gke.27',
    'location': 'europe-west2-a'
  }
}

service_account_body = {
    'serviceAccount': {
        'displayName': 'service-account-k8s-cluster',
        'description': 'This service account is used to manage the newly created k8s cluster.',
    },
    'accountId': 'service-account-k8s-cluster'
}


grant_role_sa_body = {'members': ['serviceAccount:{}@{}.iam.gserviceaccount.com'.format(
                                  service_account_body['serviceAccount']['displayName'], 
                                  project_body['projectId']
                                  )
                                  ], 
                      'role': 'roles/container.admin'}
 

service_to_enable = ['compute', 'container']

private_key_json = 'sa_{}_privatekey.json'.format(service_account_body['serviceAccount']['displayName'])

if __name__ == '__main__':

    credentials = create_credentials()
    create_project(project_body, credentials)
    wait_operation('cloudresourcemanager', 'v1', credentials, project_body['projectId'], 5)

    enable_billing(credentials, billing_body)
    enable_service(service_to_enable, credentials, enable_service_body)

    create_k8s(body=k8s_body, projectId=project_body['projectId'], zone=k8s_body['cluster']['location'], credentials=credentials)

    # create_service_account(projectId=project_body['projectId'], body=service_account_body, credentials=credentials)
    # grant_role_sa(projectId=project_body['projectId'], body=grant_role_sa_body, credentials=credentials)
    # create_key_sa(resource_name='projects/-/serviceAccounts/{}@{}.iam.gserviceaccount.com'.format(
    #                               service_account_body['serviceAccount']['displayName'], 
    #                               project_body['projectId']), 
    #                               credentials=credentials,
    #                               name_file=private_key_json)
    