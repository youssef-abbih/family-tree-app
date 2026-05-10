from nicegui import app, ui
from config.settings import DEFAULT_LANGUAGE
from ui.components.header import create_header
from ui.components.hero_section import create_hero
from ui.components.stats_cards import create_stats
from ui.components.about_section import create_about


def create_landing_page() -> None:
    """Assemble the full landing page from its component parts."""
    language = app.storage.user.get('language', DEFAULT_LANGUAGE)

    create_header(language=language)

    with ui.element('main').classes('w-full flex-1'):
        create_hero(language=language)
        create_stats(language=language)
        create_about(language=language)

    direction = 'rtl' if language == 'ar' else 'ltr'
    with ui.footer().classes(
        'bg-amber-900 dark:bg-slate-950 text-amber-100 text-center py-5'
    ).props(f'dir="{direction}"'):
        ui.label('© 2024 Arab Genealogy Tree — شجرة أنساب العرب').classes(
            'text-sm'
        )
