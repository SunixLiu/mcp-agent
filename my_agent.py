from smolagents import ToolCollection, CodeAgent, OpenAIServerModel
from mcp import StdioServerParameters

# Define API parameters for the OpenAI-compatible server
API_BASE = "http://127.0.0.1:1234/v1"
API_KEY = "sk-whatever"
MODEL_ID = "qwen-2.5-coder-14b-instruct"

# Initialize the OpenAIServerModel with specified parameters
model = OpenAIServerModel(
    api_base=API_BASE,
    api_key=API_KEY,
    model_id=MODEL_ID,
)

#MCP server 1
server_1= StdioServerParameters(
    command="uv",
    args=[
        "--directory",
        "D:/01Projects/MCP/documentation",
        "run",
        "main.py"
    ],
)

#MCP server 2
server_2= StdioServerParameters(
    command="uv",
    args=[
        "--directory",
        "D:/01Projects/MCP/credit-risk",
        "run",
        "credit-risk.py"
    ],
)

# Use the ToolCollection to create tool sets from MCP servers
with ToolCollection.from_mcp(server_1) as tool_collection1, \
     ToolCollection.from_mcp(server_2) as tool_collection2:
    # Combine tools from both collections into a single list
    combined_tools = list(tool_collection1.tools) + list(tool_collection2.tools)
    
    # Initialize a CodeAgent with the OpenAI model and combined tools
    agent = CodeAgent(model=model, tools=combined_tools, add_base_tools=False)
    
    # Run the agent with a specific query about the credit risk dataset
    agent.run("get me columns of the credit risk dataset, and tell me how many columns are there")
