VENV_DIR ?= .venv
PYTHON ?= python3
PIP := $(VENV_DIR)/bin/pip

.PHONY: venv syntax-check check encrypt-vault deploy deploy-pass task

venv:
	@if [ ! -x "$(PIP)" ]; then \
		$(PYTHON) -m venv "$(VENV_DIR)"; \
		"$(PIP)" install --upgrade pip; \
		"$(PIP)" install -r requirements.txt; \
	fi

all: venv
	./.venv/bin/python3 src/main.py $(ARGS)

m100000: venv
	./.venv/bin/python3 src/main.py -m model/model_100000.json -l 0 -c 1000

m1: venv
	./.venv/bin/python3 src/main.py -m model/model_1.json -l 0


fclear: 
	rm -rf .venv	

act: venv
	. ./.venv/bin/activate