# 🌳 Arab Genealogy Tree | شجرة أنساب العرب
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![NiceGUI](https://img.shields.io/badge/NiceGUI-Latest-green.svg)](https://nicegui.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()
> **🚧 Project Status: In Active Development**

An interactive web application to explore the complete genealogy tree of Arabs, starting from Prophet Ibrahim (PBUH), featuring comprehensive profiles of historical personalities including poets, companions, leaders, scholars, and many others.

تطبيق ويب تفاعلي لاستكشاف شجرة الأنساب الكاملة للعرب، بدءاً من النبي إبراهيم عليه السلام، مع عرض شامل للشخصيات التاريخية من شعراء وصحابة وقادة وعلماء وغيرهم.

## ✨ Features | المميزات

### Current Features (v0.1)
- 🌍 **Bilingual Support** - Arabic and English interface
- 🌓 **Dark/Light Mode** - Toggle between themes
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Beautiful Landing Page** - Intuitive and welcoming interface

### Planned Features
- 🌳 **Complete Genealogy Tree** - Starting from Prophet Ibrahim (PBUH)
- ⭐ **Highlighted Personalities** - Special marking for:
  - 🟢 Prophets (الأنبياء)
  - 🔵 Companions (الصحابة)
  - 🟡 Poets (الشعراء)
  - 🔴 Leaders (القادة)
  - 🟣 Scholars (العلماء)
  - And many more...
- 🔍 **Progressive Loading** - Load genealogy data layer by layer
- 📖 **Detailed Profiles** - Biography, achievements, and historical context
- 🔎 **Advanced Search** - Find any personality by name, type, or era
- 📊 **Statistics Dashboard** - Insights about generations and personalities
- 🗺️ **Geographic View** - Map of birthplaces and travels
- 📥 **Export Functionality** - Save tree sections as images/PDFs

## 🎯 Project Vision

This project aims to create a comprehensive, accessible, and interactive database of Arab genealogy and historical personalities. By combining historical accuracy with modern technology, we preserve and share this invaluable heritage with future generations.

يهدف هذا المشروع إلى إنشاء قاعدة بيانات شاملة ومتاحة وتفاعلية لأنساب العرب والشخصيات التاريخية. من خلال الجمع بين الدقة التاريخية والتكنولوجيا الحديثة، نحفظ ونشارك هذا التراث القيّم مع الأجيال القادمة.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/youssef-abbih/family-tree-app.git
cd family-tree-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

5. Open your browser and navigate to:
```
http://localhost:8080
```

## 📁 Project Structure
```
family-tree-app/
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
│
├── config/
│   └── settings.py        # Application settings and constants
│
├── data/
│   ├── translations.py    # Bilingual text content
│   └── family_tree.json   # [Planned] Genealogy data
│
├── models/
│   └── person.py          # [Planned] Person data model
│
├── services/
│   └── tree_service.py    # [Planned] Business logic
│
└── ui/
    ├── pages/
    │   ├── landing.py     # Landing page
    │   └── tree_view.py   # [Planned] Interactive tree view
    │
    └── components/
        ├── header.py      # App header with controls
        ├── hero_section.py
        ├── stats_cards.py
        ├── about_section.py
        ├── person_card.py # [Planned]
        └── modal.py       # [Planned]
```

## 🛠️ Technologies Used

- **[NiceGUI](https://nicegui.io/)** - Python-based web UI framework
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **Python 3.10+** - Programming language
- **JSON** - Data storage (considering SQLite for future scalability)

## 📊 Current Progress

- [x] Project setup and architecture
- [x] Landing page with bilingual support
- [x] Dark/Light mode toggle
- [x] Language switcher with persistence
- [x] Responsive design foundation
- [ ] Data collection and validation (In Progress)
- [ ] Interactive tree visualization
- [ ] Person profile pages
- [ ] Search and filtering system
- [ ] Data for 50+ generations
- [ ] Profiles for 1000+ personalities
- [ ] Mobile optimization
- [ ] Performance optimization

## 🎯 Roadmap

### Phase 1: Foundation ✅ (Current)
- Landing page and UI framework
- Multi-language support
- Theme system

### Phase 2: Core Features 🔄 (Next)
- Basic tree visualization
- Data structure implementation
- Progressive loading system
- Person detail modals

### Phase 3: Enhancement
- Advanced search and filtering
- Statistics dashboard
- Interactive features
- Performance optimization

### Phase 4: Polish & Launch
- Complete data validation
- Mobile optimization
- Documentation
- User testing
- Public release

## 🤝 Contributing

This project is in active development and contributions are highly welcome! Whether you're a developer, historian, or just passionate about Arab heritage, there are many ways to contribute:

### How to Contribute:
- 📚 **Historical Data** - Help verify and add genealogy information
- 💻 **Code** - Implement new features or fix bugs
- 🎨 **Design** - Improve UI/UX
- 📖 **Documentation** - Improve guides and documentation
- 🌍 **Translation** - Help with additional languages
- 🐛 **Testing** - Report bugs and suggest improvements

### Steps:
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Data Sources

The genealogy data will be compiled from authentic Islamic and historical sources including:
- **Jamharat Ansab al-Arab** (جمهرة أنساب العرب) - Ibn Hazm
- **Nasab Quraysh** (نسب قريش) - Al-Zubairi
- **Al-Tabaqat al-Kubra** (الطبقات الكبرى) - Ibn Sa'd
- **Tarikh al-Tabari** (تاريخ الطبري)
- Islamic biographical dictionaries and scholarly references

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the Islamic scholars and historians who preserved this knowledge through centuries
- Inspired by the need to make Arab genealogy accessible to modern audiences
- Built with [NiceGUI](https://nicegui.io/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)

## ⚠️ Disclaimer

This project aims for historical accuracy based on authenticated sources. However, genealogy records, especially for ancient times, may have varying accounts. We strive to present the most widely accepted information while acknowledging scholarly differences when they exist.

## 📧 Contact

Project Link: [https://github.com/youssef-abbih/family-tree-app](https://github.com/youssef-abbih/family-tree-app)

---

**🚧 This is a work in progress. Star ⭐ the repo to follow development!**

Made with ❤️ for preserving Arab heritage | صُنع بحب للحفاظ على التراث العربي