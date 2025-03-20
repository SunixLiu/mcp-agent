from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests

# Initialize FastMCP with "docs" as the name
mcp = FastMCP("docs")

# User agent string for making HTTP requests
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

# Dictionary of documentation URLs for different frameworks
docs_urls={
    "crewai": "docs.crewai.com/introduction",
    "llamaindex": "docs.llamaindex.ai/en/stable",
    "smolagents": "huggingface.co/docs/smolagents/index",    
}

async def search_web(query: str) -> list | None:
    """
    Perform a web search using DuckDuckGo and return the results.

    Args:
        query: The search query.

    Returns:
        list | None: A list of search results or None if the search fails.
    """
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=3)  # Limit to 3 results
        return list(results)  # Convert generator to list
    except Exception as e:
        print(f"Search failed: {str(e)}")
        return None

async def fetch_url(url: str):
    """
    Fetch the content of a given URL and return the text.

    Args:
        url: The URL to fetch.

    Returns:
        str | None: The text content of the URL or None if the fetch fails.
    """
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"Fetch failed: {str(e)}")
        return None

@mcp.tool()
async def get_docs(query: str, framework: str):
    """
    Search the docs of a specified framework for a given query and return the top 3 results.

    Args:
        query: The query to search for.
        framework: The framework to search for (crewai, llamaindex, or smolagents).

    Returns:
        str: Text from the docs or an error message if the framework is not supported.
    """
    if framework not in docs_urls:
        return f"Framework {framework} not supported"
    
    query = f"{query} site:{docs_urls[framework]}"
    results = await search_web(query)
    
    if not results:
        return "No results found"
    
    text = ""
    for result in results:
        text += await fetch_url(result["href"])
    return text

@mcp.tool()
def new_function():
    pass

if __name__ == "__main__":
    mcp.run(transport="stdio")