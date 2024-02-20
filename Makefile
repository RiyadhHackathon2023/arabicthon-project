compose: docker-compose.yml
	docker compose up -d
	sleep 2
	./poststart.sh
