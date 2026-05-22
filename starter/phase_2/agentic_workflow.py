# agentic_workflow.py

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module

import os
from dotenv import load_dotenv

from starter.phase_1.workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, \
    EvaluationAgent, RoutingAgent

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
try:
    with open("Product-Spec-Email-Router.txt", "r", encoding="utf-8") as f:
        product_spec = f.read()

    if not product_spec.strip():
        raise ValueError("Product spec document is empty.")

except FileNotFoundError:
    raise FileNotFoundError("Product spec document not found. Please check the file path.")

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    f"Product spec: {product_spec}"     # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key,
                                                                 persona=persona_product_manager,
                                                                 knowledge=knowledge_product_manager)
# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria = "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
product_manager_evaluation_agent = EvaluationAgent(openai_api_key=openai_api_key,persona=persona_product_manager_eval,evaluation_criteria=evaluation_criteria,worker_agent=product_manager_knowledge_agent,max_interactions=10)
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = (
    "Product features are defined by grouping related user stories. "
    "Each feature must be described using this exact structure:\n"
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user\n"
    f"Product spec: {product_spec}"
)
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key,persona=persona_program_manager,knowledge=knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
evaluation_criteria = (f"The answer should be product features that follow the following structure: " 
                      f"Feature Name: A clear, concise title that identifies the capability\n" 
                      "Description: A brief explanation of what the feature does and its purpose\n" 
                      "Key Functionality: The specific capabilities or actions the feature provides\n" 
                      "User Benefit: How this feature creates value for the user")
program_manager_evaluation_agent = EvaluationAgent(openai_api_key=openai_api_key,persona=persona_program_manager_eval,evaluation_criteria=evaluation_criteria,worker_agent=program_manager_knowledge_agent,max_interactions=10)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = (
    "Development tasks are defined by identifying what needs to be built to implement each user story. "
    "Each task must follow this exact structure:\n"
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story (must use personas from the product spec "
    "such as Customer Support Representative, Subject Matter Expert, or IT Administrator)\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first\n"
    f"Product spec: {product_spec}"
)
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key,persona=persona_dev_engineer,knowledge=knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
evaluation_criteria = ("The answer should be tasks following this exact structure: "
                       "Task ID: A unique identifier for tracking purposes\n"
                       "Task Title: Brief description of the specific development work\n"
                       "Related User Story: Reference to the parent user story\n"
                       "Description: Detailed explanation of the technical work required\n"
                       "Acceptance Criteria: Specific requirements that must be met for completion\n"
                       "Estimated Effort: Time or complexity estimation\n"
                       "Dependencies: Any tasks that must be completed first")
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
development_engineer_evaluation_agent = EvaluationAgent(openai_api_key=openai_api_key,persona=persona_dev_engineer_eval,evaluation_criteria=evaluation_criteria,worker_agent=development_engineer_knowledge_agent,max_interactions=10)


# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.
def product_manager_support_function(query):
    response = product_manager_knowledge_agent.respond(query)
    evaluated = product_manager_evaluation_agent.evaluate(response)
    return evaluated['final_response']

def program_manager_support_function(query):
    response = program_manager_knowledge_agent.respond(query)
    evaluated = program_manager_evaluation_agent.evaluate(response)
    return evaluated['final_response']

def development_engineer_support_function(query):
    response = development_engineer_knowledge_agent.respond(query)
    evaluated = development_engineer_evaluation_agent.evaluate(response)
    return evaluated['final_response']


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
agents = [
    {
        "name": "product manager",
        "description": "Product Manager responsible for writing user stories only, in the format 'As a [user], I want [action] so that [benefit]'. Does not define product features or engineering tasks.",
        "func": product_manager_support_function
    },
    {
        "name": "program manager",
        "description": "Program Manager responsible for defining and organizing product capabilities into features with Feature Name, Description, Key Functionality, and User Benefit. Does not write user stories or engineering tasks.",
        "func": program_manager_support_function
    },
    {
        "name": "development engineer",
        "description": "Development Engineer responsible for defining the development tasks for a product only, Does not define the user stories or features for a product.",
        "func": development_engineer_support_function
    }
]
routing_agent = RoutingAgent(openai_api_key, agents)

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = ("Create a complete project plan for the Email Router product. "
                   "The plan must include: "
                   "1. User stories for all user personas in the product spec, "
                   "2. Product features defined by grouping those user stories, "
                   "3. Engineering development tasks for implementing each user story.")
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
action_plan = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
#   2. Initialize an empty list to store 'completed_steps'.
completed_steps = []
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
user_stories_output = ""
features_output = ""
tasks_output = []
for step in action_plan:
    print(f"Executing step: {step}")
    route_result = routing_agent.route_prompt_to_agent(step)
    completed_steps.append(route_result)
    print(f"Step: {step}, Route Result: {route_result}")
    #   4. After the loop, print the final output of the workflow (the last completed step).

    stripped = step.strip()
    if stripped.startswith("1."):
        user_stories_output = route_result
    elif stripped.startswith("2."):
        features_output = route_result
    elif stripped.startswith("3."):
        tasks_output.append(route_result)

final_output = (
    "Completed Plan \n\n"
    "--- USER STORIES ---\n"
    f"{user_stories_output}\n\n"
    "--- PRODUCT FEATURES ---\n"
    f"{features_output}\n\n"
    "--- ENGINEERING TASKS ---\n"
    f"{chr(10).join(tasks_output)}\n"
)

print(f"Final workflow output:\n{final_output}")