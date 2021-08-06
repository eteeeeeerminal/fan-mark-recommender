import append_src
import asyncio
from src.scrape_fan_mark import extract_vtuber_links

loop = asyncio.get_event_loop()
loop.run_until_complete(extract_vtuber_links())