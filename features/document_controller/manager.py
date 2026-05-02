# Contoh parser untuk blok <file_operations>
# Diletakkan di features/document_controller/manager.py nantinya

import json
import re
from pathlib import Path
from typing import Any

def parse_file_operations(raw_llm_output: str) -> list[dict[str, Any]]:
    match = re.search(r"<file_operations>(.*?)</file_operations>", raw_llm_output, re.DOTALL)
    if not match:
        return []
    return json.loads(match.group(1).strip())

def execute_operation(op: dict[str, Any], vault_path: Path) -> None:
    action = op["action"]
    if action == "CREATE_DIR":
        Path(op["path"]).mkdir(parents=True, exist_ok=True)
    elif action == "WRITE_FILE":
        Path(op["path"]).write_text(op["content"].replace("\\n", "\n"), encoding="utf-8")
    elif action == "MAKE_SYMLINK":
        src, dst = Path(op["src"]), Path(op["dst"])
        dst.symlink_to(src, target_is_directory=src.is_dir())
    elif action == "REMOVE_SYMLINK":
        p = Path(op["path"])
        if p.is_symlink():
            p.unlink()
    elif action == "MOVE":
        Path(op["src"]).rename(Path(op["dst"]))

