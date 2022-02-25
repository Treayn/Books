#!/bin/bash

helm upgrade -i books ./cicd/helm/books-app --values ./cicd/helm/books-app/values.yaml

export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services books-books-app)
export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
echo "Access your app at http://$NODE_IP:$NODE_PORT"
