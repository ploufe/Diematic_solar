ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8
WORKDIR /app

RUN apk add --no-cache python3 py3-pip
COPY src/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /app/requirements.txt
COPY src/*.py /app/
COPY src/conf /app/conf
COPY run.sh /run.sh
RUN mkdir -p /app/log && chmod a+x /run.sh

CMD ["/run.sh"]
