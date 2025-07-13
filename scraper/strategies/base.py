from abc import ABC, abstractmethod

class ScrapingStrategy(ABC):
    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def fetch_html(self, url):
        pass

    @abstractmethod
    def close(self):
        pass

class ScrapingStrategyFactory(ABC):
    @abstractmethod
    def create(self) -> ScrapingStrategy:
        pass
