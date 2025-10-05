.PHONY: demo test clean

demo:
	docker-compose up -d
	@echo "Jenkins container started at http://localhost:8080"

test:
	chmod +x test/test_version_fix.sh
	./test/test_version_fix.sh

clean:
	docker-compose down -v
