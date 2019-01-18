FROM dora-python

RUN python -m nltk.downloader wordnet
RUN pip install gunicorn
RUN pip install gevent

ENV FORM_EXPERT_PORT=80
ENV FORM_EXPERT_HOST=mongodb://1b9ca34b-0c80-4f38-8cb5-5426abfd9a32:280f86c9-65d0-48a4-a2ea-a49837ca41a1@replicaset-team-pterodactyl-0.mia.ulti.io:27017,replicaset-team-pterodactyl-1.mia.ulti.io:27017,replicaset-team-pterodactyl-2.mia.ulti.io:27017/ee65afa1-bb3c-459d-84f6-709b6784e822?ssl=true
ENV FORM_EXPERT_DATABASE=ee65afa1-bb3c-459d-84f6-709b6784e822

COPY ./formexpert /app

WORKDIR /app

EXPOSE 80

CMD ["gunicorn","-b","0.0.0.0:80","-w","3","-k","gevent","--log-file","-","--log-level","debug","--access-logfile","-","service:app"]
