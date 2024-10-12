FROM postgres:17

ENV POSTGRES_DB=${DATABASE_NAME}
ENV POSTGRES_USER=${DATABASE_USER}
ENV POSTGRES_PASSWORD=${DATABASE_PW}

# Copy your initialization script
COPY init_db.sh /docker-entrypoint-initdb.d/init_db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh

EXPOSE 5432
