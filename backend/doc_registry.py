import json
from pathlib import Path

REGISTRY_PATH = Path("forest/backend/uploaded_docs.json")

def load_registry():
    if not REGISTRY_PATH.exists():
        return {}

    text = REGISTRY_PATH.read_text().strip()
    if not text:
        return {}   # 🔑 HANDLE EMPTY FILE

    return json.loads(text)

def save_registry(registry):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2))
