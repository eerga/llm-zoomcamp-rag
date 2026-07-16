start-env:
	source /workspaces/llm-zoomcamp-rag/.venv/bin/activate
	
run:
	uv run python assistant.py "$(Q)"

chat:
	uv run streamlit run app.py

network:
	docker network create monitoring 2>/dev/null || true

postgres: network
	docker run -it \
		--name course-assistant-pg \
		--network monitoring \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=course_assistant \
		-p 5432:5432 \
		-v pgdata:/var/lib/postgresql/data \
		postgres:17

start-agent:
	docker start course-assistant-pg

start-db:
	uv run python db_init.py

check-data:
	docker exec -it course-assistant-pg psql -U user -d course_assistant \
    -c "SELECT id, question, response_time, cost FROM conversations;"

query:
	uv run python db_query.py

dashboard:
	uv run streamlit run dashboard.py --server.port 8502

judge:
	uv run python judge.py

gen-data:
	uv run python generate_data.py

grafana:
	docker run -d \
    --name grafana \
    --network monitoring \
    -p 3000:3000 \
    -v grafana_data:/var/lib/grafana \
    grafana/grafana