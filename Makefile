all:
	docker compose up -d

down:
	docker compose down

exec:
	docker exec -it python-trascendence bash

clean: 
	docker compose down --volumes
	yes | docker system prune -a
