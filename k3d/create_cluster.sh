#!/bin/sh
# file: create_cluster.sh

k3d cluster create mycluster \
    -p "9900:80@loadbalancer" \
    --registry-use k3d-test-app-registry:5050 \
    --registry-config registries.yaml