from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE
from typing import Callable, Optional


def open_person_modal(
    person: dict,
    language: str = DEFAULT_LANGUAGE,
    favorites: Optional[set] = None,
    on_favorite_toggle: Optional[Callable[[str], None]] = None,
) -> None:
    """Open a NiceGUI dialog showing full person details."""
    if favorites is None:
        favorites = set()

    name_key = 'name_ar' if language == 'ar' else 'name_en'
    desc_key = 'description_ar' if language == 'ar' else 'description_en'
    direction = 'rtl' if language == 'ar' else 'ltr'
    text_align = 'text-right' if language == 'ar' else 'text-left'

    name        = person.get(name_key) or person.get('name_en', '—')
    title       = person.get('title', '')
    description = (person.get(desc_key) or '').strip()
    type_key    = person.get('type', 'companion')
    gen_num     = person.get('generation', '')
    birth       = person.get('birth_year') or get_text('unknown', language)
    death       = person.get('death_year') or get_text('unknown', language)
    person_id   = person.get('id', '')
    is_fav      = person_id in favorites

    type_label = get_text(f'type_{type_key}', language)

    # Badge color per type
    _BADGE = {
        'prophet':   'bg-emerald-100 text-emerald-800',
        'companion': 'bg-blue-100    text-blue-800',
        'poet':      'bg-amber-100   text-amber-800',
        'leader':    'bg-red-100     text-red-800',
        'scholar':   'bg-purple-100  text-purple-800',
    }
    badge_class = _BADGE.get(type_key, 'bg-gray-100 text-gray-800')

    with ui.dialog().props('persistent') as dialog, ui.card().classes(
        'w-full max-w-lg rounded-2xl p-0 overflow-hidden'
    ):
        # Colored top bar matching the type
        _TOP_BAR = {
            'prophet':   'bg-emerald-500',
            'companion': 'bg-blue-500',
            'poet':      'bg-amber-500',
            'leader':    'bg-red-500',
            'scholar':   'bg-purple-500',
        }
        top_color = _TOP_BAR.get(type_key, 'bg-gray-400')

        with ui.element('div').classes(
            f'{top_color} px-6 py-4 flex items-start justify-between'
        ).props(f'dir="{direction}"'):
            with ui.column().classes('gap-1'):
                ui.label(name).classes(
                    'text-white text-2xl font-bold leading-tight'
                )
                if title:
                    ui.label(title).classes('text-white/80 text-sm')
            ui.button(
                icon='close',
                on_click=dialog.close,
            ).props('flat round').classes('text-white')

        # Body
        with ui.element('div').classes(
            'px-6 py-5 bg-white dark:bg-slate-800'
        ).props(f'dir="{direction}"'):

            # Type badge + generation
            with ui.row().classes('gap-3 items-center mb-4'):
                ui.label(type_label).classes(
                    f'px-3 py-1 rounded-full text-sm font-semibold {badge_class}'
                )
                if gen_num:
                    gen_text = (
                        f"Gen {gen_num}" if language == 'en'
                        else f"الجيل {gen_num}"
                    )
                    ui.label(gen_text).classes(
                        'text-xs text-gray-500 dark:text-gray-400 '
                        'border border-gray-300 dark:border-gray-600 '
                        'px-2 py-0.5 rounded-full'
                    )

            # Birth / Death years
            with ui.row().classes('gap-6 mb-4'):
                with ui.column().classes('gap-0.5'):
                    ui.label(get_text('birth_year', language)).classes(
                        'text-xs text-gray-400 uppercase tracking-wide'
                    )
                    ui.label(str(birth)).classes(
                        'text-sm font-medium text-gray-700 dark:text-gray-200'
                    )
                with ui.column().classes('gap-0.5'):
                    ui.label(get_text('death_year', language)).classes(
                        'text-xs text-gray-400 uppercase tracking-wide'
                    )
                    ui.label(str(death)).classes(
                        'text-sm font-medium text-gray-700 dark:text-gray-200'
                    )

            # Biography
            if description:
                ui.label(get_text('biography', language)).classes(
                    'text-xs text-gray-400 uppercase tracking-wide mb-1'
                )
                ui.label(description).classes(
                    f'text-gray-700 dark:text-gray-200 text-sm '
                    f'leading-relaxed {text_align}'
                )

            # Favorite toggle button
            if on_favorite_toggle:
                fav_label = (
                    get_text('remove_favorite', language) if is_fav
                    else get_text('add_favorite', language)
                )
                fav_icon  = 'star' if is_fav else 'star_border'
                fav_color = (
                    'text-amber-500' if is_fav
                    else 'text-gray-400 hover:text-amber-400'
                )

                def toggle_fav():
                    on_favorite_toggle(person_id)
                    dialog.close()

                with ui.row().classes('mt-4 justify-end'):
                    ui.button(
                        fav_label,
                        icon=fav_icon,
                        on_click=toggle_fav,
                    ).props('flat no-caps').classes(f'text-sm {fav_color}')

    dialog.open()
