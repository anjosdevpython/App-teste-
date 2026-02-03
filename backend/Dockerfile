FROM alpine:3.20

ARG PB_VERSION=0.22.20

RUN apk add --no-cache curl unzip bash tzdata

WORKDIR /pb

RUN curl -L -o pocketbase.zip https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip \
  && unzip pocketbase.zip \
  && rm pocketbase.zip

COPY docker-entrypoint.sh /pb/docker-entrypoint.sh
COPY pb_migrations /pb/pb_migrations
COPY seed /pb/seed

RUN chmod +x /pb/docker-entrypoint.sh

EXPOSE 8090

ENTRYPOINT ["/pb/docker-entrypoint.sh"]
