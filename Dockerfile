FROM debian:bookworm


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    tor && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt .

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

COPY . .

RUN echo "SocksPort 0.0.0.0:9050" >> /etc/tor/torrc


CMD ["./entrypoint.sh"]
