ARG BUILD_FROM=ghcr.io/tarahome/taraassistant:latest
FROM ${BUILD_FROM}

# Switch to root for add-on compatibility
USER root

# Overlay patched files for ingress support
COPY app/config.py /app/app/config.py
COPY app/main.py /app/app/main.py
COPY app/middleware/setup_redirect.py /app/app/middleware/setup_redirect.py
COPY app/setup/routes.py /app/app/setup/routes.py

# Copy add-on entrypoint
COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
