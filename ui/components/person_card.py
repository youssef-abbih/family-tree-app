import asyncio
from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE
from typing import Callable, Optional


# Card border + background per category type
_TYPE_CARD = {
    'prophet':   'border-emerald-500 bg-emerald-50  dark:bg-emerald-950',
    'companion': 'border-blue-500    bg-blue-50     dark:bg-blue-950',
    'poet':      'border-amber-500   bg-amber-50    dark:bg-amber-950',
    'leader':    'border-red-500     bg-red-50      dark:bg-red-950',
    'scholar':   'border-purple-500  bg-purple-50   dark:bg-purple-950',
}

# Badge pill color per category type
_TYPE_BADGE = {
    'prophet':   'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200',
    'companion': 'bg-blue-100    text-blue-800    dark:bg-blue-900    dark:text-blue-200',
    'poet':      'bg-amber-100   text-amber-800   dark:bg-amber-900   dark:text-amber-200',
    'leader':    'bg-red-100     text-red-800     dark:bg-red-900     dark:text-red-200',
    'scholar':   'bg-purple-100  text-purple-800  dark:bg-purple-900  dark:text-purple-200',
}

_FALLBACK_CARD  = 'border-gray-400 bg-gray-50 dark:bg-gray-900'
_FALLBACK_BADGE = 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'


def create_person_card(
    person: dict,
    language: str = DEFAULT_LANGUAGE,
    on_click: Optional[Callable] = None,
    on_info_click: Optional[Callable[[dict], None]] = None,
    is_favorite: bool = False,
    # Ancestor-comparison highlight states
    is_selected: bool = False,   # user clicked this card for comparison
    is_on_path: bool = False,    # on the path to the common ancestor
    is_ancestor: bool = False,   # IS the common ancestor
    is_max_reached: bool = False,  # selection limit hit, not selected
) -> None:
    """
    Render a single person card.

    Click the card body  → toggle selection (for ancestor highlighting).
    Click the ℹ button   → open person detail modal.
    """
    name_key  = 'name_ar' if language == 'ar' else 'name_en'
    type_key  = person.get('type', 'companion')
    name      = person.get(name_key) or person.get('name_en', '—')
    title     = person.get('title', '')
    gen_num   = person.get('generation', '')

    type_label  = get_text(f'type_{type_key}', language)
    card_class  = _TYPE_CARD.get(type_key,  _FALLBACK_CARD)
    badge_class = _TYPE_BADGE.get(type_key, _FALLBACK_BADGE)
    gen_label   = (
        f"Gen {gen_num}" if language == 'en' else f"الجيل {gen_num}"
    ) if gen_num else ''

    direction = 'rtl' if language == 'ar' else 'ltr'

    # Extra ring class based on selection / highlight state
    if is_ancestor:
        ring_class = 'ring-4 ring-purple-500 ring-offset-2 scale-105'
    elif is_selected:
        ring_class = 'ring-3 ring-purple-500 ring-offset-1'
    elif is_on_path:
        ring_class = 'ring-2 ring-purple-300 ring-offset-1'
    else:
        ring_class = ''

    # Dim card when max selections reached and this card is not selected
    dim_class = (
        'opacity-40 cursor-not-allowed'
        if is_max_reached and not is_selected and not is_ancestor
        else ''
    )

    async def handle_card_click():
        if on_click:
            result = on_click(person)
            if asyncio.iscoroutine(result):
                await result

    def handle_info_click(e):
        if on_info_click:
            on_info_click(person)

    with ui.card().classes(
        f'border-2 {card_class} {ring_class} {dim_class} '
        'rounded-xl p-3 cursor-pointer '
        'hover:shadow-xl hover:-translate-y-1 '
        'transition-all duration-300 min-w-[140px] max-w-[190px] w-full '
        'relative'
    ).props(f'dir="{direction}"').on('click', handle_card_click):

        # ── Info button (top-right corner, opens modal) ────────
        if on_info_click:
            with ui.element('div').classes(
                'absolute top-1 right-1' if language == 'en' else 'absolute top-1 left-1'
            ):
                ui.button(
                    icon='info',
                    on_click=handle_info_click,
                ).props('flat round dense').classes(
                    'text-gray-400 hover:text-amber-600 text-xs'
                )

        with ui.column().classes('gap-1.5 items-center text-center w-full pt-1'):

            # Crown for the common ancestor
            if is_ancestor:
                ui.label('👑').classes('text-base leading-none')
            elif is_selected:
                ui.label('✓').classes(
                    'text-xs font-bold text-purple-600 leading-none'
                )

            # Favorite star
            if is_favorite:
                ui.label('⭐').classes('text-xs leading-none')

            # Highlighted dot (from original data flag)
            if person.get('is_highlighted') and not is_ancestor and not is_selected:
                ui.element('div').classes(
                    'w-1.5 h-1.5 rounded-full bg-amber-500 mx-auto'
                )

            # Person name
            ui.label(name).classes(
                'font-bold text-gray-900 dark:text-gray-100 text-sm leading-snug'
            )

            # Honorific title
            if title:
                ui.label(title).classes(
                    'text-xs text-gray-500 dark:text-gray-400 leading-none'
                )

            # Category badge
            ui.label(type_label).classes(
                f'text-xs px-2 py-0.5 rounded-full font-medium {badge_class}'
            )

            # Generation label
            if gen_label:
                ui.label(gen_label).classes(
                    'text-xs text-gray-400 dark:text-gray-500'
                )
