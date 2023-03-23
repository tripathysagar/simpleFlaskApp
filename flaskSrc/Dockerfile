FROM python:3.11-slim


# Add source code
WORKDIR /app

# Install requirements
COPY . .
RUN pip install -r requirements.txt




# Set environment variables
#ENV FLASK_APP=app.py

# Run
#ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]

#ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]
