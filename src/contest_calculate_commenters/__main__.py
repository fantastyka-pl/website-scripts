import dataclasses
import sys
import re

from bs4 import BeautifulSoup
from requests import Session


def download_webpage(url: str) -> str:
    session = Session()
    response = session.get(url)
    if response.status_code != 200:
        print("Couldn't download the webpage.")
        sys.exit(1)
    return response.text


@dataclasses.dataclass
class Story:
    author: str
    title: str
    url: str
    length: int
    commenters: list[str]


@dataclasses.dataclass
class Author:
    name: str
    story: Story
    commented_on: list[Story]


def parse_story_page(url: str) -> Story:
    print(f"Fetching data from {url}")
    soup_story = BeautifulSoup(download_webpage(url), 'html.parser')
    author = soup_story.select('article.tekst a.login')[0].text
    title = soup_story.select('.opko h1')[0].text
    print(f"Data related to the '{title}' story has been fetched.")
    length = int(re.search(r'(\d+)$', soup_story.select('.tekst .data')[0].text).group())
    commenters_data = soup_story.select('section.kom .login')
    commenters: list[str] = []
    for commenter_data in commenters_data:
        commenters.append(commenter_data.text)

    return Story(
        author=author,
        title=title,
        url=url,
        length=length,
        commenters=commenters
    )


FANTASTYKA_DOMAIN = 'https://www.fantastyka.pl'

contest_id = input("Enter contest id: ")

contest_url = f"{FANTASTYKA_DOMAIN}/opowiadania/konkursy/{contest_id}"

contest_page = download_webpage(contest_url)
soup = BeautifulSoup(contest_page, 'html.parser')

stories_data = soup.select('section:nth-child(5) .lista')

stories = []
for story_data in stories_data:
    url = FANTASTYKA_DOMAIN + story_data.select(".tytul")[0].get('href')
    stories.append(
        parse_story_page(url)
    )


authors = []
for story in stories:
    authors.append(
        Author(
            name=story.author,
            story=story,
            commented_on=[]
        )
    )

for author in authors:
    name = author.name
    # Don't count an anonymous author.
    if name == 'Anonim':
        continue
    for story in stories:
        # Don't count the story that the author wrote.
        if story.url == author.story.url:
            continue
        if name in story.commenters:
            author.commented_on.append(story)

for author in authors:
    print(f"'{author.name}' author of the story '{author.story.title}' ({author.story.length}) commented on {len(author.commented_on)} stories{'.' if len(author.commented_on) == 0 else ':' }")
    for story in author.commented_on:
        print(f"{story.title} : {story.url}")
    print("")
