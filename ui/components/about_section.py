from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE


def create_about(language: str = DEFAULT_LANGUAGE) -> None:
    """About section with project description and category chips."""
    direction = 'rtl' if language == 'ar' else 'ltr'
    text_align = 'text-right' if language == 'ar' else 'text-left'

    # Category chips: label and Tailwind color classes
    categories = [
        (get_text('type_prophet',   language), 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200'),
        (get_text('type_companion', language), 'bg-blue-100    text-blue-800    dark:bg-blue-900    dark:text-blue-200'),
        (get_text('type_poet',      language), 'bg-amber-100   text-amber-800   dark:bg-amber-900   dark:text-amber-200'),
        (get_text('type_leader',    language), 'bg-red-100     text-red-800     dark:bg-red-900     dark:text-red-200'),
        (get_text('type_scholar',   language), 'bg-purple-100  text-purple-800  dark:bg-purple-900  dark:text-purple-200'),
    ]

    with ui.element('section').classes(
        'w-full py-20 px-6 bg-amber-50 dark:bg-slate-900'
    ).props(f'dir="{direction}"'):

        with ui.element('div').classes('max-w-3xl mx-auto'):

            # Section title centered
            ui.label(get_text('about_title', language)).classes(
                'text-3xl md:text-4xl font-bold text-amber-900 dark:text-amber-100 '
                'mb-8 text-center'
            )

            # Description text
            ui.label(get_text('about_text', language).strip()).classes(
                f'text-amber-800 dark:text-amber-200 text-lg leading-relaxed '
                f'mb-10 {text_align}'
            )

            # Category chips row
            with ui.element('div').classes(
                'flex flex-wrap gap-3 justify-center'
            ):
                for label, color_classes in categories:
                    ui.label(label).classes(
                        f'px-4 py-2 rounded-full text-sm font-semibold {color_classes}'
                    )
