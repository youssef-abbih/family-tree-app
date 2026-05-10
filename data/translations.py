"""
النصوص بالعربية والإنجليزية
"""

TRANSLATIONS = {
    'ar': {
        'app_title': 'شجرة أنساب العرب',
        'hero_title': 'رحلة عبر التاريخ',
        'hero_subtitle': 'من إسماعيل عليه السلام إلى محمد صلى الله عليه وسلم',
        'cta_button': 'ابدأ الاستكشاف',
        
        # Stats
        'stat_generations': 'جيل',
        'stat_personalities': 'شخصية',
        'stat_companions': 'صحابي',
        'stat_poets': 'شاعر',
        
        # About
        'about_title': 'نبذة عن المشروع',
        'about_text': '''
        مشروع شجرة أنساب العرب هو رحلة تفاعلية لاستكشاف أصول العرب
        من النبي إسماعيل عليه السلام وصولاً إلى النبي محمد صلى الله عليه وسلم.
        يهدف المشروع إلى حفظ التاريخ وتسهيل فهم الأنساب والعلاقات بين
        الشخصيات التاريخية المهمة.
        ''',
        
        # Header
        'toggle_theme': 'تبديل الوضع الليلي',
        'change_language': 'English',

        # Tree view - navigation
        'tree_title': 'شجرة الأنساب',
        'back_to_landing': 'الرئيسية',
        'load_next_generation': 'تحميل الجيل التالي',
        'no_more_generations': 'وصلت إلى آخر جيل',
        'generation_label': 'الجيل',

        # Tree view - sidebar
        'sidebar_title': 'الفلاتر والبحث',
        'search_placeholder': 'ابحث باسم الشخص...',
        'filter_all': 'الكل',
        'statistics': 'الإحصائيات',
        'favorites': 'المفضلة',
        'no_results': 'لا توجد نتائج',
        'no_favorites': 'لا توجد مفضلة',

        # Tree view - legend / types
        'legend': 'دليل الألوان',
        'type_prophet': 'نبي',
        'type_companion': 'صحابي',
        'type_poet': 'شاعر',
        'type_leader': 'قائد',
        'type_scholar': 'عالم',

        # Person modal
        'close': 'إغلاق',
        'biography': 'السيرة',
        'birth_year': 'سنة الميلاد',
        'death_year': 'سنة الوفاة',
        'children': 'الأبناء',
        'add_favorite': 'إضافة للمفضلة',
        'remove_favorite': 'إزالة من المفضلة',
        'unknown': 'غير معروف',
    },

    'en': {
        'app_title': 'Arab Genealogy Tree',
        'hero_title': 'A Journey Through History',
        'hero_subtitle': 'From Prophet Ismail (PBUH) to Prophet Muhammad (PBUH)',
        'cta_button': 'Start Exploring',
        
        # Stats
        'stat_generations': 'Generations',
        'stat_personalities': 'Personalities',
        'stat_companions': 'Companions',
        'stat_poets': 'Poets',
        
        # About
        'about_title': 'About the Project',
        'about_text': '''
        The Arab Genealogy Tree project is an interactive journey to explore
        the origins of Arabs from Prophet Ismail (PBUH) to Prophet Muhammad (PBUH).
        The project aims to preserve history and facilitate understanding of
        lineages and relationships between important historical figures.
        ''',
        
        # Header
        'toggle_theme': 'Toggle Dark Mode',
        'change_language': 'عربي',

        # Tree view - navigation
        'tree_title': 'Genealogy Tree',
        'back_to_landing': 'Home',
        'load_next_generation': 'Load Next Generation',
        'no_more_generations': 'You have reached the last generation',
        'generation_label': 'Generation',

        # Tree view - sidebar
        'sidebar_title': 'Filters & Search',
        'search_placeholder': 'Search by name...',
        'filter_all': 'All',
        'statistics': 'Statistics',
        'favorites': 'Favorites',
        'no_results': 'No results found',
        'no_favorites': 'No favorites yet',

        # Tree view - legend / types
        'legend': 'Legend',
        'type_prophet': 'Prophet',
        'type_companion': 'Companion',
        'type_poet': 'Poet',
        'type_leader': 'Leader',
        'type_scholar': 'Scholar',

        # Person modal
        'close': 'Close',
        'biography': 'Biography',
        'birth_year': 'Birth Year',
        'death_year': 'Death Year',
        'children': 'Children',
        'add_favorite': 'Add to Favorites',
        'remove_favorite': 'Remove from Favorites',
        'unknown': 'Unknown',
    }
}


def get_text(key: str, lang: str = 'ar') -> str:
    """
    الحصول على النص حسب اللغة
    """
    return TRANSLATIONS.get(lang, {}).get(key, key)
