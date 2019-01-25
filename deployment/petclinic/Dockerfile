FROM aist.python3

#install maven and git to build project
RUN apt-get update && apt-get install -y wget git-core maven

# Pull petclinic
RUN git clone https://github.com/spring-projects/spring-petclinic.git /spring-petclinic

# Build petclinic
WORKDIR /spring-petclinic

RUN cd /spring-petclinic && ./mvnw package

COPY Deployment/petclinic/core_nginx.conf /etc/nginx/nginx.conf
COPY Deployment/petclinic/nginx.conf /etc/nginx/conf.d/
COPY Deployment/petclinic/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PATH /bin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/sbin

CMD export uri="\$uri" \
    export http_upgrade="\$http_upgrade" \
    && envsubst < /etc/nginx/conf.d/nginx.conf > subst_ \
    && cat subst_ \
    && cp subst_ /etc/nginx/conf.d/nginx.conf \
    && /usr/bin/supervisord