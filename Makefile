build:
	docker build -t clusterapp .

bash:
	docker run -it -p 5004:5004 --rm --name clusterapp clusterapp bash

interactive:
	docker run -it -p 5004:5004 --rm --name clusterapp clusterapp bash /ClusterApp/run_server.sh

server:
	docker run -itd -p 5004:5004 --rm --name clusterapp clusterapp bash /ClusterApp/run_server.sh
