import asyncio
from nicegui import app, ui
from config.settings import DEFAULT_LANGUAGE
from data.translations import get_text
from services.tree_service import (
    get_generation, get_max_generation,
    get_children, find_lca_multiple,
)
from services.data_loader import load_data
from ui.components.header import create_header
from ui.components.legend import create_legend
from ui.components.person_card import create_person_card
from ui.components.person_modal import open_person_modal
from ui.components.sidebar import create_sidebar


MAX_SELECTION = 6


# ── CSS injected once per page ────────────────────────────────────────────────
_TREE_CSS = """
<style>
/* ── Base tree layout ── */
.tree-children-row {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: flex-start;
    flex-wrap: nowrap;
}

/*
 * .tree-node wraps each person.
 * The ::before pseudo-element draws the horizontal sibling-connector bar.
 *
 *  first-child  →  bar only on right half   (left end-cap)
 *  last-child   →  bar only on left  half   (right end-cap)
 *  only-child   →  no bar (no siblings)
 *  middle nodes →  full-width bar
 */
.tree-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 0.75rem;
    position: relative;
}
.tree-node::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: #d6b87a;
}
.tree-node:first-child::before { left:  50%; }
.tree-node:last-child::before  { right: 50%; }
.tree-node:only-child::before  { display: none; }

/* ── RTL: flip first/last so bars connect correctly in Arabic ── */
[dir="rtl"] .tree-node:first-child::before { left: 0;   right: 50%; }
[dir="rtl"] .tree-node:last-child::before  { left: 50%; right: 0;   }
[dir="rtl"] .tree-node:only-child::before  { display: none; }

/* ── Vertical connector lines ── */
.tree-drop-to-card {
    width: 2px;
    height: 1rem;
    background: #d6b87a;
    flex-shrink: 0;
}
.tree-drop-from-card {
    width: 2px;
    height: 1.5rem;
    background: #d6b87a;
    flex-shrink: 0;
}

/* ── Highlighted path (ancestor comparison) — purple ── */
.tree-node-hl::before {
    background: #a855f7 !important;
    height: 3px;
}
.tree-drop-hl {
    background: #a855f7 !important;
    width: 3px;
}

/* ── Dark mode overrides ── */
.body--dark .tree-node::before,
.body--dark .tree-drop-to-card,
.body--dark .tree-drop-from-card {
    background: #78553a;
}
.body--dark .tree-node-hl::before,
.body--dark .tree-drop-hl {
    background: #c084fc !important;
}
</style>
"""


def create_tree_view_page() -> None:
    """Genealogy tree page: recursive layout, parent always above children."""
    language = app.storage.user.get('language', DEFAULT_LANGUAGE)
    direction = 'rtl' if language == 'ar' else 'ltr'

    ui.add_head_html(_TREE_CSS)

    # ── Page state ───────────────────────────────────────────────
    state = {
        'loaded_up_to': 1,
        'max_gen': get_max_generation(),
        'favorites': set(),
        'filtered_persons': None,   # None = full tree view
        # ancestor-comparison state
        'selected_ids': set(),      # cards clicked for comparison
        'highlighted_ids': set(),   # all persons on paths to ancestor
        'ancestor_id': None,        # the common ancestor
    }
    all_persons = load_data().get('persons', [])

    # refs holds UI element handles AND shared callbacks
    refs = {
        'tree': None,
        'load_btn': None,
        'counter': None,
        'on_select': None,
        'on_modal': None,
    }

    # ── Callbacks ────────────────────────────────────────────────

    def open_modal(person: dict) -> None:
        open_person_modal(
            person=person,
            language=language,
            favorites=state['favorites'],
            on_favorite_toggle=toggle_favorite,
        )

    def toggle_favorite(person_id: str) -> None:
        if person_id in state['favorites']:
            state['favorites'].discard(person_id)
        else:
            state['favorites'].add(person_id)
        _rebuild(state, language, refs)

    async def handle_select(person: dict) -> None:
        """Toggle selection and recompute highlighted ancestor path."""
        pid = person['id']
        already_selected = pid in state['selected_ids']

        # Block new selections when max reached (unless deselecting)
        if (
            not already_selected
            and len(state['selected_ids']) >= MAX_SELECTION
        ):
            msg = (
                f'الحد الأقصى {MAX_SELECTION} أشخاص'
                if language == 'ar'
                else f'Maximum {MAX_SELECTION} selections reached'
            )
            ui.notify(msg, type='warning', position='top', timeout=2000)
            return

        if already_selected:
            state['selected_ids'].discard(pid)
        else:
            state['selected_ids'].add(pid)

        ids = list(state['selected_ids'])
        if ids:
            ancestor_id, highlighted = await asyncio.to_thread(
                find_lca_multiple, ids
            )
            state['ancestor_id'] = ancestor_id
            state['highlighted_ids'] = highlighted
        else:
            state['ancestor_id'] = None
            state['highlighted_ids'] = set()

        _rebuild(state, language, refs)

    def clear_selection() -> None:
        state['selected_ids'].clear()
        state['highlighted_ids'].clear()
        state['ancestor_id'] = None
        _rebuild(state, language, refs)

    def handle_filter_change(filtered: list[dict]) -> None:
        state['filtered_persons'] = filtered
        state['selected_ids'].clear()
        state['highlighted_ids'].clear()
        state['ancestor_id'] = None
        _rebuild(state, language, refs)

    # Store callbacks so _rebuild can use them without parameters
    refs['on_select'] = handle_select
    refs['on_modal'] = open_modal

    # ── ESC key clears selection ──────────────────────────────────
    def on_key(e) -> None:
        if e.key == 'Escape' and state['selected_ids']:
            clear_selection()

    ui.keyboard(on_key=on_key)

    # ── Header + sidebar ─────────────────────────────────────────
    create_header(language=language)
    create_sidebar(
        language=language,
        favorites=state['favorites'],
        all_persons=all_persons,
        on_filter_change=handle_filter_change,
        on_person_click=open_modal,
    )

    # ── Page body ────────────────────────────────────────────────
    with ui.element('div').classes(
        'w-full bg-amber-50 dark:bg-slate-900 min-h-screen'
    ).props(f'dir="{direction}"'):

        create_legend(language=language)

        # ── Selection counter bar ─────────────────────────────────
        refs['counter'] = ui.element('div').classes('w-full')
        with refs['counter']:
            _render_counter(state, language, clear_selection)

        # Scroll wrapper
        with ui.element('div').classes('w-full overflow-x-auto'):
            with ui.element('div').classes(
                'min-w-full flex flex-col items-center py-6 px-4'
            ):
                refs['tree'] = ui.element('div')
                with refs['tree']:
                    _render_tree(state, language, handle_select, open_modal)

                refs['load_btn'] = ui.element('div').classes(
                    'flex justify-center py-8 w-full'
                )
                with refs['load_btn']:
                    _render_load_btn(state, language, refs)


# ── Counter bar ───────────────────────────────────────────────────────────────

def _render_counter(state: dict, language: str, clear_fn) -> None:
    """Show selection count and Clear All button."""
    n = len(state['selected_ids'])
    if n == 0:
        # Hint text when nothing selected
        hint = (
            'انقر على شخص لإظهار مساره حتى الجذر، '
            'أو اختر شخصين أو أكثر لإيجاد جدّهم المشترك'
            if language == 'ar'
            else
            'Click a card to trace its path to the root, '
            'or select 2+ cards to find their common ancestor'
        )
        ui.label(hint).classes(
            'text-center text-xs text-amber-600 dark:text-amber-400 '
            'italic py-2 px-4 w-full block'
        )
        return

    # Badge row
    with ui.element('div').classes(
        'flex items-center justify-center gap-3 py-2 px-4 w-full'
    ):
        count_label = (
            f'{n} / {MAX_SELECTION} محدد'
            if language == 'ar'
            else f'{n} / {MAX_SELECTION} selected'
        )
        ui.label(count_label).classes(
            'text-sm font-semibold text-purple-700 dark:text-purple-300 '
            'bg-purple-100 dark:bg-purple-900 '
            'px-3 py-1 rounded-full'
        )

        clear_label = 'مسح الكل' if language == 'ar' else 'Clear All'
        ui.button(
            clear_label, on_click=clear_fn, icon='close'
        ).classes(
            'text-sm text-purple-700 dark:text-purple-300 '
            'border border-purple-300 dark:border-purple-700 rounded-full '
            'px-4 py-1'
        ).props('flat no-caps')


# ── Tree rendering ────────────────────────────────────────────────────────────

def _render_tree(
    state: dict,
    language: str,
    on_select,
    on_modal,
) -> None:
    """Render the full recursive tree, or a flat filtered grid."""
    if state['filtered_persons'] is not None:
        _render_flat_grid(state, language, on_select, on_modal)
        return

    roots = get_generation(1)
    with ui.element('div').classes('tree-children-row'):
        for root in roots:
            _render_subtree(
                root, depth=0, state=state,
                language=language,
                on_select=on_select, on_modal=on_modal,
            )


def _render_subtree(
    person: dict,
    depth: int,
    state: dict,
    language: str,
    on_select,
    on_modal,
) -> None:
    """
    Recursively render a person and their children up to loaded_up_to depth.
    """
    pid = person['id']
    parent_id = person.get('father_id')

    is_selected = pid in state['selected_ids']
    is_ancestor = pid == state['ancestor_id']
    is_on_path = (
        pid in state['highlighted_ids']
        and not is_selected
        and not is_ancestor
    )
    is_max_reached = (
        len(state['selected_ids']) >= MAX_SELECTION
        and not is_selected
        and not is_ancestor
    )

    parent_hl = (
        parent_id in state['highlighted_ids'] if parent_id else False
    )
    self_hl = pid in state['highlighted_ids']

    node_class = (
        'tree-node'
        + (' tree-node-hl' if parent_hl and self_hl else '')
    )

    with ui.element('div').classes(node_class):

        if depth > 0:
            drop_class = (
                'tree-drop-to-card'
                + (' tree-drop-hl' if self_hl else '')
            )
            ui.element('div').classes(drop_class)

        create_person_card(
            person=person,
            language=language,
            on_click=on_select,
            on_info_click=on_modal,
            is_favorite=pid in state['favorites'],
            is_selected=is_selected,
            is_on_path=is_on_path,
            is_ancestor=is_ancestor,
            is_max_reached=is_max_reached,
        )

        if depth < state['loaded_up_to'] - 1:
            children = get_children(pid)
            if children:
                drop_class = (
                    'tree-drop-from-card'
                    + (' tree-drop-hl' if self_hl else '')
                )
                ui.element('div').classes(drop_class)
                with ui.element('div').classes('tree-children-row'):
                    for child in children:
                        _render_subtree(
                            child, depth + 1, state,
                            language, on_select, on_modal,
                        )


def _render_flat_grid(state, language, on_select, on_modal) -> None:
    """Flat grid shown when a search or type filter is active."""
    persons = state['filtered_persons'] or []
    if not persons:
        ui.label(get_text('no_results', language)).classes(
            'text-gray-400 text-center py-12'
        )
        return

    is_max_reached = len(state['selected_ids']) >= MAX_SELECTION

    with ui.element('div').classes(
        'grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 '
        'lg:grid-cols-5 gap-4'
    ):
        for person in persons:
            pid = person['id']
            is_selected = pid in state['selected_ids']
            create_person_card(
                person=person,
                language=language,
                on_click=on_select,
                on_info_click=on_modal,
                is_favorite=pid in state['favorites'],
                is_selected=is_selected,
                is_on_path=(
                    pid in state['highlighted_ids']
                    and not is_selected
                    and pid != state['ancestor_id']
                ),
                is_ancestor=pid == state['ancestor_id'],
                is_max_reached=(
                    is_max_reached and not is_selected
                ),
            )


# ── Load-next button ──────────────────────────────────────────────────────────

def _render_load_btn(state, language, refs) -> None:
    if state['loaded_up_to'] >= state['max_gen']:
        ui.label(get_text('no_more_generations', language)).classes(
            'text-amber-700 dark:text-amber-400 font-medium'
        )
        return

    next_gen = state['loaded_up_to'] + 1
    gen_label = get_text('generation_label', language)
    btn_label = (
        f"{get_text('load_next_generation', language)} "
        f"({gen_label} {next_gen})"
    )

    def load_next():
        state['loaded_up_to'] += 1
        _rebuild(state, language, refs)

    ui.button(btn_label, on_click=load_next).classes(
        'bg-amber-600 hover:bg-amber-700 text-white font-semibold '
        'px-10 py-3 rounded-full shadow-lg hover:shadow-xl '
        'transform hover:scale-105 transition-all duration-300'
    ).props('no-caps')


def _rebuild(state, language, refs) -> None:
    """Full re-render of counter + tree + load button."""
    if refs is None:
        return
    on_select = refs.get('on_select')
    on_modal = refs.get('on_modal')

    refs['counter'].clear()
    with refs['counter']:
        _render_counter(
            state, language,
            lambda: _clear_and_rebuild(state, language, refs),
        )

    refs['tree'].clear()
    with refs['tree']:
        _render_tree(state, language, on_select, on_modal)

    refs['load_btn'].clear()
    with refs['load_btn']:
        _render_load_btn(state, language, refs)


def _clear_and_rebuild(state, language, refs) -> None:
    """Helper: clear selection state then rebuild."""
    state['selected_ids'].clear()
    state['highlighted_ids'].clear()
    state['ancestor_id'] = None
    _rebuild(state, language, refs)
