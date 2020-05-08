# Google Cloud Platform and Google Kubernetes Engine Automation

This project describes a way to automate the creation of different Google Cloud resources using [google-api-python-client](https://github.com/googleapis/google-api-python-client).

Following Google Cloud resources and actions are automatically created:

+ Creation Google Cloud Project.
+ Linking a project to a Billing account.
+ Enabling Google services, a.k.a Google APIs (i.e. `compute API`, `Kubernetes Engine API`).
+ Creation **k8s** cluster.
+ Creation service account to manage the newly created **k8s** cluster.
+ Granting new roles to the newly created service account.
+ Creation service account private key (JSON format).

## Getting started
### Prerequisites
+ Python 3.
+ `pip` package manager.
+ `virtualenv`.
+ `gcloud`.

### Installing
1. Create a new Python virtual environment.
```sh
$virtualenv python-env-gcp -p python3
```
2. Install required Python packages.
```sh 
$pip install -r requirements.txt
```
3. Enable the newly created virtual environment.
```sh
$source python-env-gcp/bin/activate
```
#### How to authenticate to use Google libraries
1. Run the following command to authenticate by using a Google account. You will have to give consent to `Google Auth Library` app.
```sh
$gcloud auth application-default login
```
After you have given consent, you can your credentials in `"~/.config/gcloud/application_default_credentials.json`.

This newly created file has the following content:
```json
     {
        "client_id": "<client_id>",
        "client_secret": "<client_secret>",
        "refresh_token": "<refresh_token>",
        "type": "authorized_user"
     }
```

`GoogleCredentials` will take care of authentication via **Oauth2**. This will search for the JSON file
named *application_default_credentials.json* in the directory described above.

#### Run Python script to create GCP resources

1. Run the Python script `create-project-k8s.py`.
```sh
$python create-project-k8s.py
```
This script will create the resources described above. Yo can find the service account private key (`sa_service-account-k8s-cluster_privatekey.json`) in the root of this project once it is created.
 


