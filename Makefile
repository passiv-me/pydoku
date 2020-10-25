PYTHON_SOURCES = $(shell find ./pydoku/ ./tests/ -name "*.py")

.PHONY: clean

all: .venv/bin/activate .test_report
	@pip install .
	@pydoku

.venv/bin/activate: requirements.txt
	@virtualenv .venv
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@. .venv/bin/activate

test: .test_report
.test_report: .venv/bin/activate $(PYTHON_SOURCES)
	@pytest -v --maxfail=1
	@echo "All good!" > .test_report

clean:
	@echo "Cleaning project workspace..."
	@rm -rf .venv
	@echo "Done."