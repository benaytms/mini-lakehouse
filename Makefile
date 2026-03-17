include .env
LOCALSTACK_URL=http://localhost:4566

up:
	docker compose up -d
	cd terraform && terraform init && terraform apply
run:
	docker exec -i pgdatabase psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < database/schema.sql
	sleep 3
	docker compose run pipeline
psql:
	docker exec -it pgdatabase psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)
down:
	aws --endpoint-url=$(LOCALSTACK_URL) s3 rm s3://$(BUCKET_NAME) --recursive
	cd terraform && terraform destroy
	docker compose down