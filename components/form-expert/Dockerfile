FROM aist-python

USER root

RUN apk add build-base gcc abuild binutils binutils-doc gcc-doc

COPY requirements.txt /app/

WORKDIR /app

RUN if [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; \
    then \
        echo "Windows Environment"; \
        python -m pip install -U pip; \
    else \
        echo "Not Windows Environment"; \
        pip install -U pip; \
    fi

RUN pip install -r requirements.txt

RUN python3 -m spacy download en

RUN python3 -m nltk.downloader wordnet
RUN pip install gunicorn
RUN pip install gevent

COPY src /app

EXPOSE 80

COPY supervisord.conf /etc/supervisord.conf

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]