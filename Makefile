# run tests
test:
	pytest test_main.py

# run tests on any change
continuous_test:
	ptw *.py
#	ptw main.py settings.py test_*.py


# generate coverage report as html
coverage:
	pytest test_main.py --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html

# start app in dev mode
# --host="0.0.0.0" makes the server available on all network interfaces
# --port=8000 specifies the port on which the server will listen
# --reload makes the server restart automatically when code changes

dev:
	uvicorn main:app --host="0.0.0.0" --port=8000 --reload

local_tag=startrek_ships:0.1
#remote_tag=localhost:5050/$(local_tag)
remote_tag=host.docker.internal:5050/$(local_tag)
service_name=go-web-server
image_build:	
	docker build --rm -t $(local_tag) .
image_run:
	docker run -p 1111:8001 -it $(local_tag)
image_local_tag:
	docker tag $(local_tag) $(remote_tag) 
image_push:
	docker push $(remote_tag)
image_local_delete:
	docker image rm -f $(local_tag)
create_deployment:
	kubectl create deployment startrek-ships-server --image=$(remote_tag)
createÙ_service:
	kubectl create service clusterip $(service_name) --tcp=8001:8001
delete_service:
	kubectl delete service $(service_name)
deploy_ingress:
	kubectl apply -f k3d/ingress.yaml
# kind
cluster_name="startrek-cluster"
kind_create: kind_delete
	kind create cluster --name $(cluster_name) # --config kind-config.yaml
kind_cluster_info: kind_create
	kubectl cluster-info --context $(cluster_name) #kind-startrek-cluster
kind_delete:
	kind delete cluster --name $(cluster_name) #startrek-cluster
kind_load_image:
	kind load docker-image $(remote_tag) --name startrek-cluster
test_deployment:
	kubectl apply -f fastapi-k8s-cluster/k8s/deployment.yaml #--dry-run=client
test_service:
	kubectl apply -f fastapi-k8s-cluster/k8s/service.yaml #--dry-run=client
test_ingreses:
	kubectl apply -f fastapi-k8s-cluster/k8s/ingress.yaml #--dry-run=client


