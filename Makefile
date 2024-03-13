.DEFAULT_GOAL := run

install: clean
	echo "Installing dependencies ..."
	python3.11 -m venv venv
	venv/bin/pip install -r requirements.txt

clean:
	echo "Cleaning up ..."
	rm -rf venv
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "pycache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +