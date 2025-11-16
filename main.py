from nicegui import app, ui
from ui.components.header import create_header  # absolute import
from config.settings import DEFAULT_LANGUAGE

@ui.page('/')
def landing_page():
    language = app.storage.user.get('language', 'ar')
    create_header(language=language)
    # باقي الصفحة...

ui.run(
    title='Arab Genealogy Tree',
    language='ar',
    storage_secret='family-tree-secret-key-2024-dev-testing'
)