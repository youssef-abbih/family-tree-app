from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE


def create_hero(language: str = DEFAULT_LANGUAGE) -> None:
    """Full-screen hero section with title, subtitle, and CTA button."""
    direction = 'rtl' if language == 'ar' else 'ltr'

    with ui.element('section').classes(
        'w-full relative flex flex-col items-center justify-center min-h-[70vh] '
        'bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 '
        'dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 '
        'px-6 py-20 text-center overflow-hidden'
    ).props(f'dir="{direction}"'):

        # Decorative large faded tree emoji as background
        ui.label('🌳').classes(
            'absolute text-[20rem] opacity-5 select-none pointer-events-none '
            'top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2'
        )

        # Main title
        ui.label(get_text('hero_title', language)).classes(
            'relative text-5xl md:text-7xl font-bold '
            'text-amber-900 dark:text-amber-100 mb-6 leading-tight z-10'
        )

        # Subtitle
        ui.label(get_text('hero_subtitle', language)).classes(
            'relative text-xl md:text-2xl '
            'text-amber-700 dark:text-amber-300 mb-12 max-w-2xl z-10'
        )

        # CTA button navigates to /tree
        ui.button(
            get_text('cta_button', language),
            on_click=lambda: ui.navigate.to('/tree'),
        ).classes(
            'relative bg-amber-600 hover:bg-amber-700 active:bg-amber-800 '
            'text-white font-semibold px-12 py-4 rounded-full text-lg '
            'shadow-xl hover:shadow-2xl transform hover:scale-105 '
            'transition-all duration-300 z-10'
        ).props('no-caps')
