"""Provider registry for Behavioral Signals AI aggregate/public signals."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.providers.appstore.appstore_provider import AppStoreAggregateProvider
from Behavioral_Signals_AI.providers.fintech.fintech_aggregate_provider import FintechAggregateProvider
from Behavioral_Signals_AI.providers.marketplace.ecommerce_price_provider import EcommercePriceProvider
from Behavioral_Signals_AI.providers.marketplace.jumia_provider import JumiaAggregateProvider
from Behavioral_Signals_AI.providers.mobility.google_maps_provider import GoogleMapsAggregateProvider
from Behavioral_Signals_AI.providers.news.gdelt_provider import GdeltNewsProvider
from Behavioral_Signals_AI.providers.news.newsapi_provider import NewsApiProvider
from Behavioral_Signals_AI.providers.news.rss_provider import RssProvider
from Behavioral_Signals_AI.providers.search.google_trends_provider import GoogleTrendsSearchProvider
from Behavioral_Signals_AI.providers.search.pytrends_provider import PytrendsSearchProvider
from Behavioral_Signals_AI.providers.search.serpapi_provider import SerpApiSearchProvider
from Behavioral_Signals_AI.providers.social.instagram_provider import InstagramAggregateProvider
from Behavioral_Signals_AI.providers.social.tiktok_provider import TikTokAggregateProvider
from Behavioral_Signals_AI.providers.social.x_provider import XAggregateProvider
from Behavioral_Signals_AI.providers.social.youtube_provider import YouTubeAggregateProvider


def build_provider_registry() -> dict[str, Any]:
    """Return the full provider registry by mode/provider key."""

    return {
        "google": GoogleTrendsSearchProvider(),
        "google_trends": GoogleTrendsSearchProvider(),
        "serpapi": SerpApiSearchProvider(),
        "pytrends": PytrendsSearchProvider(),
        "x": XAggregateProvider(),
        "twitter": XAggregateProvider(),
        "gdelt": GdeltNewsProvider(),
        "news": NewsApiProvider(),
        "newsapi": NewsApiProvider(),
        "rss": RssProvider(),
        "tiktok": TikTokAggregateProvider(),
        "youtube": YouTubeAggregateProvider(),
        "instagram": InstagramAggregateProvider(),
        "jumia": JumiaAggregateProvider(),
        "ecommerce": EcommercePriceProvider(),
        "maps": GoogleMapsAggregateProvider(),
        "fintech": FintechAggregateProvider(),
        "appstore": AppStoreAggregateProvider(),
    }


def phase_one_provider_keys() -> list[str]:
    return ["google", "serpapi", "pytrends", "x", "gdelt", "news"]


def future_provider_keys() -> list[str]:
    return ["tiktok", "youtube", "instagram", "jumia", "ecommerce", "maps", "fintech", "appstore"]