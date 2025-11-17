# Flask J2 Minimal

Flask J2 Minimal is a simple template based on Flask with Jinja2 templating engine.


## Getting Started

```bash
# Create the virtual env
python -m venv .venv

# Activate the virtual env
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Copy the .env.example file to .env
cp .env.example .env

# Run the migrate
python run.py --migrate

# Run the app
python run.py
```