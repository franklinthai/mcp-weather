import asyncio
import sys
import json
import ollama
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server"""
        is_python = server_script_path.endswith('.py')
        if not is_python:
            raise ValueError("Server script must be a Python (.py) file")

        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        self.available_tools = {tool.name: tool for tool in response.tools}
        print("\nConnected to server with tools:", list(self.available_tools.keys()))

    async def call_mcp_tool(self, tool_name: str, params: dict):
        """Call an MCP tool if available and ensure output is a string."""
        if tool_name in self.available_tools:
            try:
                result = await self.session.call_tool(tool_name, params)
                
                # Ensure response content is a string
                if isinstance(result.content, list):
                    return "\n".join(map(str, result.content))  # Convert list to a string
                return str(result.content)  # Convert any other type to a string

            except Exception as e:
                return f"Error calling tool {tool_name}: {str(e)}"

        return f"Tool {tool_name} not available."

    async def process_query(self, query: str) -> str:
        """Process a query using Ollama's latest model and MCP tools if relevant"""
        messages = [{"role": "user", "content": query}]

        # Check if the query matches any tool usage
        if "weather alert in" in query.lower():
            state = query.split("weather alert in")[-1].strip().upper()
            return await self.call_mcp_tool("get_alerts", {"state": state})

        elif "weather forecast for" in query.lower():
            location = query.split("weather forecast for")[-1].strip()
            try:
                lat, lon = map(float, location.split())
                return await self.call_mcp_tool("get_forecast", {"latitude": lat, "longitude": lon})
            except ValueError:
                return "Invalid location format. Please provide latitude and longitude."

        # If no tool is applicable, use Ollama
        model_response = ollama.chat(model="llama3.2:latest", messages=messages)
        return model_response["message"]["content"]

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
