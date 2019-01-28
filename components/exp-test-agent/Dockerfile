FROM aist-python

USER root

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN pip install -i https://test.pypi.org/simple/ aeoncloud>=0.1.4

COPY . /app

COPY supervisord.conf /etc/supervisord.conf

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]