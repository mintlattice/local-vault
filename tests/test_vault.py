from pathlib import Path
from vault.core import Vault


def test_put_get(tmp_path: Path):
    v = Vault(tmp_path, "pw123")
    v.init()
    v.put("hello", "world")
    assert v.get("hello") == "world"

