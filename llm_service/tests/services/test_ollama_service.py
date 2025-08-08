from unittest import mock

import pytest

from entities.ollama_entities import Llama3
from services.ollama_service import llm_request


@pytest.fixture
def mock_req():
    mock_req = mock.Mock()
    mock_req.faiss_index_path = "mock_index_path"
    mock_req.input = "mock query"
    mock_req.k = 5
    return mock_req


@mock.patch('services.indices.generate_paper_index.get_paper_vec_store')
@mock.patch('services.indices.generate_confluence_index.get_confluence_vec_store')
@mock.patch.object(Llama3, 'create')
def test_llm_request_paper_vec_store(mock_create, mock_get_paper_vec_store, mock_get_confluence_vec_store, mock_req):
    mock_vector_store = mock.Mock()
    mock_docs = [("doc1", 0.1), ("doc2", 0.2)]
    mock_vector_store.similarity_search_with_score.return_value = mock_docs

    mock_get_paper_vec_store.return_value = mock_vector_store
    mock_get_confluence_vec_store.return_value = mock_vector_store

    mock_llm = mock.Mock()
    mock_create.return_value = mock_llm

    mock_llm.invoke.return_value = "mock result"

    result = llm_request(mock_req, paper_vec_store=True)

    mock_get_paper_vec_store.assert_called_once_with(mock_req.faiss_index_path)
    mock_llm.invoke.assert_called_once()

    assert result == "mock result"


@mock.patch('your_module.get_paper_vec_store')
@mock.patch('your_module.get_confluence_vec_store')
@mock.patch.object(Llama3, 'create')
def test_llm_request_confluence_vec_store(mock_create, mock_get_paper_vec_store, mock_get_confluence_vec_store,
                                          mock_req):
    mock_vector_store = mock.Mock()

    mock_docs = [("doc1", 0.1), ("doc2", 0.2)]
    mock_vector_store.similarity_search_with_score.return_value = mock_docs

    mock_get_confluence_vec_store.return_value = mock_vector_store
    mock_get_paper_vec_store.return_value = mock_vector_store

    mock_llm = mock.Mock()
    mock_create.return_value = mock_llm

    mock_llm.invoke.return_value = "mock result"

    result = llm_request(mock_req, paper_vec_store=False)

    mock_get_confluence_vec_store.assert_called_once_with(mock_req.faiss_index_path)
    mock_llm.invoke.assert_called_once()

    assert result == "mock result"
