from nicegui import ui
from ui.pages.landing import create_landing_page
from ui.pages.tree_view import create_tree_view_page


@ui.page('/')
def landing_page():
    create_landing_page()


@ui.page('/tree')
def tree_page():
    create_tree_view_page()


ui.run(
    title='Arab Genealogy Tree',
    language='ar',
    storage_secret='family-tree-secret-key-2024-dev-testing',
    favicon='🌳',
    port=9091
)