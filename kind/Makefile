tag="0.3"
image="startrek-ship:$(tag)"
cluster_name="my-startrek-cluster"
dockerfile="Dockerfile.startrek-ships"
pods:
	kubectl get pods -A
delete_cluster:
	kind delete cluster --name $(cluster_name)
create_cluster:
	kind create cluster --name $(cluster_name) --config kind-config.yaml
show_clusters:
	kind get clusters
build_ships:
	docker build --rm -f $(dockerfile) -t $(image) ..
load_ships:
	kind load docker-image $(image) --name $(cluster_name)
deploy_ships:
	kubectl apply -f startrek-ships-deployment.yaml 

