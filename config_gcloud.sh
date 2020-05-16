gcloud config set project k8s-cluster-shoppingapp1
gcloud config set compute/zone europe-west2-a

gcloud alpha cloud-shell scp localhost:./install_helm.sh cloudshell:~/install_helm.sh 

printf '*****************************\nSetting up gcloud, Helm3 and Ingress-Nginx\n*****************************'
gcloud alpha cloud-shell ssh --command='chmod +x ~/install_helm.sh && ./install_helm.sh'