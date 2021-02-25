FROM python:alpine3.8
COPY . /app
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt git && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && rm -rf requirements.txt
EXPOSE 6543

ENTRYPOINT [ "python" ]

CMD [ "moviemeter.py" ]
