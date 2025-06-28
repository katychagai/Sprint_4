
from main import BooksCollector
import pytest




@pytest.fixture
def collector():
    collector = BooksCollector()
    return collector