gcloud alpha cloud-shell scp localhost:./install_helm.sh cloudshell:~/install_helm.sh 

printf '*****************************\nSetting up gcloud, Helm3 and Ingress-Nginx\n*****************************'
gcloud alpha cloud-shell ssh --command='chmod +x ~/install_helm.sh && ./install_helm.sh'