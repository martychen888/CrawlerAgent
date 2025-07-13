import json
from config import load_config, CONFIG_PATH

def test_load_config_valid_json(tmp_path, monkeypatch):
    test_config = tmp_path / "config.json"
    test_config.write_text(json.dumps({"USERNAME": "test"}))

    monkeypatch.setattr("config.CONFIG_PATH", str(test_config))  # Patch the global path
    config = load_config()

    assert config["USERNAME"] == "test"