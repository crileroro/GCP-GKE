
printf '\n************************\nSet up gcloud\n************************\n'

printf '  --> Setting up project in gcloud config ...\n'
gcloud config set project k8s-cluster-shoppingapp

printf '  --> Setting up zone in gcloud config ...\n'
gcloud config set compute/zone europe-west2-a

printf '  --> Setting up Kubeconfig (Kubectl config file) to point to the proper cluster...\n'
gcloud container clusters get-credentials multi-cluster-k8s-shoppingapp

printf '\n************************\nInstall Helm3\n************************\n'
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh

printf '\n************************\nInstall Ingress-Nginx\n************************\n'
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm install my-nginx stable/nginx-ingress --set rbac.create=true



