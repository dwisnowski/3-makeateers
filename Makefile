# Define the virtual environment directory
VENV_DIR = venv

# Define the Python executable
PYTHON = python

# Define the pip executable
PIP = $(VENV_DIR)/Scripts/pip

# Define the Flask application entry point
FLASK_APP = wsgi.py

# Create a virtual environment
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

# Install the required packages
install: $(VENV_DIR)
	$(PIP) install -r requirements.txt

# Initialize the database
init-db:
	$(VENV_DIR)/Scripts/python -c "from app import init_db; init_db()"

# Run the application
run:
	$(VENV_DIR)/Scripts/python $(FLASK_APP)

# Clean up the virtual environment
clean:
	rm -rf $(VENV_DIR)

# Phony targets
.PHONY: install init-db run clean