# <img src="docs/images/superman.png" width="40" height="40"/> Agent 

# Autonomous Website Exploration and Testing
Agent, using training data from Agent-X, autonomously learns to explore a website and evaluate its actions, fields, and forms. Agents, apply abstract test flows, represented in a standard grammar, when not exploring. The executed test are capable of determining if a web page is operating in a manner consistent with learned test flow behaviors. Message queues and a coordinator support multiple distributed and concurrent agents operating on a system under test, thus enabling the rapid evaluation of new applications.

# Quickstart Guide 

### Step 1: Clone this Agent repository
```bash
git clone ssh://git@ultigit.ultimatesoftware.com:7999/aist/agent.git
cd agent
```

### Step 2: Start a local Docker Machine

See https://docs.docker.com/machine/install-machine/ and https://docs.docker.com/machine/get-started/ for instructions on installing and starting a Docker Machine.

### Step 3: Start the Agent Docker containers
```bash
docker-compose up -d
```

### Step 4: Open a terminal for viewing Agent logs
```bash
docker-compose logs -f
```

Note: The Agent system does not currently include a separate reporting capability. The Agent logs provide insight into the operation of the system's agents.


### Step 5: Open viewport and start Agent
1. Open index.html
2. Point Agent to System Under Test (SUT) URL. This automatically defaults to the PetClinic application contained in the repository.
2. Click on connect button to view Agent exploration and test of SUT.
3. Click on start button to begin exploration and test.
4. Click on stop button to stop exploration and test. Will stop 

# Documentation
* [Install](docs/install.md)
* [Get started](docs/get_started.md)
* [User Manual](docs/user_manual.md)
* [Changelog](docs/changelog.md)
* [How to contribute](docs/how_to_contribute.md)

# An Intelligent Agent Based Microservices Framework

Very brief description of the architecture. Go into a little more detail in the user manual.

# Exploring the Application

Short explanation and GIF.

# Trainable Page Analysis and Labeling

Brief overview of Agent-X and reference to GIT repository. A GIF here would be nice as well.

# Understanding Test Flows

Again ... a short simple explanation of what a test flow is and the grammar. Reference User Manual for detail.

# Autonomous Testing

Again ... a short simple explanation with GIF showing the system running through a test.

# A Research Testbed

Finish up first page with a description of project as a research testbed along with email links for people to register interest.

Reference or repeat "How to Contribute" information from user manual.