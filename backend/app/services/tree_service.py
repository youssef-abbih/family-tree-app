import json
from pathlib import Path
from typing import Optional

_DATA_PATH = Path(__file__).parent.parent.parent.parent / "data" / "family_tree.json"

_cache: dict = {}
_path_cache: dict[str, list[str]] = {}
_set_cache: dict[str, frozenset] = {}


def _load() -> dict:
    global _cache
    if not _cache:
        with open(_DATA_PATH) as f:
            _cache = json.load(f)
    return _cache


def get_all_persons() -> list[dict]:
    return _load().get("persons", [])


def get_person(person_id: str) -> Optional[dict]:
    return next((p for p in get_all_persons() if p["id"] == person_id), None)


def get_by_generation(n: int) -> list[dict]:
    return [p for p in get_all_persons() if p.get("generation") == n]


def get_max_generation() -> int:
    persons = get_all_persons()
    return max((p.get("generation", 1) for p in persons), default=1)


def search(query: str) -> list[dict]:
    q = query.lower().strip()
    if not q:
        return []
    return [
        p for p in get_all_persons()
        if q in p.get("name_en", "").lower() or q in p.get("name_ar", "")
    ]


def filter_by_type(type_name: str) -> list[dict]:
    if not type_name or type_name == "all":
        return get_all_persons()
    return [p for p in get_all_persons() if p.get("type") == type_name]


def get_stats() -> dict:
    persons = get_all_persons()
    types = ["prophet", "companion", "leader", "poet", "scholar"]
    return {
        "total": len(persons),
        "generations": get_max_generation(),
        "by_type": {t: sum(1 for p in persons if p.get("type") == t) for t in types},
    }


# ── Cached ancestor path functions ───────────────────────────────────────────

def _ensure_cache() -> None:
    global _path_cache, _set_cache
    if _path_cache:
        return
    persons = get_all_persons()
    pm = {p["id"]: p for p in persons}
    for p in persons:
        pid = p["id"]
        path, seen = [], set()
        curr: Optional[str] = pid
        while curr and curr not in seen:
            path.append(curr)
            seen.add(curr)
            parent = pm.get(curr)
            if not parent:
                break
            curr = parent.get("father_id")
        _path_cache[pid] = path
        _set_cache[pid] = frozenset(path)


def get_path_to_root(person_id: str) -> list[str]:
    _ensure_cache()
    return _path_cache.get(person_id, [person_id])


def find_lca(person_ids: list[str]) -> tuple[Optional[str], list[str]]:
    _ensure_cache()
    if not person_ids:
        return None, []
    if len(person_ids) == 1:
        return None, _path_cache.get(person_ids[0], [person_ids[0]])

    common: frozenset = _set_cache.get(person_ids[0], frozenset())
    for pid in person_ids[1:]:
        common = common & _set_cache.get(pid, frozenset())

    if not common:
        return None, person_ids

    pm = {p["id"]: p for p in get_all_persons()}
    lca_id = max(common, key=lambda pid: pm.get(pid, {}).get("generation", 0))

    highlighted: set[str] = set()
    for pid in person_ids:
        for node in _path_cache.get(pid, []):
            highlighted.add(node)
            if node == lca_id:
                break

    return lca_id, list(highlighted)
