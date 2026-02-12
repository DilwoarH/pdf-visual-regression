.PHONY: install test clean

# Variables
PYTHON = python3

# Default target
all: install

install:
	$(PYTHON) -m pip install -r requirements.txt

# Target to run tests
test: setup
	@echo "Running tests..."
	$(PYTHON) -m unittest tests/test_diff_script.py

# Target to set up test dependencies
setup:
	@echo "Setting up test environment..."
	@# Create test PDFs if they don't exist
	$(PYTHON) tests/create_test_pdfs.py

# Target to clean up generated files
clean:
	@echo "Cleaning up..."
	@rm -rf tests/test_output
	@rm -rf tests/test_pdfs
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@rm -rf diff_output
