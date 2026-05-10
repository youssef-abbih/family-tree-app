from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE
from services.tree_service import get_stats, filter_by_type, search_by_name
from typing import Callable, Optional


_FILTER_TYPES = ['all', 'prophet', 'companion', 'poet', 'leader', 'scholar']


def create_sidebar(
    language: str = DEFAULT_LANGUAGE,
    favorites: Optional[set] = None,
    all_persons: Optional[list] = None,
    on_filter_change: Optional[Callable[[list[dict]], None]] = None,
    on_person_click: Optional[Callable[[dict], None]] = None,
) -> None:
    """
    Collapsible sidebar drawer.
    Opens on the RIGHT for Arabic (RTL) and LEFT for English (LTR).
    """
    if favorites is None:
        favorites = set()
    if all_persons is None:
        all_persons = []

    direction = 'rtl' if language == 'ar' else 'ltr'

    # Use the correct drawer side based on language direction
    drawer_fn = ui.right_drawer if language == 'ar' else ui.left_drawer

    with drawer_fn(value=True, bordered=True).classes(
        'bg-amber-50 dark:bg-slate-800 flex flex-col gap-4 p-4 '
        'border-amber-200 dark:border-slate-700 overflow-y-auto'
    ).props(f'dir="{direction}" width=280'):

        # ── Title ──────────────────────────────────────────────
        ui.label(get_text('sidebar_title', language)).classes(
            'text-base font-bold text-amber-900 dark:text-amber-200 '
            'border-b border-amber-200 dark:border-slate-600 pb-2'
        )

        # ── Search ─────────────────────────────────────────────
        def on_search(e):
            query = e.value.strip()
            if on_filter_change:
                results = search_by_name(query) if query else all_persons
                on_filter_change(results)

        ui.input(
            placeholder=get_text('search_placeholder', language),
        ).classes(
            'w-full bg-white dark:bg-slate-700 rounded-lg '
            'text-sm text-gray-800 dark:text-gray-100'
        ).props('outlined dense clearable').on('keyup', on_search)

        # ── Type filters ───────────────────────────────────────
        with ui.column().classes('gap-1 w-full'):
            for type_key in _FILTER_TYPES:
                label_key = 'filter_all' if type_key == 'all' else f'type_{type_key}'
                label = get_text(label_key, language)

                def make_filter_click(tk):
                    def handler():
                        if on_filter_change:
                            results = (
                                all_persons if tk == 'all'
                                else filter_by_type(tk)
                            )
                            on_filter_change(results)
                    return handler

                ui.button(
                    label,
                    on_click=make_filter_click(type_key),
                ).classes(
                    'w-full text-left text-sm font-medium rounded-lg px-3 py-2 '
                    'text-amber-900 dark:text-amber-200 '
                    'hover:bg-amber-200 dark:hover:bg-slate-600 '
                    'transition-colors duration-150'
                ).props('flat no-caps align=left')

        # ── Statistics ─────────────────────────────────────────
        ui.label(get_text('statistics', language)).classes(
            'text-xs font-bold text-gray-500 dark:text-gray-400 uppercase '
            'tracking-wide mt-2 border-t border-amber-200 dark:border-slate-600 pt-3'
        )

        stats = get_stats()
        with ui.element('div').classes('grid grid-cols-2 gap-2'):
            for type_key in ['prophet', 'companion', 'poet', 'leader', 'scholar']:
                count = stats['by_type'].get(type_key, 0)
                label = get_text(f'type_{type_key}', language)
                with ui.element('div').classes(
                    'flex justify-between text-xs '
                    'text-gray-600 dark:text-gray-300'
                ):
                    ui.label(label)
                    ui.label(str(count)).classes('font-bold')

        # ── Favorites ──────────────────────────────────────────
        ui.label(get_text('favorites', language)).classes(
            'text-xs font-bold text-gray-500 dark:text-gray-400 uppercase '
            'tracking-wide mt-2 border-t border-amber-200 dark:border-slate-600 pt-3'
        )

        fav_persons = [p for p in all_persons if p.get('id') in favorites]
        if fav_persons:
            with ui.column().classes('gap-1 w-full'):
                for person in fav_persons:
                    name_key = 'name_ar' if language == 'ar' else 'name_en'
                    name = person.get(name_key) or person.get('name_en', '—')

                    def make_fav_click(p):
                        def handler():
                            if on_person_click:
                                on_person_click(p)
                        return handler

                    ui.button(
                        f'⭐ {name}',
                        on_click=make_fav_click(person),
                    ).classes(
                        'w-full text-left text-xs rounded-lg px-3 py-1.5 '
                        'text-amber-900 dark:text-amber-200 '
                        'hover:bg-amber-200 dark:hover:bg-slate-600 '
                        'transition-colors duration-150'
                    ).props('flat no-caps align=left')
        else:
            ui.label(get_text('no_favorites', language)).classes(
                'text-xs text-gray-400 italic'
            )
