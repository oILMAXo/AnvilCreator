# Anvil Creator

Визуальный редактор рецептов ковки на наковальне и лепки из глины для игры Vintage Story.

Приложение позволяет рисовать рецепты на сетке 16×16 (до 16 слоёв), видеть 3D-превью результата в реальном времени и экспортировать готовый JSON-файл рецепта, который можно сразу использовать в моде.

## Возможности

- Сетка 16×16, 16 слоёв с переключением через кнопки, клавиши или колёсико мыши
- Кисти 1×1, 2×2, 3×3 и резинки 1×1, 2×2, 9×9
- Полупрозрачное отображение заполненных клеток на соседних слоях
- 3D-превью с вращением мышью
- Подсчёт вокселей и необходимых слитков (42 вокселя = 1 слиток)
- Режимы: ковка (smithing) и лепка из глины (clay forming)
- Экспорт в JSON, совместимый с Vintage Story
- Сохранение/загрузка проектов
- Импорт существующих рецептов из JSON
- Drag & drop файлов
- 3 цветовые темы, 2 языка (RU/EN)
- Горячие клавиши для всех основных действий

## Автор

Идея и концепция: **ilmax** ([oILMAXo](https://github.com/oILMAXo))

Разработка: **Claude** (Anthropic), модель Claude Opus 4

## Технологии

- Python 3.11 + pywebview (десктопное окно)
- HTML/CSS/JS (интерфейс, единый файл)
- PyInstaller (сборка в .exe)

## Запуск

Запустить `AnvilCreator.exe`. Установка не требуется.

Для запуска из исходников:
```
pip install pywebview
python src/anvil_creator_app.py
```

---

# Anvil Creator (English)

Visual editor for smithing and clay forming recipes for the game Vintage Story.

The application lets you draw recipes on a 16×16 grid (up to 16 layers), see a real-time 3D preview of the result, and export a ready-to-use JSON recipe file for your mod.

## Features

- 16×16 grid, 16 layers with switching via buttons, keys, or mouse wheel
- Brushes 1×1, 2×2, 3×3 and erasers 1×1, 2×2, 9×9
- Ghost overlay showing filled cells on adjacent layers
- 3D preview with mouse rotation
- Voxel count and ingot calculator (42 voxels = 1 ingot)
- Modes: smithing and clay forming
- JSON export compatible with Vintage Story
- Project save/load
- Import existing recipes from JSON
- Drag & drop file support
- 3 color themes, 2 languages (RU/EN)
- Keyboard shortcuts for all main actions

## Author

Idea and concept: **ilmax** ([oILMAXo](https://github.com/oILMAXo))

Development: **Claude** (Anthropic), Claude Opus 4 model

## Tech stack

- Python 3.11 + pywebview (desktop window)
- HTML/CSS/JS (UI, single file)
- PyInstaller (exe build)

## Running

Run `AnvilCreator.exe`. No installation required.

To run from source:
```
pip install pywebview
python src/anvil_creator_app.py
```
