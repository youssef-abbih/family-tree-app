from nicegui import app, ui
from data.translations import get_text, TRANSLATIONS
from config.settings import DEFAULT_LANGUAGE

def create_header(language=DEFAULT_LANGUAGE):
    direction = 'rtl' if language == 'ar' else 'ltr'
    app_title = TRANSLATIONS[language]['app_title']
    toggle_theme = TRANSLATIONS[language]['toggle_theme']
    with ui.header().classes('bg-amber-100 dark:bg-slate-800 shadow-md').props(f'dir="{direction}"'):
        with ui.row().classes('w-full justify-between items-center px-6 py-3'):
            # القسم الأيمن: Logo + العنوان
            with ui.row().classes('gap-3 items-center'):
                ui.label("🌳").classes('text-3xl')
                ui.label(get_text(app_title, language)).classes('text-xl font-bold text-amber-900 dark:text-amber-100')

            # القسم الأيسر: الأزرار
            with ui.row().classes('gap-4 items-center'):
                # Dark mode toggle
                dark = ui.dark_mode()
                ui.button(icon='dark_mode', on_click=dark.toggle).props('flat round').classes(
                    'text-amber-900 dark:text-amber-100').tooltip(get_text(toggle_theme, language))

                # Language selector
                def on_language_change(e):
                    new_lang = e.value  # أو e.args حسب النسخة
                    app.storage.user['language'] = new_lang
                    ui.navigate.reload()
                ui.select(
                    options=['ar', 'en'],
                    value=language,
                    label='🌍'
                ).classes('w-24').props('dense outlined').on_value_change(on_language_change)