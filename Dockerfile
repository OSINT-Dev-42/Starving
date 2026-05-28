FROM debian:bookworm


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl\
    python3 \
    python3-pip \
    tor && rm -rf /var/lib/apt/lists/*

# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.46/supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=5bcefed628e32adc08e32634db2d10e9230dbca0 \
    SUPERCRONIC=supercronic-linux-amd64

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

WORKDIR /app
COPY ./requirements.txt .

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

COPY . .
COPY crontab /etc/crontab

RUN echo "SocksPort 0.0.0.0:9050" >> /etc/tor/torrc


CMD ["./entrypoint.sh"]
