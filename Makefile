.PHONY: clean


all: .venv/bin/activate
	pip install .
	pydoku

.venv/bin/activate: requirements.txt
	@virtualenv .venv
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@. .venv/bin/activate

clean:
	@echo "Cleaning project workspace..."
	@rm -rf .venv
	@echo "Done."