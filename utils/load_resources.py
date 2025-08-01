from pathlib import Path
import json

BASE = Path(__file__).absolute().parent.parent

def resources_schemas_path(schema_file, module=None):
    if module:
        return BASE / "src" / "resources" / "schemas" / module / schema_file
    else:
        return BASE / "src" / "resources" / "schemas" / schema_file

def load_schema_resource(schema_file, module=None):
    try:
        with resources_schemas_path(schema_file, module).open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Schema file '{schema_file}' not found in module '{module}'")