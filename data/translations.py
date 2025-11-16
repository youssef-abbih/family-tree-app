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
    }
}


def get_text(key: str, lang: str = 'ar') -> str:
    """
    الحصول على النص حسب اللغة
    """
    return TRANSLATIONS.get(lang, {}).get(key, key)
