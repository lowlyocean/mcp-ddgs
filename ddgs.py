from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS
from typing import Annotated
from pydantic import Field

# Initialize FastMCP server
mcp = FastMCP("ddgs")

@mcp.tool()
async def search(query: Annotated[str, Field(description="The query to search for")]) -> list[dict]:
    """
    Search using DuckDuckGo's Search API and return the results as a list of dictionaries
    """
    # Use the DDGS context manager to create a DDGS object
    with DDGS() as ddgs:
        # Use the ddgs.text() method to perform the search
        ddgs_gen = ddgs.text(
            query, safesearch="moderate", max_results=3, backend="auto"
        )
        # Check if there are search results
        if ddgs_gen:
            # Convert the search results into a list
            search_results = [r for r in ddgs_gen]

    # Return the list of search results
    return [
        {
            "link": result["href"],
            "title": result.get("title"),
            "snippet": result.get("body"),
        }
        for result in search_results
    ]

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')