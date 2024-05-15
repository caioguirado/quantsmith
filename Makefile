SHELL := /bin/bash

activate:
		@echo "Activating virtual environment..."
		. $(shell pwd)/venv/bin/activate

deactivate:
	deactivate

print:
	@echo $(shell pwd)

