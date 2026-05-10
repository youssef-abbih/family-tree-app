from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE


# (type key, border color class, bg color class)
_LEGEND_ITEMS = [
    ('prophet',   'border-emerald-500', 'bg-emerald-500'),
    ('companion', 'border-blue-500',    'bg-blue-500'),
    ('poet',      'border-amber-500',   'bg-amber-500'),
    ('leader',    'border-red-500',     'bg-red-500'),
    ('scholar',   'border-purple-500',  'bg-purple-500'),
]


def create_legend(language: str = DEFAULT_LANGUAGE) -> None:
    """Horizontal color-coding legend bar shown above the tree."""
    direction = 'rtl' if language == 'ar' else 'ltr'

    with ui.element('div').classes(
        'w-full flex flex-wrap items-center gap-4 px-6 py-3 '
        'bg-white dark:bg-slate-800 border-b border-amber-200 '
        'dark:border-slate-700'
    ).props(f'dir="{direction}"'):

        ui.label(get_text('legend', language)).classes(
            'text-xs font-bold text-amber-900 dark:text-amber-300 uppercase tracking-wide'
        )

        for type_key, _, dot_class in _LEGEND_ITEMS:
            label = get_text(f'type_{type_key}', language)
            with ui.element('div').classes('flex items-center gap-1.5'):
                ui.element('div').classes(
                    f'w-3 h-3 rounded-full {dot_class}'
                )
                ui.label(label).classes(
                    'text-xs text-gray-700 dark:text-gray-300'
                )
