FROM python:3.10.16

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY tailwindcss .
COPY static ./static
RUN chmod +x ./tailwindcss
RUN ./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

COPY . .
RUN chmod +x ./scripts/entrypoint.sh

ENTRYPOINT ["./scripts/entrypoint.sh"] 
