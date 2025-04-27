import asyncio
import datetime
from typing import List, Optional, Union, Literal

import httpx
from pydantic import BaseModel, Field
import tiktoken

import pydantic


def to_lower_camel_case(snake_str: str) -> str:
    # We capitalize the first letter of each component except the first one
    camel_string = "".join(x.capitalize() for x in snake_str.lower().split("_"))
    return snake_str[0].lower() + camel_string[1:]


class CamelCaseDTO(pydantic.BaseModel):
    """
    This is a base schema intended for all API facing schemas
    to have the came casing functionality.

    when you create your schema extending from this one you API
    will expect both request and response to
    have camelCasing.
    """
    
    if pydantic.__version__.startswith("2"):
        model_config = pydantic.ConfigDict(
            populate_by_name=True, 
            alias_generator=to_lower_camel_case
        )
    else:

        class Config:
            alias_generator = to_lower_camel_case
            allow_population_by_field_name = True



class Item(BaseModel):
    id: int
    type: str


class Story(Item):
    type: Literal["story"]
    by: Optional[str] = None
    time: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    text: Optional[str] = None
    score: Optional[int] = None
    descendants: Optional[int] = None
    kids: List[int] = Field(default_factory=list)


class Comment(Item):
    type: Literal["comment"]
    by: Optional[str] = None
    time: Optional[int] = None
    parent: Optional[int] = None
    text: Optional[str] = None
    kids: List[int] = Field(default_factory=list)


class Job(Item):
    type: Literal["job"]
    by: Optional[str] = None
    time: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    text: Optional[str] = None
    score: Optional[int] = None


class Poll(Item):
    type: Literal["poll"]
    by: Optional[str] = None
    time: Optional[int] = None
    title: Optional[str] = None
    parts: List[int] = Field(default_factory=list)
    descendants: Optional[int] = None
    kids: List[int] = Field(default_factory=list)


class PollOpt(Item):
    type: Literal["pollopt"]
    by: Optional[str] = None
    time: Optional[int] = None
    poll: Optional[int] = None
    score: Optional[int] = None
    text: Optional[str] = None


class User(BaseModel):
    id: str
    created: int
    karma: int
    about: Optional[str] = None
    submitted: List[int] = Field(default_factory=list)


class HNClient:
    """
    Async Hacker News client using httpx and pydantic.
    """

    def __init__(
        self,
        base_url: str = "https://hacker-news.firebaseio.com/v0",
        algolia_url: str = "https://hn.algolia.com/api/v1",
    ):
        self.base_url = base_url.rstrip("/")
        self.algolia_url = algolia_url.rstrip("/")
        self.client = httpx.AsyncClient()

    async def get_item(self, id: int) -> Union[Story, Comment, Job, Poll, PollOpt, Item]:
        resp = await self.client.get(f"{self.base_url}/item/{id}.json")
        resp.raise_for_status()
        data = resp.json() or {}
        t = data.get("type")
        mapping = {
            "story": Story,
            "comment": Comment,
            "job": Job,
            "poll": Poll,
            "pollopt": PollOpt,
        }
        model = mapping.get(t, Item)
        return model(**data)

    async def get_story(self, id: int) -> Story:
        item = await self.get_item(id)
        if not isinstance(item, Story):
            raise TypeError(f"Item {id} is not a story")
        return item

    async def get_comment(self, id: int) -> Comment:
        item = await self.get_item(id)
        if not isinstance(item, Comment):
            raise TypeError(f"Item {id} is not a comment")
        return item

    async def get_user(self, id: str) -> User:
        resp = await self.client.get(f"{self.base_url}/user/{id}.json")
        resp.raise_for_status()
        return User(**(resp.json() or {}))

    async def search(
        self,
        query: str,
        object_type: Literal["story", "comment", "job"],
        limit: int = 10,
        since: Optional[datetime.datetime] = None,
        until: Optional[datetime.datetime] = None,
    ) -> List[Union[Story, Comment, Job]]:
        params = {"query": query, "tags": object_type, "hitsPerPage": limit}
        filters = []
        if since:
            filters.append(f"created_at_i>{int(since.timestamp())}")
        if until:
            filters.append(f"created_at_i<{int(until.timestamp())}")
        if filters:
            params["numericFilters"] = ",".join(filters)

        resp = await self.client.get(f"{self.algolia_url}/search", params=params)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
        results: List[Union[Story, Comment, Job]] = []

        for h in hits:
            typ = object_type
            if typ == "comment":
                results.append(
                    Comment(
                        id=int(h.get("objectID", 0)),
                        by=h.get("author"),
                        time=h.get("created_at_i"),
                        parent=int(h.get("story_id", 0)),
                        text=h.get("comment_text"),
                        kids=[],
                        type="comment",
                    )
                )
            else:
                # story or job
                results.append(
                    Story(
                        id=int(h.get("objectID", 0)),
                        by=h.get("author"),
                        time=h.get("created_at_i"),
                        title=h.get("title") or h.get("story_title"),
                        url=h.get("url") or h.get("story_url"),
                        text=h.get("story_text"),
                        score=h.get("points"),
                        descendants=h.get("num_comments"),
                        kids=[],
                        type="story",
                    )
                )
        return results

    async def get_latest_stories(self, limit: int = 30) -> List[Story]:
        resp = await self.client.get(f"{self.base_url}/newstories.json")
        resp.raise_for_status()
        ids = resp.json() or []
        tasks = [self.get_story(i) for i in ids[:limit]]
        return await asyncio.gather(*tasks)

    async def get_top_stories(self, limit: int = 30) -> List[Story]:
        resp = await self.client.get(f"{self.base_url}/topstories.json")
        resp.raise_for_status()
        ids = resp.json() or []
        tasks = [self.get_story(i) for i in ids[:limit]]
        return await asyncio.gather(*tasks)

    async def close(self) -> None:
        await self.client.aclose()



import os
import json
from dotenv import load_dotenv
import httpx
import openai
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

encoder = tiktoken.encoding_for_model('gpt-4o-mini')

MAX_TOKENS = 120000

async def extract_main_url_content(content: str) -> str:

    website = BeautifulSoup(content, 'html.parser')
    
    website_body = website.find('body')
    prompt = (
        "You are a web scrapping bot for a news company, extract the raw information contain the following html source code.\n" +
        "<raw_source>\n" +
        website_body.get_text(separator='\n', strip=True) +
        "</raw_source>"
    )
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

async def gather_full_comment_thread(client: HNClient, comment_id: int) -> str:

    
    comment = await client.get_comment(comment_id)
    
    formatted_result = (
        '<comment>\n'+
        '<content>\n' +
        (comment.text or 'no content') +
        '</content>\n'
    )
    
    for nested_comment_id in comment.kids:
        nested_comment  = await gather_full_comment_thread(client, nested_comment_id)
        formatted_result += nested_comment + '\n'
    
    formatted_result += '</comment>'
    
    return formatted_result
    
    

async def gather_full_story_corpus(client: HNClient, story: Story) -> str:
    
    if story.url is not None:
        async with httpx.AsyncClient() as http_client:
            story_source = await http_client.get(story.url)
            story_source.raise_for_status()
            story_source_text = story_source.text

        extracted_source_content = await extract_main_url_content(story_source_text)


    conversation_thread = (
        '<thread_title>\n' +
        story.title +
        '<thread_title>\n' +
        '<thread_description>\n' +
            (story.text or 'no description') +
        '</thread_description>\n'
    )

    for comment_id in story.kids:
        comment = await gather_full_comment_thread(client, comment_id)
        conversation_thread += comment + '\n'
        
        
        
        
        
    return f"""You are a new york times best writers. 
    You are tasked with the duty of creating a good compelling article for our readers based on the following story found in hacker news.
    You'll be given the story source url content in between <story_url_content> tags and the hacker news conversation that followed it in <story_conversation> tags.
    the story comes directly from hacker news, meaning you will find nested comments which represent the conversations under the posts, they are denoted with <comment> tags.
    Please, use this information to generate a compelling story for our readers. Your guidelines are:
    You should ONLY write the content of the article. 
    Do not include date
    Do not include author
    The article should be helpful and pleasant to read.
    
    <story_url_content>
    {extracted_source_content}
    </story_url_content>

    <story_conversation>
    {conversation_thread}
    </story_conversation>

    You MUST use markdown format to write your article.
    """


def generate_article(prompt: str) -> str:
    """
    Summarize a list of comment texts using OpenAI.
    """
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_lead(article):
    """
    Summarize a list of comment texts using OpenAI.
    """
    prompt = (
        "Create a brief lead paragraph of the following article \n" +
        "You should ONLY include factual information of the article.\n" + 
        "Do not include date \n" +
        "Do not include author \n" +
        "Do not include author \n" +
        "The summary should catch the reader's attention.\n"
        "The summary should NOT EXCEED 3 sentences.\n"
        "<Article>\n" +
        article +
        "</Article>\n" 
    )
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_image(article_summary):
    client = openai.OpenAI()
    result = client.images.generate(
    model="gpt-image-1",
    size='1024x1024',
    response_format='b64_json',
    prompt="Generate a cover image in  8bit style for an article which contains the following summary: " + article_summary
)

    image_base64 = result.data[0].b64_json
    return image_base64

from typing import List
from pydantic import BaseModel, Field
import pathlib

class ArticleSource(CamelCaseDTO):
    id: str
    title: str
    source_name: str
    source_icon: str
    url: str

    class Config:
        allow_population_by_field_name = True

class NewsItem(CamelCaseDTO):
    id: str
    title: str
    date: datetime.datetime
    labels: List[str]
    cover_image: str
    description: str
    summary: str
    sources: List[ArticleSource]
    content: str

    class Config:
        allow_population_by_field_name = True



# Usage example
async def main():
    client = HNClient()
    top_stories = await client.get_top_stories(5)
    news = []
    for story in top_stories:
        
        try:
            print(f'generating articles for post about {story.title}')
            full_story = await gather_full_story_corpus(client, story)
            article_content = generate_article(full_story)
            article_summary = generate_lead(article_content)
            article_img = generate_image(article_summary)
            news.append(
            json.loads(NewsItem(
                id=str(story.id),
                title=story.title,
                date=datetime.datetime.fromtimestamp(story.time),
                labels=[],
                coverImage=article_img,
                description=article_summary,
                summary=article_summary,
                content=article_content,
                sources=[
                    ArticleSource(id='1',
                                title=story.title,
                                sourceName='HackerNews',
                                sourceIcon='https://news.ycombinator.com/y18.svg',
                                url=story.url or '')
                ]
            ).model_dump_json(by_alias=True))
            )
        except Exception as e:
            print(f'there was an error while processing the story => {e}')
        
    await client.close()
    
    path =pathlib.Path(__file__).parent.parent.joinpath('web', 'src', 'result.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(news, f)

asyncio.run(main())
