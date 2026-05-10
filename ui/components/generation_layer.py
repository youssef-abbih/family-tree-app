from collections import defaultdict
from nicegui import ui
from data.translations import get_text
from config.settings import DEFAULT_LANGUAGE
from services.tree_service import get_generation, get_person
from ui.components.person_card import create_person_card
from typing import Callable, Optional


def create_generation_layer(
    generation_number: int,
    persons: list[dict],
    language: str = DEFAULT_LANGUAGE,
    favorites: Optional[set] = None,
    on_card_click: Optional[Callable[[dict], None]] = None,
) -> None:
    """
    Render one generation grouped by parent, with tree connector lines
    showing which children belong to which father.
    """
    if favorites is None:
        favorites = set()

    direction = 'rtl' if language == 'ar' else 'ltr'
    gen_label = get_text('generation_label', language)

    with ui.element('div').classes('w-full').props(f'dir="{direction}"'):

        # ── Generation header ──────────────────────────────────
        with ui.element('div').classes('flex items-center gap-3 mb-6 px-2'):
            ui.label(f'{gen_label} {generation_number}').classes(
                'flex-shrink-0 text-xs font-bold uppercase tracking-widest '
                'text-amber-700 dark:text-amber-400 '
                'bg-amber-100 dark:bg-amber-900/40 '
                'px-3 py-1 rounded-full border border-amber-300 dark:border-amber-700'
            )
            ui.element('div').classes('flex-1 h-px bg-amber-200 dark:bg-slate-600')

        if not persons:
            ui.label(get_text('no_results', language)).classes(
                'text-center text-gray-400 py-8'
            )
            return

        # ── Group persons by father_id ─────────────────────────
        groups: dict[str, list[dict]] = defaultdict(list)
        for p in persons:
            key = p.get('father_id') or 'root'
            groups[key].append(p)

        # Order groups to match the left-to-right order of parents
        # from the previous generation so connectors align visually.
        if generation_number > 1:
            prev_gen = get_generation(generation_number - 1)
            ordered_keys = [p['id'] for p in prev_gen if p['id'] in groups]
        else:
            ordered_keys = []
        # Append any group whose father is not in the previous generation
        ordered_keys += [k for k in groups if k not in ordered_keys]

        # ── Render a horizontal row of parent-groups ───────────
        with ui.element('div').classes(
            'flex flex-wrap justify-center items-start gap-10 px-2 pb-6'
        ):
            for father_key in ordered_keys:
                if father_key not in groups:
                    continue
                children = groups[father_key]
                _render_family_group(
                    children=children,
                    father_key=father_key,
                    generation_number=generation_number,
                    language=language,
                    favorites=favorites,
                    on_card_click=on_card_click,
                )


# ── Helper ────────────────────────────────────────────────────────────────────

def _render_family_group(
    children: list[dict],
    father_key: str,
    generation_number: int,
    language: str,
    favorites: set,
    on_card_click,
) -> None:
    """
    Render a single group of siblings with tree-line connectors.

    Layout (one or more children):

        father (prev gen)
             │            ← vertical drop
        ─────┴─────       ← horizontal bar spanning all children
        │         │       ← individual drops
    [child1]  [child2]
    """
    name_key = 'name_ar' if language == 'ar' else 'name_en'

    with ui.element('div').classes('flex flex-col items-center'):

        # ── "Children of [parent]" label ──────────────────────
        if generation_number > 1:
            father = get_person(father_key)
            if father:
                parent_name = father.get(name_key) or father.get('name_en', '')
                label_text = (
                    f'أبناء {parent_name}' if language == 'ar'
                    else f'Children of {parent_name}'
                )
                ui.label(label_text).classes(
                    'text-xs text-amber-600 dark:text-amber-400 '
                    'font-medium italic mb-1'
                )

            # Vertical drop line from parent
            ui.element('div').classes(
                'w-0.5 h-8 bg-amber-300 dark:bg-amber-600'
            )

        # ── Cards ─────────────────────────────────────────────
        if len(children) == 1:
            # Single child — just the card, no horizontal bar needed
            child = children[0]
            create_person_card(
                person=child,
                language=language,
                on_click=on_card_click,
                is_favorite=child.get('id', '') in favorites,
            )
        else:
            # Multiple children — T-junction connector
            #
            # The `relative` wrapper lets us place the horizontal bar
            # with `position: absolute` so it doesn't disturb the flex layout
            # of the children row.  Each child then gets its own short drop.
            with ui.element('div').classes('relative flex gap-4 items-start'):

                # Horizontal bar (absolute, spans full width of this container)
                ui.element('div').style(
                    'position: absolute; top: 0; left: 0; right: 0; height: 2px;'
                ).classes('bg-amber-300 dark:bg-amber-600')

                # Individual children with their short drop lines
                for child in children:
                    with ui.element('div').classes('flex flex-col items-center'):
                        # Short drop connecting to the horizontal bar above
                        ui.element('div').classes(
                            'w-0.5 h-4 bg-amber-300 dark:bg-amber-600'
                        )
                        create_person_card(
                            person=child,
                            language=language,
                            on_click=on_card_click,
                            is_favorite=child.get('id', '') in favorites,
                        )
