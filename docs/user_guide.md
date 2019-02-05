# Autonomous Generation and Exploration System (Agent) and Agent-X User's Guide

## Overview

Agent, and its associated Chrome plug-in classification tool, Agent-X, support the autonomous exploration and testing of web applications. The system learns to classify and build the *abstract* page and abstract test flows necessary to cross-site application. Three design elements are particularly important to this capability:  

1. A trainable classifier capable of perceiving abstract application states,  
2. A language specification and grammar that can be used to describe test flows, and  
3. A trainable test flow generation model capable of generating test cases from learned human testing behavior.  

These elements synergistically abstract away many of the exploration and testing problems resulting from the use of concrete page representations, selectors, and test flows. They permit an Agent to efficiently perceive the Application Under Test in sufficient detail to plan exploration and testing actions while minimizing or avoiding state explosion issues and test brittleness.  

The Agent and Agent-X applications are intended for use in research activities and as a testbed for further development and experimentation. While the application's components and functional flows have been tested with the included PetClinic Web application, the application is not intended for production testing or for testing against production systems. The descriptions and observations of Agent and Agent-X's performance characteristics are limited to the analyses done to date on the PetClinic application, see References.  

### Trainable Classifiers

Trainable page classifiers abstract detailed page information while detecting the critical inherent features necessary to their understanding. Using multiple, diverse extracted features, the page analysis classifiers extend the abstract page representation to include inferred features that may otherwise be difficult to deterministically calculate. These inferred features include page titles, labels candidates, error messages, commits and cancels. While these elements are all items that are relatively easy for humans to reliably classify, each presents classic algorithms based on DOM structure or visual presentation alone with problems that detrimentally impact accuracy, precision, recall, and specificity. By training across a diverse set of web pages and applications, and using an appropriately broad and independent set of feature vectors, Agent is able to provide for the effective abstract modeling of a page and its features.  

### Page and Test Flow Abstraction

Perhaps as importantly, Agent's classifiers analyze pages in terms of their abstracted content so that the results are divorced from field specific data including the actual title, the string value of a text field, or the DOM positioning of a commit within, or external to, a form. Without the ability to classify such features at an abstract level, learning from the labeled pages of one application could not be effectively applied to the perception of pages in a separate application. Further, if the Agent lacked the ability to appropriately abstract the page state, the system may not be able to detect if a given path had been explored sufficiently, or if a given test flow had been executed correctly. Agent's abstract page representation, or abstract state, provides a point on which widgets and flows can be organized. If an abstraction obscures features important to planing, important detail necessary to exploration and testing may be lost. Conversely, if too much detail is retained, state and test explosions may slow system discovery and inhibit test coverage determinations.  

### Trainable Test Flow Generation

While abstract representations of web elements and pages may be sufficient to support site exploration, test planning and execution requires an equally abstract understanding to enable learning and robust cross-site application. Fundamental to Agent's design is its test flow language specification and grammar. Agent abstract test flows capture the necessary conceptions of positive and negative testing, observation, and actions while filtering out brittle features that are difficult to learn. Please see the references for additional information.  

### Agent-X

Agent-X is a Chrome extension used to supplement the Agent system. It allows users to run machine learning page classification models and visualize the prediction results within live webpages. The machine learning classification models are hosted within the Page Analysis Service.  

The extension additionally provides a mechanism for interactively labeling trainable features within a live webpage. The results of labeling may be exported to the Page Analysis Service, which will use the new labeling to update its macine-learning classifiers in real-time. The effect of the updated classifiers may then be viewed within the Agent-X extension.

## Architecture

## Pet Clinic

PetClinic demonstrates the use of a Spring Boot with Spring MVC and Spring Data. While the testing of Spring functionality is not the purpose of this project, the PetClinic has an old history on the web and is well established within the community. In addition, the PetClinic application supports the primary form and action features the Agent is intended to explore and test. The PetClinic implements the following use cases:  

* View a list of veterinarians and their specialties  
* View information pertaining to a pet owner  
* Update the information pertaining to a pet owner  
* Add a new pet owner to the system  
* View information pertaining to a pet  
* Update the information pertaining to a pet  
* Add a new pet to the system  
* View information pertaining to a pet's visitation history  
* Add information pertaining to a visit to the pet's visitation history  

![PetClinic Home Page](https://deors.files.wordpress.com/2012/04/petclinic1.png)

A dockerized version of the clinic is instantiated as the test Application Under Test.

The performance and capabilities of the Agent system have not been tested and validated on web applications other than Petclinic. Please use with appropriate caution. The system is not recommended for use on production systems.  

## Components

### Exploration and Test Agent

Interacting with a multiple agent, distributed control flow determined by the Coordinator, one or more Exploration and Test Agents _Observe_ the System Under Test, _Plan_ a next action or test flow, and _Act_ to implement that plan. The Exploration and Test Agents are externally controlled through an Celery Distributed Task Queue. After receiving a start command, an Agent Loop is setup to iterate through the agents Observe, Plan and Act process. The Exploaration and Test Agent receives external test flows emitted from other agent instances as deduped and distributed by the Coordinator.

To accomplish its tasks, the Agent Loop relies on other internal objects and component micro-services to execute specific elements of its Observe, Plan and Act functionality.

The RunnerClient, via an AEON runner, _observes_ the System Under Test (SUT) and generates concrete states (scrapes) of the SUT after each action. This information is observed and analyzed further with the aid of the StateAbstracter, LabelExtraction, StateObserver and PageAnalysisClient objects. The PageAnalysisClient interacts with the Page Analyzer Service to obtain its results. 

The FlowGeneratorClient, via the Flow Generator service, and SequenceParser support the _planning_ of abstract flows. The FormExpertClient, using the Form Expert Service, provides for the determination of appropriate form field data as abstract steps or actions are converted into concrete executable actions on the SUT.

The Exploration and Test Agent's FlowExecutor is responsible for _Acting_ given an initial state, a concrete test flow, and a link to the RunnerClient. Alternative the Agent Loop iteraction method calculates a next exploratory action, with the support of the Form Expert, and commands the AEON runner via the RunnerClient.

An interface to the Celery Distributed Task Queue is provided for within the agent_celery, inbound_tasks, and outbound_tasks modules. Starting and stopping the Exploration and Test Agents is accomplished through these interfaces through messages initiated by the Gateway services.

Agent, priority, and celery thread-safe memory is supported provided by their respective memory modules.

A DefectReporter currently captures identified defects; however, the reporting of these defects is still a work in progress. Currently, the actions (success or failure) of the Exploration and Test Agent can be monitored through the terminal logs.

#### Abstraction

In order to successfully navigate through the System Under Test and avoid unnecessary duplication of tasks, scraped _concrete states_ must be appropriately abstracted. Theoretically, multiple approaches to state abstraction are not only possible, but appropriate, as the state abstraction methodology directly impacts the mechanics of exploration and the type of test flows which the system can detect. For this implementation, the Exploration and Testing Agent compares actionable widgets.

#### *Actionable State*

A class that represents a page state of the System Under Test as a collection of widgets. The hash for an actionable state only depends on the actionable widgets on a page. The hash is used to determine unique abstract states.

A widget is typically a graphical element of the user interface. Programatically, a widget is a representation of an atomic HTML DOM node excluding VirtualTextNodes. An abstract widget is a set of name-value pairs.  Two abstract widgets are distinguished by having either a different value for at least one name-value pair, an additional name-value pair, or the absence of a pair.   While a Value Instantiated widget may have many attributes, a few are selected as identifying attributes.  For example, a text field widget may have an *id* field, an *enabled* field, and a *text_value* field.  The *id*/*enabled* pair may be chosen as the identifier that uniquely identifies this widget as distinct from other widgets on the page and from a widget with the same *id* but a different *enabled* value.

#### *State Abstracter*

Converts a concrete state into an abstract state representation in order to control state explosion.

#### Clients

The Exploration and Test Agent interfaces with the Flow Generation service, the Form Expert service and the Page Analysis service and Aeon runner service through clients. These clients communicate with their respective services through REST APIs for each of the host services.

#### *Flow Generation Client*

The Flow Generator Client communicates with the Flow Generation Service, generate_flow method, to generate an abstract test flow given a precondition. A precondition is the natural language string format of an  Observation (e.g. "Observe TextBox"). When POST to the Flow Generator Service, this example observation is first converted to its equivalent JSON , \["Observe", "TextBox"\].  

##### `Flow Generation API`

---
**Client method:** generate_flow  
**Flow Generator method:** predict  
**URL accessed**: \[FLOW_GENERATION_URL\]  
**REST method:** POST  
**Client method:** generate_flow  
**Endpoint accesssed:** /v1/predict  
**Summary:** Generate a list of potential Test Flows  
**Request Body:**  

```json
[observation_word_1, observation_word_2, ... observation_word_n]
```

**Return Body:**  

```python
if index(observation_word_n) < max_length:
```

```json
[observation_word_1, observation_word_2, ... predicted_observation_word_m]
```

where index(predicted_observation_word_m) > index(observation_word_n)

```python
else:
```

```json
[]
```

---

#### F*orm Expert Client*

The Exploration and Test Agent uses the Form Expert Service to generate suggested field input values given widget labels. For a test flow, the agent uses the get_concrete_values method to suggest inputs for all widgets within a list based on the widget labels. The client submits a list of widget labels and label_keys (corresponding to Form Expert label ids) to the Form Expert Service. When exploring, the agent queries the Form Expert Service one actionable widget at a time using same Form Expert Service request. The Form Expert Service returns a dictionary of widget label_keys paired with their suggested input values. If the Form Expert Service does not return a value for a given label, the client uses the fallback method to provide suggested form input data. The client sets the widget values according to their suggested values and returns the widget list.

##### `Form Expert API`

---
**Client Methods:** get_concrete_values and get_concrete_value  
**Form Expert controller mapped method:** fill_form  
**URL accessed:** \[FORM_EXPERT_URL\] 
**REST method:** POST   
**Endpoint accessed:** /api/v1/fill_form  
**Summary:** Provides suggested input values for the provided widgets based on their label information.  
**Request Body:**  

```json
[
  {
    'label': w['label'],
    'id': w['label_key']
  } for w in widgets
]
```

---

#### *Page Analysis Client*

The Page Analysis Client communicates with the Page Analysis Service, page_analysis method, to analyze a concrete state (page) scraped from the System Under Test (SUT). The Page Analysis Service runs machine learning classifiers on the supplied concrete state to classify various elements of the page to include:

* Page Titles
* Label Candidates
* Error Messages
* Commits
* Cancels

This data is returned as a JSON dictionary of lists with one list per element type.

##### `Page Analysis API`

---
**Client Method:** run_analysis  
**Page Analysis method:** page_analysis  
**URL accessed:** \[PAGE_ANALYSIS_URL\]
**REST method:** POST  
**Endpoint accessed:** /v1/pageAnalysis/state/concrete  
**Summary:** Classifies inferred concrete state (page) elements.  
**Request Body:**  

```json
[
  {
    'label': w['label'],
    'id': w['label_key']
  } for w in widgets
]
```

---

#### *Runner Client*

Aeon wraps Selenium to provide a flexible, scalable framework for the low-level testing of web-applications. The Runner Client communicates with, and provides the capabilites of, the Aeon Runner service. The following Runner Client services access the Aeon Runner Services via the aeoncloud library to effect or obtain their result.

##### `Launch`

The client `launch` method is called when the Exploration and Test Agent starts the Agent Loop. It communicates with the Aeon Runner Service to launch an aeon session and navigate to the System Under Test (SUT) URL. The method takes one parameter, the SUT URL. It returns true if successful. Other methods, use the established aeon session to communicate with the Aeon Runner Service.

##### `Navigate`

The client `navigate` method runs the Aeon session `execute_command('GoToUrlCommand', [url])` to navigate or re-navigate to the start page of the Application Under Test. It may be used at the end of the client launch method, or it may be used if the Exploration and Test Agent ends up on a page with no actionable widgets. The method takes one parameter, the SUT URL. It returns true if successful.

##### `Perform Action`

The client `perform_action` method performs either a click or set on the AUT via the Aeon Service. The client method accepts three parameters, an element selector, the action, and the value that the element is to be set to in the case of a 'set' action. For click actions, the client runs the Aeon session `execute_command('ClickCommand', [css, "Text", value])`, where the value (in the case of click action) is ignored. The css variable for this command and the next described command, is defined as the dictionary, `css = {'type': 'jQuery', 'value': selector}`. jQuery selectors are required. For set actions, the client runs the Aeon session `execute_command('SetCommand', [css, "Text", value])`. In this case the value of the element pointed to by the jQuery selector is set to the value.

##### `Concrete State`

The client `concrete_state` method obtains a scrape of the current page from the Aeon Runner. Obtaining a scrape is a multi-step process requiring multiple calls to the Aeon session. The runner client begins by obtaining the URL for the new AUT page. It then determines if jQuery has been loaded into the page and injects it if it has not been loaded.

As there is no determinative mechanism to know how long it should take for all elements on the page to load, and because the Chrome AUT client will not response proactively when all elements have loaded, the Aeon Runner polls the Chrome AUT Client to determine if the DOM is loaded and in a ready state. It makes 10 attempts with a timeout of 0.2 seconds between attempts. If the AUT contains pages that are particularly slow at loading, either or both of these numbers may need to be adjusted.

Once the DOM has completed loading and is ready, the Runner Service runs the Aeon session's `execute_command('ExecuteScriptCommand', [self.SCRAPE_SCRIPT])` to obtain the final concrete state information. If no failures have occurred, it returns the concrete state; otherwise, False.

##### `Quit`

The client `quit` method is called to stop an Aeon Runner Service session.

#### Data

The runner client injects the following three javascript files to enable the scraping of data from the Aeon Runner's Chrome AUT client.

#### *checkReadyState.js*

Used by the Runner Client and Aeon Runner Service to determine if the a AUT page is ready to be scraped.

#### *installJQuery.js*

The stateScaper.js requires the use of jQuery. The Runner Client and Aeon Runner Service determine if jQuery has been loaded on a page, and if not, this script is injected into the Chrome AUT client. 

#### *stateScraper.js*

This JavaScript file performs the scrape of an AUT page. The scrape represents a concrete state, and in its raw form as produced by the stateScraper, consists of the following elements:

```python
    var data = {
        url: "",
        title: "",
        widgets: {},
        elements: {}
    };
```

The url is set to the page's `window.location.href` and the title is set to the page's `document.title`.  The primary logic of the stateScraper populates the widgets and elements dictionary.

Each visible HTML element on the page, or on any referenced page through an iFrame, with the exception of VirtualTextNodes, are captured as widgets.

#### Defects

#### *Defect*

A defect represents an issue found during exploration and testing. Expectations are derived from past experience with similar tests, on similar fields, with similar test flows. Agent expectations are not derived from explicitly stated requirements. Rather, they are the product of domain knowledge reflected in the training of the system.

A defect object is initialized with the abstract test flow that resulted in the defect, the actions associated with the test flow, and an index to indicate at which point within the test flow the defect was detected.

##### `Defect Reporter`

The Defect Reporter maintains a list of tracked defects, which the Flow Executor adds to when it discovers a defect. The external reporting of defects is not yet implemented.

#### Flow Execution

The Flow Execution module consists of the FlowExecutor, the FlowPlanner, and ConcreteTestFlow classes.

#### *Flow Executor*

The Flow Executor executes a concrete test flow. A Flow Executor object is initialized with the following parameters:

* form_expert: An instance of the form expert client.  
* page_analyzer: An instance of the page analyzer client.  
* state_abstracter: An instance of the StateAbstracter class.  
* label_extracter: An instance of the LabelExtraction class.  
* observer: An instance of the StateObserver class.  
* defect_rep: An instance of the DefectReporter class.  

The Flow Executor supports a single method, execute, which takes three parameters:

* initial_state: The current abstract state (where the concrete test flow execution begins from).
* runner: An instance of the runner client (that holds an active runner session).
* concrete_flow: The concrete test flow to execute.

The execute method returns True if the concrete test flow execution succeeded.

The Flow Executor executes the following steps:

1. To begin the Flow Executor fills out all of the form values associated with the initial_state using the Fill Entire Form, Form Strategy described further below. The Fill Entire Form, Flow Strategy attempts to fill out all form widgets with valid data. The strategy interfaces directly with the Form Expert and the Runner Client to perform the actions required to fill out the form on the AUT. Note: the values filled in by the Fill Entire Form strategy may be later written over with new values by the processing of concrete_flow 'TRY' actions in Step 3, below.  

2. If successful, and for each step within the concrete_flow.bound_actions, the Flow Executor iterates through  'TRY' and 'CLICK' substeps. Note: `bound_actions` reference an action and a widget.  

    a. If the action is 'TRY', the executor asks the Form Expert for an appropriate test value for the specified action. Given the value, the executor then sets the value on the associated widget within the AUT using the Runner Client.  

    b. If the action is 'CLICK', the executor clicks the associated widget within the AUT using the Runner Client.  

3. Subsequent to executing the action, the executor retrieves the next AUT concrete state from the Runner Client.  

4. The executor analyzes the concrete state to generate:  

    a. The Page Analysis Service extracts inferred information using machine learning classification techniques to include page titles, label candidates, error messages, commits, and cancels.  

    b. The State Abstractor determines the associated abstract state.  

    c. The Label Extraction determines the page labels the Page Analysis (label candidates) and abstract state information.

    d. The State Observer determines observations from the abstract state and page analysis results (element classifications).  

5. Does the expected observation match the actual observation? If no, the Flow Executor creates, adds, and logs a defect.  

6. The Flow Executor returns True as long as the Runner Client was able to return a valid concrete state in response to Step 3.  

#### *Flow Planner*

The Flow Planner combines information from page classifiers along with an abstract test flow to generate possible concrete test flows for the SUT. The Flow Executor supports a single method, execute, which takes three parameters:

* abstract_state  
* page_analysis  
* abstract_flow

For each action within the abstract flow, the Flow Planner finds the associated widget in the abstract state information. If it is unable to bind the flow act to a specific abstract state widget, the Flow Planner logs the failure and returns False. In the case of a 'TRY' action, an abstract widget is matched based on its associated label, and if successful, a single widget will be bound to the action as a `plan_step`. This plan step is appended to a list of 'plan_steps'.

In the case of a 'CLICK' action, multiple plan steps may be added as possible bound matches for the current action. For 'CLICK' actions, the actions are matched to a widget based on the element class of the action equivalence class. Page Analysis may match the element class to multiple candidate widgets. An `actual_widget`, matching the candidate widget, is then extracted from the abstract state, and this actual widget is matched with the abstract flow action to form a possible_step. All possible steps resulting from a 'CLICK' action are added to `plan_steps` as a single list entry.

Plan steps are then expanded into all possible list combinations, the `cartesian_product`. The cartesian product entries are planned abstract flows. In a final step, these are converted to concrete test flows and returned to the calling function.

#### Form_strategies

The form strategies is designed to ultimately support multiple different strategies; however, for this version a single strategy is supported. This strategy attempts to fill out all fields in a possible form with valid values. Once these initial values are entered, the system may go back and fill out certain fields with different values in conjunction with specific test flow steps.

#### *Fill Entire Form*

A Fill Entire Form object is initialized with a Form Expert client. The object supports one method, execute. This method takes two parameters, a Runner client and an abstract state. The execute method attempts to obtain valid input valids for all abstract state, actionable widgets. It iterates through the actionable widgets that the Form Expert returns, and sets the corresponding Chrome AUT client field values to the values proposed by the Form Expert using the Runner Client.

#### Agent Loop

The Agent Loop, agent_loop.py, implements the core control flow of the Exploration and Test Agent. It observes the SUT environment, plans, and acts upon the environment.

The Agent Loop instantiates the other primary module / classes of the Exploration and Test Agent:  

* StateAbstracter  
* LabelExtraction  
* FormExpertClient  
* PriorityMemory  
* StateObserver  
* SequenceParser  
* FlowPlanner  
* DefectReporter  
* PlannedFlowPublisher  
* RunnerClient  
* PageAnalysisClient  
* FlowGeneratorClient  
* FlowExecutor  

The Agent Loop is initialized and started within the Distributed Task Queue, Inbound Task (inbound_tasks.py), start\_session task. The Agent Loop starts a loop_thread which runs the \_loop\_start method, which in turn iterates over the \_loop\_iteration method. The loop will stop after 300 iterations, as defined by NUM\_ITERATIONS, or if the general_memory\[SESSION\_STOPPED\] boolean is set to True.

The \_loop\_iteration method executes a single control loop iteration. Each loop iteration performs the following steps:
1) Perceive the current environment, drawing observations,  
2) For each observation, consult the flow generation service to generate abstract test flows,  
3) For each generated abstract flow, attempt to map it to one or more concrete test flows for the SUT,  
4) Publish all concrete test flows to a message queue to be consumed by the Coordinator Agent,  
5) If there exists a concrete test flow on our work queue (populated by the Coordinator Agent) that is currently executable based on current SUT context, pop it off the queue and execute it,  
6) Otherwise, check if there is an executable test flow that resulted from Step 3. If so, execute it, and  
7) Otherwise, go into exploration mode.  

#### *Perceive the current environment*

The \_loop\_iteration method first observes the current environment, extracting the information necessary to make a decision. Raw information is obtained from the Runner Client. The Runner Client scrapes the current state of the Application Under Test and passes that information back as a concrete_state. The Concrete State is scraped from the browser using the window.aist_scrape function defined in stateScraper.js.

The Concrete State is utilized to generate three additional pieces of information describing the current environment:
1) A page analysis,  
2) An abstract representation of the concrete state, and  
3) Page labels extracted using both the page analysis and the abstract state information.

If there are no actional widgets found on a page, the session has reached a dead-end and the exploration / testing is restarted at the SUT url.

#### *Generate observations*

Observations are generated by the StateObserver using ML-based element classifiers, and are formulated as natural language strings (e.g. Observe TextBox FirstName).

#### *Generate abstract test flows, map to concrete test flows, and publish to coordinator*

The loop then cycles through the observations and generates any corresponding abstract and concrete test flows. An abstract test flow is a site/page independent representation of a test flow through a system. The concrete test flow represents a conversion of the abstract test flow for use on the current page. For example, abstract references "Observe TextBox FirstName" are replaced with specific selector based references to a FirstName TextBox on the page.

The abstract test flows are generated by the FlowGeneratorClient and converted into a parsed flow leveraging the Agent's abstract flow grammar. The FlowPlanner then converts the parsed, abstract flows into planned, concrete test flows if possible.

Any successfully completed planned, concrete test flows are tasked to the coordinator for future action. 

#### *If possible, execute a test flow*

If a planned, concrete test flow exists in the celery_memory, as filled by a Coordinator executed Celery task, pop it off the stack and execute it using the FlowExecutor. If not, is there a locally generated test flow on our queue (see above)? If so, pop one off the stack and execute it.

If it was possible to execute a test flow, this concludes one iteration through the Agent Loop.

#### *If not possible to execute a test flow, explore*

If the Exploration and Test Agent was unable to execute a test flow on a given iteration through the Agent Loop, it will attempt to further explore the SUT. With a memory of past activities, and input from the form expert in the case of forms, the Exploration and Test Agent randomly selects a previously untested action to perform on the SUT. This concludes one iteration through the Agent Loop.

#### Memory

The Memory source contains two actively used memory modules:  

* Agent Memory  
* Priority Memory  

The basic memory module is no longer used.

#### *Agent Memory*

The Agent Memory module establishes two globally shared memories, `celery_memory` and `general_memory` and a globally shared `memory_lock` to regulate multi-threaded access. 

#### *Priority Memory*

The Priority Memory module keeps track of which widgets have been explored by the Exploration and Testing Agent for every abstract state.  

##### `Choose Widget method`

In addition to tracking the use of the widgets, the Priority Memory provides a helper method for the selection of abstract state widgets. The `choose_widget` method takes one argument, the `abstract_state`, chooses one widget from the abstract state, and returns the chosen widget. 

The choose widget method preferably selects a widget that has not been explored, or has been explored the least number of times. It further prioritizes element tags defined in the PriorityMemory.PRIORITY list. If multiple widgets have been visited an equal number of times, and are at the same priority level, the choose widget method randomly chooses one widget from the tied set.

##### `Update Memory method`

The `update_memory` method takes two arguments, the `abstract_state`, and the `chosen_widget`. The method increments the hashed memory cell corresponding to the abstract state and chosen widget by one, thereby tracking the number of visits of the indicated widget.   

#### Perceive

#### *Label Extraction*

The Label Extraction module extracts labels for each actionable widget in an abstract state. Its main method, the `extract_labels` method takes two arguments, an abstract state and a Page Analysis client. It directly mutates the widgets contained in the abstract_state. It does not return a value.

#### *State Observer*

The State Observer is responsible for extracting observations from an abstract state. Its `perceive_method` takes two arguments, `abstract_state` and `page_analysis`, and returns observations (instances of the Observation class) from a given abstract state in the form of grammar ASTs. The method relies on element classifications provided by the Page Analysis client for the given abstract state.

#### Distributed Task Queue (Celery)

The Exploratory Test Agent support three inbound tasks and a single outbound task. The system supports one or more instances of these agents, and inbound tasks are distributed using both broadcast and round_robin queues as described below.

#### *Inbound Tasks*

Two of the inbound tasks are passed over a broadcast queue to all Exploratory Test Agents. These tasks, start_session and stop_session, will cause all of the instantiated agents to start a session using the provided System Under Test (SUT) URL.

The third task, handle_planned_flow, is passed to the next Exploratory Test Agent instance in a round robin scheme.

##### `Start Session`

The Celery task starts a new session on all instantiated Exploratory Test Agents.

**Task Name:** test_agent.start_session  
**Queue:** agent_broadcask_tasks  
**Param:** {'SUT_URL' : 'your_system_under_test_url'}  
**Return Result:** Returns False if environment variable RUNNER_URL not setup properly; otherwise, True.  

##### `Stop Session`

The Celery task stops ALL Exploratory Test Agent sessions.

**Task Name:** test_agent.stop_session  
**Queue:** agent_broadcask_tasks  
**Return Result:** True  

##### `Handle Planned Flow`

The Exploratory Test Agent adds (initializing or appending to existing information) the received Celery task, planned_flow data to the celery_memory (dictionary) item indexed by the planned_flow.intial_state.hash. A planned_flow is also an intance of a ConcreteTestFlow.

**Task Name:** test_agent.handle_planned_flow  
**Queue:** test_agent_queue  
**Param:** flow_data (A Jsonified instance of the Exploratory Test Agent, ConcreteTestFlow class)  
**Return Result:** Returns False if environment variable RUNNER_URL not setup properly; otherwise, True.

Note: Agent does not yet employ a common library or explicit contracts to define parameters sent via Celery. Modifications to the ConcreteTestFlow class must be made in both the Exploratory Test Agent and Coordinator.

#### *Outbound Tasks*

The Exploratory Test Agent sends an instance of the ConcreteTestFlow class, a planned_flow, to the Coordinator. 

**Task Name:** test_coordinator.handle_planned_flow  
**Queue:** test_coordinator_queue  
**Param:** flow_data (A Jsonified instance of the Exploratory Test Agent, ConcreteTestFlow class)  
**Return Result:** Returns False if environment variable RUNNER_URL not setup properly; otherwise, True.

### Coordinator

### Page Analyzer

### Form Expert

### Gateway

### Flow Generator

## Agent Training

### Agent-X

#### Page Labeler

#### Component Classification Viewer

### Page Recognition Training

### Test Flow Training

## Test Flow Grammar

## Dependencies

## Warnings
