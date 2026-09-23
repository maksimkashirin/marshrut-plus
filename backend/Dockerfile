FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        openssl \
    && rm -rf /var/lib/apt/lists/*

COPY certs /tmp/mincifra-certs

RUN set -eux; \
    mkdir -p /usr/local/share/ca-certificates; \
    for f in /tmp/mincifra-certs/*; do \
        name="$(basename "$f")"; \
        name="${name%.*}"; \
        if openssl x509 \
            -inform DER \
            -in "$f" \
            -out "/usr/local/share/ca-certificates/${name}.crt" \
            2>/dev/null; \
        then \
            echo "Converted DER certificate: $f"; \
        else \
            openssl x509 \
                -in "$f" \
                -out "/usr/local/share/ca-certificates/${name}.crt"; \
        fi; \
    done; \
    update-ca-certificates; \
    rm -rf /tmp/mincifra-certs

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]