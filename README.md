# <img src="docs/images/agent-logo-blue.png" width="40" height="40"/> AGENT

# Autonomous Website Exploration and Testing

AGENT, using training data from AGENT-X, autonomously learns to explore a website and evaluate its actions, fields, and forms. AGENT deploys one or more exploration and testing agents to explore a web application and apply test flows as testable patterns are recognized.  

Abstract test flows, represented in a standard grammar and learned from a training set, support a Long Short-Term Memory (LSTM) based flow planner capable of perceiving similar patterns in the Application Under Test (AUT). New AUT-specific, concrete test flows are constructed from LSTM generated abstract flows and intelligently formed input data populated using a Form Expert. Executed tests are capable of detecting if a web page is operating in a manner consistent with learned test flow behaviors.  

A coordinator dispatches testing assignments through a message queue and enables the  support of multiple distributed, concurrent execution and testing agents. Each agent is capable of independently interacting with the System Under Test via an instrumented Chrome client and AEON runner. This AI for Software Testing solution, designed for research and development applications, illuminates a new path for advancing the state-of-the-art in testing automation.  

** INSERT Phillip's GIF HERE **

## Quickstart Guide

### Step 1: Clone this AGENT repository

```bash
git clone ssh://git@ultigit.ultimatesoftware.com:7999/aist/agent.git
cd agent
```

### Step 2: Start a local Docker Machine

See https://docs.docker.com/machine/install-machine/ and https://docs.docker.com/machine/get-started/ for instructions on installing and starting a Docker Machine.

### Step 3: Start the AGENT Docker containers and terminal for viewing logs

```bash
docker-compose up -d
docker-compose logs -f
```

Note: The Agent system does not currently include a UI or reporting capability. The AGENT logs provide insight into the operation of the system's agents.

### Step 4: Open VNC viewport and Flower monitoring tool

```bash
open index.html
```

### Step 5: Start AGENT

Using a REST client such as [Insomnia](https://insomnia.rest) or [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en), send a POST command to the AGENT's start endpoint on the Gateway service (port 9002), `http://localhost:9002/v1/start`.

Set the POST body type to JSON, and the body data to the following:

```json
{
    "SUT_URL": "http://pet-clinic:8080"
}
```

The header Content-Type should be set to application/json.

### Step 6: Observe

In the browser window opened in Step 4, click the connect button to view the AGENT interacting with the AUT Chrome client. The Flower frame can be used to observe Celery message traffic. The log terminal opened in Step 3 can be used to observe the logs produced by the AGENT.

### Step 7: Stop the AGENT

AGENT will automatically stop after 300 iterations. However, if you would like to stop the AGENT sooner, use the REST client from Step 5 to send a POST command to the AGENT's stop endpoint, `http://localhost:9002/v1/stop`.

Set the POST body type to JSON, and the body data to an empty JSON object, `{}`. The header Content-Type should be set to application/json.

## Additional Documentation

* [Developer Install](docs/developer_install.md)
* [User Manual](docs/user_manual.md)
* [Changelog](docs/changelog.md)
* [How to contribute](docs/how_to_contribute.md)

## References

