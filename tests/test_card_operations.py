import pytest

from src.card_processing import card_operations, top_transactions
from src.utils import read_file_2



@pytest.fixture
def text():
    return read_file_2()
def test_card_operations(text):


    assert type(card_operations(text)) ==  list
    assert len(card_operations(text)) != 0


@pytest.fixture
def text_2():
    return read_file_2()

def test_top_transactions(text_2):
    # print(text)
    assert type(top_transactions(text_2)) == list
    assert len(top_transactions(text_2)) != 0
