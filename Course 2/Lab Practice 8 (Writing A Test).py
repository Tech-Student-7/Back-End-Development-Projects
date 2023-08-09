import pytest
from spellcheck import word_count, char_count, first_char, last_char

alpha = "Checking the length & structure of the sentence."
beta = "This sentence should fail the test"

@pytest.fixture
def input_value():
    input = alpha
    return input

def test_length(input_value):
    assert word_count(input_value) < 10
    assert char_count(input_value) < 50

def test_struc(input_value):
    assert first_char(input_value).isupper()
    assert last_char(input_value) == '.'
