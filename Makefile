# Define the virtual environment directory
VENV_DIR = venv

# Define the Python executable
PYTHON = python

# Define the pip executable
PIP = $(VENV_DIR)/Scripts/pip

# Define the Flask executable
FLASK = $(VENV_DIR)/Scripts/flask

# Define the Waitress executable
WAITRESS = $(VENV_DIR)/Scripts/waitress-serve

# Define the Flask application entry point
FLASK_APP = wsgi:app

# Create a virtual environment
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

# Install the required packages
install: $(VENV_DIR)
	$(PIP) install -r requirements.txt

# Initialize the database
init-db:
	$(VENV_DIR)/Scripts/python -c "from app import init_db; init_db()"

# Run the application with Flask development server
run:
	$(VENV_DIR)/Scripts/python -m flask run --host=0.0.0.0 --port=5000

# Run the application with Eventlet
run-eventlet:
	$(VENV_DIR)/Scripts/python wsgi.py


# Clean up the virtual environment
clean:
	rm -rf $(VENV_DIR)

# Phony targets
.PHONY: install init-db run run-eventlet clean