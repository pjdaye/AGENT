# Setup
```bash
docker-compose up --build
```

# Push Updates
```bash
# Build the docker image for the Ulti docker registery.
docker build -t docker.mia.ulti.io/aist/form-expert .

# Push to registry
docker login docker.mia.ulti.io
docker push docker.mia.ulti.io/aist/form-expert:latest

# Push to PCF
cf login
cf push form-expert --docker-image docker.mia.ulti.io/aist/form-expert
```