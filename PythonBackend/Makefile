.PHONY: lint
lint:
	pycodestyle --max-line-length=120 --exclude=venv,.git,*pb2* .

.PHONY: test
test:
	py.test

.PHONY: codegen
codegen:
	python -m grpc_tools.protoc -I.. --python_out=. --grpc_python_out=. ../calc_service.proto
