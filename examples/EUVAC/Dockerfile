FROM alpine:3.12.4 AS alpine

ENTRYPOINT ["/bin/bash", "/home/euvac/entrypoint.sh"]
WORKDIR /home/euvac

RUN apk add bash build-base cargo curl libffi-dev iptables libxml2-dev libxslt-dev \
            openssl openssl-dev python3 py3-pip python3-dev rust
RUN apk add -u awall

# dotnet dependencies:
RUN apk add icu-libs krb5-libs libgcc libintl libssl1.1 libstdc++ zlib

RUN pip3 install wheel
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
# rust only required for building crypto libs, can be removed from image once crypto built (requirements.txt)
RUN apk del rust
RUN rm /tmp/requirements.txt
COPY flask.json /usr/share/awall/optional/

RUN addgroup -S euvac && \
    adduser -s /bin/bash -G euvac -S euvac && \
    (echo euvac ; echo euvac) | passwd euvac

USER euvac

RUN curl -sSL https://dot.net/v1/dotnet-install.sh | /bin/bash /dev/stdin -c 5.0

COPY entrypoint.sh \
     cose_sign.py \
     cose_verify.py \
     fhir2qr.py \
     fhir_query.py \
     gen-csca-dsc.sh \
     immu_context.jsonld \
     immu_parser.py \
     min_data_set.py \
     /home/euvac/
COPY static /home/euvac/static

RUN /home/euvac/gen-csca-dsc.sh
