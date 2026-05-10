"""
Business-logic layer for querying the family tree.
"""

from typing import Optional
from services.data_loader import load_data

# ── Pre-computed ancestor caches ──────────────────────────────────────────────
# Populated on first call to _ensure_cache().
# _path_cache[id] = [id, father_id, ..., root_id]  (ordered, closest first)
# _set_cache[id]  = frozenset of all ancestor IDs including self
_path_cache: dict[str, list[str]] = {}
_set_cache:  dict[str, frozenset] = {}


def _ensure_cache() -> None:
    """Build ancestor-path caches if not already built."""
    global _path_cache, _set_cache
    if _path_cache:
        return
    persons = load_data().get('persons', [])
    person_map = {p['id']: p for p in persons}
    for p in persons:
        pid = p['id']
        path: list[str] = []
        seen: set[str] = set()
        curr: Optional[str] = pid
        while curr and curr not in seen:
            path.append(curr)
            seen.add(curr)
            parent = person_map.get(curr)
            if not parent:
                break
            curr = parent.get('father_id')
        _path_cache[pid] = path
        _set_cache[pid] = frozenset(path)


def invalidate_cache() -> None:
    """Clear caches (call after data reload)."""
    global _path_cache, _set_cache
    _path_cache = {}
    _set_cache = {}


def get_path_to_root_fast(person_id: str) -> list[str]:
    """Return cached [person_id, ..., root_id] path."""
    _ensure_cache()
    return _path_cache.get(person_id, [person_id])


def find_lca_multiple(person_ids: list[str]) -> tuple[Optional[str], set[str]]:
    """
    Find the lowest common ancestor among 1+ persons using cached paths.

    1 person  → returns (None, full path to root)
    2+ persons → returns (lca_id, union of all paths up to lca)
    No common ancestor → returns (None, set of input ids)
    """
    _ensure_cache()
    if not person_ids:
        return None, set()

    if len(person_ids) == 1:
        return None, set(_path_cache.get(person_ids[0], [person_ids[0]]))

    # Intersection of ancestor sets gives all common ancestors
    common: frozenset = _set_cache.get(person_ids[0], frozenset())
    for pid in person_ids[1:]:
        common = common & _set_cache.get(pid, frozenset())

    if not common:
        return None, set(person_ids)

    # LCA = common ancestor with highest generation (deepest in tree)
    persons = load_data().get('persons', [])
    pm = {p['id']: p for p in persons}
    lca_id = max(common, key=lambda pid: pm.get(pid, {}).get('generation', 0))

    # Collect all nodes on any path from a selected person up to the LCA
    highlighted: set[str] = set()
    for pid in person_ids:
        for node in _path_cache.get(pid, []):
            highlighted.add(node)
            if node == lca_id:
                break

    return lca_id, highlighted


def get_person(person_id: str) -> Optional[dict]:
    """Return a single person by ID, or None if not found."""
    for person in load_data().get('persons', []):
        if person['id'] == person_id:
            return person
    return None


def get_children(person_id: str) -> list[dict]:
    """Return all direct children of a person."""
    parent = get_person(person_id)
    if not parent:
        return []
    children_ids = set(parent.get('children_ids', []))
    return [p for p in load_data().get('persons', []) if p['id'] in children_ids]


def get_generation(number: int) -> list[dict]:
    """Return all persons belonging to a given generation number."""
    return [p for p in load_data().get('persons', []) if p.get('generation') == number]


def get_max_generation() -> int:
    """Return the highest generation number present in the dataset."""
    persons = load_data().get('persons', [])
    if not persons:
        return 1
    return max(p.get('generation', 1) for p in persons)


def search_by_name(query: str) -> list[dict]:
    """Case-insensitive search across both Arabic and English names."""
    query_lower = query.lower().strip()
    if not query_lower:
        return []
    return [
        p for p in load_data().get('persons', [])
        if query_lower in p.get('name_en', '').lower()
        or query_lower in p.get('name_ar', '')
    ]


def filter_by_type(type_name: str) -> list[dict]:
    """Return all persons of a given category type (prophet, companion, etc.)."""
    if not type_name or type_name == 'all':
        return load_data().get('persons', [])
    return [p for p in load_data().get('persons', []) if p.get('type') == type_name]


def get_path_to_root(person_id: str) -> list[str]:
    """
    Return [person_id, father_id, grandfather_id, ..., root_id].
    Walks up the tree following father_id links.
    """
    path: list[str] = []
    current_id: Optional[str] = person_id
    seen: set[str] = set()
    while current_id and current_id not in seen:
        path.append(current_id)
        seen.add(current_id)
        person = get_person(current_id)
        if not person:
            break
        current_id = person.get('father_id')
    return path


def find_common_ancestor(
    person_ids: list[str],
) -> tuple[Optional[str], set[str]]:
    """
    Find the lowest common ancestor (LCA) among the given persons.

    Returns:
        (ancestor_id, highlighted_ids)
        - ancestor_id: ID of the LCA, or None if none found
        - highlighted_ids: every person on any path from a selected person
          up to (and including) the ancestor
    """
    if len(person_ids) < 2:
        return None, set(person_ids)

    paths = [get_path_to_root(pid) for pid in person_ids]
    path_sets = [set(p) for p in paths]

    # Intersection gives all persons that appear in every path (common ancestors)
    common = path_sets[0].copy()
    for s in path_sets[1:]:
        common &= s

    if not common:
        return None, set(person_ids)

    # Lowest common ancestor = the one with the highest generation number
    candidates = [get_person(pid) for pid in common]
    candidates = [p for p in candidates if p]
    ancestor = max(candidates, key=lambda p: p.get('generation', 0))
    ancestor_id = ancestor['id']

    # Collect all person IDs on any path from a selected person to the ancestor
    highlighted: set[str] = set()
    for path in paths:
        for pid in path:
            highlighted.add(pid)
            if pid == ancestor_id:
                break

    return ancestor_id, highlighted


def get_stats() -> dict:
    """Return computed statistics from live data."""
    persons = load_data().get('persons', [])
    return {
        'total': len(persons),
        'generations': get_max_generation(),
        'by_type': {
            'prophet': sum(1 for p in persons if p.get('type') == 'prophet'),
            'companion': sum(1 for p in persons if p.get('type') == 'companion'),
            'poet': sum(1 for p in persons if p.get('type') == 'poet'),
            'leader': sum(1 for p in persons if p.get('type') == 'leader'),
            'scholar': sum(1 for p in persons if p.get('type') == 'scholar'),
        },
    }
