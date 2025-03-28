FROM python:3.10.16-bookworm

# Set the working directory
WORKDIR /app

RUN apt update

# Copy application files
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose the app port
EXPOSE 8501

# Check if working
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
#CMD ["streamlit", "run", "app.py"]
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
