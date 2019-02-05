# Developer Installation Instructions

**Step 1:** Clone this AGENT repository

**Step 2:** Create a Python 3.6 virtual environment (or Conda Environment)

**Step 3:** Install docker-machine if not already installed

See https://docs.docker.com/machine/install-machine/ and https://docs.docker.com/machine/get-started/ for instructions on installing and starting a Docker Machine, or Windows equivalent for your environment.

**Step 4:** Activate the virtual environment 

**Step 5:** Build the common and base images

Open a bash terminal (Mac OS X) or Windows 10 command window (cmd.exe) and execute the following commands.

```bash
./build_common.sh
./build_base_images.sh
```

**Step 6:** Run docker-compose

```bash
docker-compose -f docker-compose-dev.yml up --force-recreate --build
```

Note: To run two or five distributed Exploration and Test Agents, change `docker-compose-dev.yml` to `docker-compose-2agents.yml` or `docker-compose-5agents.yml`.

**Step 7** Start the AGENT Docker containers and terminal for viewing logs

```bash
docker-compose up -d
docker-compose logs -f
```

Note: The Agent system does not currently include a UI or reporting capability. The AGENT logs provide insight into the operation of the system's agents.

**Step 7** Open VNC viewport and Flower monitoring tool

```bash
open index.html
```

Alternatively to view the Flower - Celery monitor, open `http://localhost:5555` to view Flower. Wait until both agents are connected and online to ensure that AGENT is running for the VNC viewer to connect.

Alternatively the VNC viewer can be opened in its own window. Open `http://localhost:8001/vnc.html` and `Connect` to view the runner screen. Note: when running with multiple Exploration and Test Agents and their associated runners, port 8001 views the 1st runner, 8002 the second, and so on.

**Step 8** Start AGENT

Using a REST client such as [Insomnia](https://insomnia.rest) or [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en), send a POST command to the AGENT's start endpoint on the Gateway service (port 9002), `http://localhost:9002/v1/start`.

Set the POST body type to JSON, and the body data to the following:

```json
{
    "SUT_URL": "http://pet-clinic:8080"
}
```

The header Content-Type should be set to application/json.

**Step 9:** Observe

**Step 10:** Stop the AGENT

AGENT will automatically stop after 300 iterations. However, if you would like to stop the AGENT sooner, use the REST client from Step 5 to send a POST command to the AGENT's stop endpoint, `http://localhost:9002/v1/stop`.

Set the POST body type to JSON, and the body data to an empty JSON object, `{}`. The header Content-Type should be set to application/json.
