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

split: venv
	./.venv/bin/python3 src/split.py $(ARGS)

train: venv
	./.venv/bin/python3 src/train.py $(ARGS)

predict: venv
	./.venv/bin/python3 src/predict.py $(ARGS)	

fclear: 
	rm -rf .venv	

act: venv
	. ./.venv/bin/activate