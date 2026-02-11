from pathlib import Path

import pytest
import yaml


@pytest.fixture
def yaml_path():
    return Path(__file__).resolve().parents[2] / "data" / "test_data1.yaml"


def test_yaml(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None
    db_config = data["db"]
    server_config = data["server"]
    params_config = data["params"]
    print("数据库hostַ", db_config["host"])
    print("数据库port", server_config["port"])
    print("延迟时间", params_config["timeout"])


if __name__ == "__main__":
    res = test_yaml(Path(__file__).resolve().parents[2] / "data" / "test_data1.yaml")