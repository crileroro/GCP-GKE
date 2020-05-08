# pylint: disable=maybe-no-member
from googleapiclient.errors import HttpError
from helpers.helpers import print_title
from googleapiclient import discovery


def enable_billing(credentials, billing_body):
    print_title('Enabling Billing for project {}'.format(billing_body['projectId']))

    try:    
        service = discovery.build('cloudbilling', 'v1', credentials=credentials)
        request = service.projects().updateBillingInfo(name='projects/{}'.format(billing_body['projectId']), body=billing_body)
        response = request.execute()

        if response['billingEnabled']:
            print('  --> Billing successfully enabled.')

    except HttpError as error:
        print("  --> Error {}: {}".format(error.resp.status, error._get_reason()))