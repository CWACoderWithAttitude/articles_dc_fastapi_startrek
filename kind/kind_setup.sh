#!/bin/sh

name="my-kind-cluster"
kind create cluster --name $name --config kind-config.yaml
kubectl get pods -A

read -n 1 -s -r -p "Press any key to continue"

kind delete cluster --name $name