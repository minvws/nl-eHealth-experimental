FROM alpine:3.12.4 AS alpine

RUN apk add bash curl python3

# dotnet dependencies:
RUN apk add icu-libs krb5-libs libgcc libintl libssl1.1 libstdc++ zlib

RUN addgroup -S euvac && \
    adduser -s /bin/bash -G euvac -S euvac && \
    (echo euvac ; echo euvac) | passwd euvac

USER euvac
WORKDIR /home/euvac
RUN curl -sSL https://dot.net/v1/dotnet-install.sh | /bin/bash /dev/stdin -c 5.0
COPY entrypoint.sh /home/euvac

USER root
# IANA 3030 -> Arepa Cas
EXPOSE 3030
ENTRYPOINT ["/bin/bash", "/home/euvac/entrypoint.sh"]

USER euvac
