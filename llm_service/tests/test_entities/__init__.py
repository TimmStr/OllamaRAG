import pytest
from langchain_text_splitters import RecursiveCharacterTextSplitter

from entities import TextSplitterSingleton


@pytest.fixture(scope="module")
def singleton_instance():
    return TextSplitterSingleton.get_instance()


def test_singleton_instance(singleton_instance):
    instance_1 = TextSplitterSingleton.get_instance()
    instance_2 = TextSplitterSingleton.get_instance()
    assert instance_1 is instance_2, "The instances are unequal!"


def test_instance_type(singleton_instance):
    assert isinstance(singleton_instance,
                      RecursiveCharacterTextSplitter), "The instance is not of type RecursiveCharacterTextSplitter!"


def test_instance_parameters(singleton_instance):
    assert singleton_instance._chunk_size == 500, f"Expected chunk_size: 500, but is {singleton_instance.chunk_size}"
    assert singleton_instance._chunk_overlap == 50, f"Expected chunk_overlap: 500, but is {singleton_instance.chunk_overlap}"
