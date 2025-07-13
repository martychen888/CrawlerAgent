from typing import Dict
from scraper.strategies.base import ScrapingStrategyFactory
import importlib

STRATEGY_REGISTRY: Dict[str, ScrapingStrategyFactory] = {}

def register_strategy(name: str, factory: ScrapingStrategyFactory):
    STRATEGY_REGISTRY[name.lower()] = factory

def get_factory(engine: str, headless=True) -> ScrapingStrategyFactory:
    factory = STRATEGY_REGISTRY.get(engine.lower())
    if factory:
        return factory(headless=headless) if callable(factory) else factory
    raise ValueError(f"Unknown scraping engine: {engine}")

# Dynamically load strategy modules to ensure registration
for mod in ("requests_strategy", "selenium_strategy", "playwright_strategy"):
    importlib.import_module(f"scraper.strategies.{mod}")