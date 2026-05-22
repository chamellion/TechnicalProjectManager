# TODO: 1 - Import the AugmentedPromptAgent class
import os
from dotenv import load_dotenv

from starter.phase_1.workflow_agents.base_agents import AugmentedPromptAgent

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# TODO: 2 - Instantiate an object of AugmentedPromptAgent with the required parameters
augmented_agent = AugmentedPromptAgent(openai_api_key, persona)

# TODO: 3 - Send the 'prompt' to the agent and store the response in a variable named 'augmented_agent_response'
augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# TODO: 4 - Add a comment explaining:
# - What knowledge the agent likely used to answer the prompt.
print("The agent will likely have used it trained model to answer the prompt as no external knowledge was provided to model.")
# - How the system prompt specifying the persona affected the agent's response.
print("The agent clearly assumed the persona by starting the response with the persona string \"Dear students,\"")
