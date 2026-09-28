from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from backend.app.config import Settings
from backend.app import llm
from backend.app.models import GeneratedSQL


def config(**values):
    return Settings(_env_file=None, **values)


def test_mysql_fields_preserve_special_password_characters():
    settings = config(mysql_password="p@ss:/?#", mysql_user="reader", mysql_database="demo")
    url = settings.database_connection_url
    assert url.password == "p@ss:/?#"
    assert url.database == "demo"
    assert config(database_url="sqlite://").database_connection_url == "sqlite://"


def test_cloud_endpoint_and_model_normalization():
    settings = config(ollama_host="https://ollama.com/v1/", ollama_llm_model="qwen3.5:cloud")
    assert settings.ollama_native_host == "https://ollama.com"
    assert settings.ollama_chat_model == "qwen3.5"
    assert settings.embedding_host == "http://127.0.0.1:11434"
    assert config(ollama_llm_model="qwen3.5:cloud").ollama_chat_model == "qwen3.5:cloud"


def test_client_authentication(monkeypatch):
    client = Mock()
    monkeypatch.setattr(llm, "Client", client)
    llm.make_client("https://ollama.com", "test-key")
    assert client.call_args.kwargs["headers"] == {"Authorization": "Bearer test-key"}
    llm.make_client("http://127.0.0.1:11434")
    assert client.call_args.kwargs["headers"] == {}


@pytest.mark.parametrize("cloud", [False, True])
def test_structured_chat_validates_and_retries(monkeypatch, cloud):
    monkeypatch.setattr(llm, "settings", config(ollama_host="https://ollama.com/v1" if cloud else "http://localhost:11434"))
    client = Mock()
    client.chat.side_effect = [
        SimpleNamespace(message=SimpleNamespace(content='{"wrong": true}')),
        SimpleNamespace(message=SimpleNamespace(content='```json\n{"sql": "SELECT 1"}\n```')),
    ]
    monkeypatch.setattr(llm, "_client", client)
    assert llm.structured_chat(GeneratedSQL, "system", "user").sql == "SELECT 1"
    assert ("format" in client.chat.call_args.kwargs) is not cloud


def test_invalid_cloud_output_fails_closed(monkeypatch):
    client = Mock()
    client.chat.return_value = SimpleNamespace(message=SimpleNamespace(content="invalid"))
    monkeypatch.setattr(llm, "_client", client)
    with pytest.raises(ValueError, match="after two attempts"):
        llm.structured_chat(GeneratedSQL, "system", "user")
    assert client.chat.call_count == 2
