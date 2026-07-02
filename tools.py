from langchain.tools import tool
import requests
import os
from bs4 import BeautifulSoup
from tavily import TavilyClient
from rich import print
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def  web_search(query: str) -> str:
     """Perform a web search using Tavily and return the top result's title and URL and snippet."""

     response = tavily.search(query=query, max_results=4)
     out = []
     
     for r in response['results']:
          out.append(
               f"Title : {r ['title']}\n URL : {r ['url']}\n Snippet : {r['content'][:300]}...\n"
          )  
     return "\n\n------\n\n".join(out)


@tool
def scrape_url(url: str) -> str:
        """Scrape the content of a given URL and return the clean text content."""
        try:
            response = requests.get(url , timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # error for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove script and style elements
            for tag in soup(['script', 'style' , 'nav' , 'footer']):
                tag.decompose()
            return soup.get_text( separator=' ', strip=True )[:2000]
        except Exception as e:
            return f"Error while scraping URL: {str(e)}"



