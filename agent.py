import json
from tools import ToolBox
from llm import OllamaModel
from termcolor import colored

AGENT_SYSTEM_PROMPT_TEMPLATE = """
You are an intelligent AI assistant with access to specific tools. Your responses must ALWAYS be in this JSON format:
{{
    "tool_choice": "name_of_the_tool",
    "tool_input": "inputs_to_the_tool"
}}

TOOLS AND WHEN TO USE THEM:

1. basic_calculator: Use for ANY mathematical calculations
   - Input format: {{"num1": number, "num2": number, "operation": "add/subtract/multiply/divide"}}
   - Supported operations: add/plus, subtract/minus, multiply/times, divide
   - Example inputs and outputs:
     Input: "Calculate 15 plus 7"
     Output: {{"tool_choice": "basic_calculator", "tool_input": {{"num1": 15, "num2": 7, "operation": "add"}}}}
     
     Input: "What is 100 divided by 5?"
     Output: {{"tool_choice": "basic_calculator", "tool_input": {{"num1": 100, "num2": 5, "operation": "divide"}}}}

2. reverse_string: Use for ANY request involving reversing text
   - Input format: Just the text to be reversed as a string
   - ALWAYS use this tool when user mentions "reverse", "backwards", or asks to reverse text
   - Example inputs and outputs:
     Input: "Reverse of 'Howwwww'?"
     Output: {{"tool_choice": "reverse_string", "tool_input": "Howwwww"}}
     
     Input: "What is the reverse of Python?"
     Output: {{"tool_choice": "reverse_string", "tool_input": "Python"}}

3. no tool: Use for general conversation and questions
   - Example inputs and outputs:
     Input: "Who are you?"
     Output: {{"tool_choice": "no tool", "tool_input": "I am an AI assistant that can help you with calculations, reverse text, and answer questions. I can perform mathematical operations and reverse strings. How can I help you today?"}}
     
     Input: "How are you?"
     Output: {{"tool_choice": "no tool", "tool_input": "I'm functioning well, thank you for asking! I'm here to help you with calculations, text reversal, or answer any questions you might have."}}

STRICT RULES:
1. For questions about identity, capabilities, or feelings:
   - ALWAYS use "no tool"
   - Provide a complete, friendly response
   - Mention your capabilities

2. For ANY text reversal request:
   - ALWAYS use "reverse_string"
   - Extract ONLY the text to be reversed
   - Remove quotes, "reverse of", and other extra text

3. For ANY math operations:
   - ALWAYS use "basic_calculator"
   - Extract the numbers and operation
   - Convert text numbers to digits

Here is a list of your tools along with their descriptions:
{tool_descriptions}

Remember: Your response must ALWAYS be valid JSON with "tool_choice" and "tool_input" fields.
"""

class Agent:
    def __init__(self, tools, model_service, model_name, stop=None):
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name
        self.stop = stop
    
    def prepare_tools(self):
        toolbox = ToolBox()
        toolbox.store(self.tools)

        tool_desc = toolbox.tools()
        
        return tool_desc

    def think(self, prompt):
        tool_desc = self.prepare_tools()
        agent_system_prompt = AGENT_SYSTEM_PROMPT_TEMPLATE.format(tool_descriptions=tool_desc)

        if self.model_service == "OllamaModel":
            llm = self.model_service(self.model_name, agent_system_prompt, temperature=0, stop=self.stop)
        else:
            llm = self.model_service(model=self.model_name, system_prompt=agent_system_prompt, temperature=0)

        agent_response = llm.generate_text(prompt)
        
        return json.loads(agent_response)

    def work(self, prompt):
        agent_response = self.think(prompt)
        tool_choice = agent_response["tool_choice"]
        tool_input = agent_response["tool_input"]

        for tool in self.tools:
            if tool.__name__ == tool_choice:
                response = tool(tool_input)
                print(colored(response, "cyan"))
                return
        
        print(colored(tool_input, "cyan"))
        return
