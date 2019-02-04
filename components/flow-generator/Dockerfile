FROM aist-tensorflow

USER root

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

COPY . /app

COPY supervisord.conf /etc/supervisord.conf

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]