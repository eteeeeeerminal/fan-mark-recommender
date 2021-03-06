import pytest
from src.scrape_fan_mark import (
    greedy_emoji,
    make_emoji_page_url
)

def test_make_emoji_page_url():
    assert "https://v-data.info/e/F09FA6B4" == make_emoji_page_url("π¦΄")
    assert "https://v-data.info/e/F09F98BA" == make_emoji_page_url("πΊ")
    assert "https://v-data.info/e/E29ABD" == make_emoji_page_url("β½")

def test_greedy_emoji():
    assert "π¦π«" == greedy_emoji("π¦π«π½")
    assert "πΊ" == greedy_emoji("πΊπ§")