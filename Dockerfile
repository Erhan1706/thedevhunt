FROM python:3.10.16

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
RUN playwright install
RUN playwright install-deps

COPY tailwindcss .
COPY static ./static
RUN chmod +x ./tailwindcss
RUN rm -f ./static/css/output.css

COPY . .
RUN ./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
RUN chmod +x ./scripts/entrypoint.sh

ENTRYPOINT ["./scripts/entrypoint.sh"] 
