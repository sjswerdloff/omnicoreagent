
import asyncio
import os
import sys
from unittest.mock import MagicMock

# Mock apscheduler to bypass missing dependency in omni_agent
sys.modules["apscheduler"] = MagicMock()
sys.modules["apscheduler.schedulers"] = MagicMock()
sys.modules["apscheduler.schedulers.asyncio"] = MagicMock()
sys.modules["apscheduler.triggers"] = MagicMock()
sys.modules["apscheduler.triggers.interval"] = MagicMock()
sys.modules["apscheduler.triggers.cron"] = MagicMock()
sys.modules["omnicoreagent.omni_agent"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.agent"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.background_agent"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.omni_serve"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.omni_serve.resilience"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.omni_serve.observability"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.workflow"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.workflow.parallel_agent"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.workflow.sequential_agent"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.workflow.router_agent"] = MagicMock()
sys.modules["omnicoreagent.omni_agent.deep_agent"] = MagicMock()
sys.modules["agno"] = MagicMock()
sys.modules["agno.agent"] = MagicMock()
sys.modules["agno.team"] = MagicMock()
sys.modules["agno.team.team"] = MagicMock()

from typing import Any, Dict
from omnicoreagent.core.tools.local_tools_registry import Tool

async def verify_tool_structure(tool_instance: Any):
    """Verifies that a tool follows the standard structure."""
    print(f"Verifying {tool_instance.__class__.__name__}...")

    # 1. Check get_tool method
    if not hasattr(tool_instance, "get_tool"):
        print(f"❌ {tool_instance.__class__.__name__} missing get_tool method")
        return False
    
    # 2. Check get_tool returns a Tool object
    try:
        tool_def = tool_instance.get_tool()
        if not isinstance(tool_def, Tool):
             print(f"❌ {tool_instance.__class__.__name__}.get_tool() did not return a Tool object")
             return False
        print(f"✅ {tool_instance.__class__.__name__}.get_tool() returned a valid Tool object")
    except Exception as e:
        print(f"❌ {tool_instance.__class__.__name__}.get_tool() raised exception: {e}")
        return False

    # 3. Check inputSchema is present and valid
    if not tool_def.inputSchema or "properties" not in tool_def.inputSchema:
        print(f"❌ {tool_def.name} inputSchema is invalid")
        return False
    print(f"✅ {tool_def.name} inputSchema is valid")

    return True

async def main():
    # Import tools directly from files to avoid heavy __init__ imports
    try:
        from omnicoreagent.community.exa_search import ExaSearch
        exa = ExaSearch(api_key="test_key")
        await verify_tool_structure(exa)
    except ImportError:
        print("⚠️ ExaSearch not found or failed to import")

    try:
        from omnicoreagent.community.tavily_search import TavilySearch
        tavily = TavilySearch(api_key="test_key")
        await verify_tool_structure(tavily)
    except ImportError:
        print("⚠️ TavilySearch not found or failed to import")
    
    try:
        from omnicoreagent.community.tavily_extract import TavilyExtract
        tavily_extract = TavilyExtract(api_key="test_key")
        await verify_tool_structure(tavily_extract)
    except ImportError:
        print("⚠️ TavilyExtract not found or failed to import")


    try:
        from omnicoreagent.community.exa_find_similar import ExaFindSimilar
        exa_fs = ExaFindSimilar(api_key="test_key")
        await verify_tool_structure(exa_fs)
    except ImportError:
        print("⚠️ ExaFindSimilar not found or failed to import")

    try:
        from omnicoreagent.community.exa_get_contents import ExaGetContents
        exa_gc = ExaGetContents(api_key="test_key")
        await verify_tool_structure(exa_gc)
    except ImportError:
        print("⚠️ ExaGetContents not found or failed to import")

    try:
        from omnicoreagent.community.exa_answer import ExaAnswer
        exa_ans = ExaAnswer(api_key="test_key")
        await verify_tool_structure(exa_ans)
    except ImportError:
        print("⚠️ ExaAnswer not found or failed to import")

    # Batch 2 Verifications
    try:
        from omnicoreagent.community.arxiv import ArxivTool
        await verify_tool_structure(ArxivTool())
    except ImportError:
        print("⚠️ ArxivTool not found or failed to import")

    try:
        from omnicoreagent.community.bravesearch import BraveSearchTool
        await verify_tool_structure(BraveSearchTool(api_key="test"))
    except ImportError:
        print("⚠️ BraveSearchTool not found or failed to import")

    try:
        from omnicoreagent.community.duckduckgo import DuckDuckGoSearchTool
        await verify_tool_structure(DuckDuckGoSearchTool())
    except ImportError:
        print("⚠️ DuckDuckGoSearchTool not found or failed to import")

    try:
        from omnicoreagent.community.serpapi import SerpApiGoogleSearch
        await verify_tool_structure(SerpApiGoogleSearch(api_key="test"))
    except ImportError:
        print("⚠️ SerpApiGoogleSearch not found or failed to import")

    try:
        from omnicoreagent.community.wikipedia import WikipediaSearchTool
        await verify_tool_structure(WikipediaSearchTool())
    except ImportError:
        print("⚠️ WikipediaSearchTool not found or failed to import")


    # Batch 3 Verifications
    try:
        from omnicoreagent.community.discord import DiscordSendMessage, DiscordListChannels
        await verify_tool_structure(DiscordSendMessage(bot_token="test"))
        await verify_tool_structure(DiscordListChannels(bot_token="test"))
    except ImportError:
        print("⚠️ Discord tools not found or failed to import")

    try:
        from omnicoreagent.community.slack import SlackSendMessage, SlackListChannels
        await verify_tool_structure(SlackSendMessage(token="test"))
        await verify_tool_structure(SlackListChannels(token="test"))
    except ImportError:
        print("⚠️ Slack tools not found or failed to import")

    try:
        from omnicoreagent.community.telegram import TelegramSendMessage
        await verify_tool_structure(TelegramSendMessage(token="test", chat_id="123"))
    except ImportError:
        print("⚠️ Telegram tools not found or failed to import")

    try:
        from omnicoreagent.community.x import XCreatePost, XSearchPosts
        await verify_tool_structure(XCreatePost(bearer_token="test"))
        await verify_tool_structure(XSearchPosts(bearer_token="test"))
    except ImportError:
        print("⚠️ X tools not found or failed to import")

    try:
        from omnicoreagent.community.gmail import GmailSendEmail, GmailReadEmail
        # Verify structure only, don't execute
        await verify_tool_structure(GmailSendEmail())
        await verify_tool_structure(GmailReadEmail())
    except ImportError:
        print("⚠️ Gmail tools not found or failed to import")
    
    try:
        from omnicoreagent.community.notion import NotionCreatePage, NotionSearchPage
        await verify_tool_structure(NotionCreatePage(api_key="test"))
        await verify_tool_structure(NotionSearchPage(api_key="test"))
    except ImportError:
        print("⚠️ Notion tools not found or failed to import")

    try:
        from omnicoreagent.community.aws_lambda import AWSLambdaListFunctions, AWSLambdaInvoke
        await verify_tool_structure(AWSLambdaListFunctions(region_name="us-east-1"))
        await verify_tool_structure(AWSLambdaInvoke(region_name="us-east-1"))
    except ImportError:
        print("⚠️ AWS Lambda tools not found or failed to import")

    try:
        from omnicoreagent.community.aws_ses import AWSSETSendEmail
        # Note: AWSSETSendEmail naming typo in file, consistent here
        await verify_tool_structure(AWSSETSendEmail(sender_email="test@example.com"))
    except ImportError:
        print("⚠️ AWS SES tools not found or failed to import")

    try:
        from omnicoreagent.community.docker import DockerListContainers, DockerRunContainer
        await verify_tool_structure(DockerListContainers())
        await verify_tool_structure(DockerRunContainer())
    except ImportError:
        print("⚠️ Docker tools not found or failed to import")

    try:
        from omnicoreagent.community.github import GithubSearchRepos, GithubCreateIssue, GithubGetRepository
        await verify_tool_structure(GithubSearchRepos(access_token="test"))
        await verify_tool_structure(GithubCreateIssue(access_token="test"))
        await verify_tool_structure(GithubGetRepository(access_token="test"))
    except ImportError:
        print("⚠️ GitHub tools not found or failed to import")
    try:
        from omnicoreagent.community.pandas import PandasCreateDataframe
        await verify_tool_structure(PandasCreateDataframe())
    except ImportError:
        print("⚠️ Pandas tools not found or failed to import")

    try:
        from omnicoreagent.community.csv_toolkit import CsvRead, CsvGetColumns
        # Mock file path as it checks existence
        # await verify_tool_structure(CsvRead()) 
        # CsvRead requires file_path in inputSchema but not in init. 
        # Wait, the tool definition doesn't require init args usually unless for config.
        # CsvRead init is empty (implicit).
        await verify_tool_structure(CsvRead())
        await verify_tool_structure(CsvGetColumns())
    except ImportError:
        print("⚠️ CSV tools not found or failed to import")

    try:
        from omnicoreagent.community.file import FileRead, FileWrite, FileList
        await verify_tool_structure(FileRead())
        await verify_tool_structure(FileWrite())
        await verify_tool_structure(FileList())
    except ImportError:
        print("⚠️ File tools not found or failed to import")

    try:
        from omnicoreagent.community.calculator import CalculatorTool
        await verify_tool_structure(CalculatorTool())
    except ImportError:
        print("⚠️ Calculator tools not found or failed to import")

    # Batch 6 Verifications
    try:
        from omnicoreagent.community.clickup import ClickUpListTasks
        await verify_tool_structure(ClickUpListTasks(api_key="test"))
    except ImportError:
        print("⚠️ ClickUp tools not found or failed to import")

    try:
        from omnicoreagent.community.confluence import ConfluenceGetPage
        await verify_tool_structure(ConfluenceGetPage())
    except ImportError:
        print("⚠️ Confluence tools not found or failed to import")

    try:
        from omnicoreagent.community.jira import JiraGetIssue
        await verify_tool_structure(JiraGetIssue())
    except ImportError:
        print("⚠️ Jira tools not found or failed to import")

    try:
        from omnicoreagent.community.linear import LinearGetIssue
        await verify_tool_structure(LinearGetIssue())
    except ImportError:
        print("⚠️ Linear tools not found or failed to import")

    try:
        from omnicoreagent.community.trello import TrelloListBoards
        await verify_tool_structure(TrelloListBoards())
    except ImportError:
        print("⚠️ Trello tools not found or failed to import")

    try:
        from omnicoreagent.community.todoist import TodoistGetTasks
        await verify_tool_structure(TodoistGetTasks())
    except ImportError:
        print("⚠️ Todoist tools not found or failed to import")

    try:
        from omnicoreagent.community.zendesk import ZendeskSearchArticles
        await verify_tool_structure(ZendeskSearchArticles())
    except ImportError:
        print("⚠️ Zendesk tools not found or failed to import")

    try:
        from omnicoreagent.community.googlecalendar import GoogleCalendarListEvents
        await verify_tool_structure(GoogleCalendarListEvents())
    except ImportError:
        print("⚠️ Google Calendar tools not found or failed to import")

    try:
        from omnicoreagent.community.googlesheets import GoogleSheetsRead
        await verify_tool_structure(GoogleSheetsRead())
    except ImportError:
        print("⚠️ Google Sheets tools not found or failed to import")

    try:
        from omnicoreagent.community.google_drive import GoogleDriveListFiles
        await verify_tool_structure(GoogleDriveListFiles())
    except ImportError:
        print("⚠️ Google Drive tools not found or failed to import")

    # Batch 7 Verifications
    try:
        from omnicoreagent.community.agentql import AgentQLScrapeWebsite
        await verify_tool_structure(AgentQLScrapeWebsite())
    except ImportError:
        print("⚠️ AgentQL tools not found or failed to import")

    try:
        from omnicoreagent.community.apify import ApifyRunActor
        await verify_tool_structure(ApifyRunActor())
    except ImportError:
        print("⚠️ Apify tools not found or failed to import")

    try:
        from omnicoreagent.community.firecrawl import FirecrawlScrape
        await verify_tool_structure(FirecrawlScrape())
    except ImportError:
        print("⚠️ Firecrawl tools not found or failed to import")

    try:
        from omnicoreagent.community.scrapegraph import ScrapeGraphSmartScraper
        await verify_tool_structure(ScrapeGraphSmartScraper(api_key="test"))
    except ImportError:
        print("⚠️ ScrapeGraph tools not found or failed to import")

    try:
        from omnicoreagent.community.browserbase import BrowserbaseSessionTool
        await verify_tool_structure(BrowserbaseSessionTool())
    except ImportError:
        print("⚠️ Browserbase tools not found or failed to import")

    try:
        from omnicoreagent.community.crawl4ai import Crawl4AICrawl
        await verify_tool_structure(Crawl4AICrawl())
    except ImportError:
        print("⚠️ Crawl4AI tools not found or failed to import")

    # Batch 8 Verifications
    try:
        from omnicoreagent.community.openai import OpenAIGenerateImage
        await verify_tool_structure(OpenAIGenerateImage(api_key="test"))
    except ImportError as e:
        print(f"⚠️ OpenAI tools not found or failed to import: {e}")

    try:
        from omnicoreagent.community.dalle import DalleCreateImage
        await verify_tool_structure(DalleCreateImage(api_key="test"))
    except ImportError as e:
        print(f"⚠️ DALL-E tools not found or failed to import: {e}")

    try:
        from omnicoreagent.community.eleven_labs import ElevenLabsGetVoices
        await verify_tool_structure(ElevenLabsGetVoices(api_key="test"))
    except ImportError as e:
        print(f"⚠️ ElevenLabs tools not found or failed to import: {e}")

    try:
        from omnicoreagent.community.replicate import ReplicateGenerateMedia
        await verify_tool_structure(ReplicateGenerateMedia(api_key="test"))
    except ImportError as e:
        print(f"⚠️ Replicate tools not found or failed to import: {e}")

    try:
        from omnicoreagent.community.fal import FalGenerateMedia
        await verify_tool_structure(FalGenerateMedia(api_key="test"))
    except ImportError as e:
        print(f"⚠️ Fal tools not found or failed to import: {e}")

if __name__ == "__main__":
    asyncio.run(main())
