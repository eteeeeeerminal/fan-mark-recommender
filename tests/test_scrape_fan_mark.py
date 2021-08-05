import pytest
from src.scrape_fan_mark import (
    make_emoji_page_url
)

def test_make_emoji_page_url():
    assert "https://v-data.info/e/F09FA6B4" == make_emoji_page_url("🦴")
    assert "https://v-data.info/e/F09F98BA" == make_emoji_page_url("😺")
    assert "https://v-data.info/e/E29ABD" == make_emoji_page_url("⚽")