"""
Главный модуль игры с графическим интерфейсом.
Отвечает за отображение информации о герое и управление основными игровыми действиями.
"""
import sys
import os
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QTableWidget, QTableWidgetItem, QLabel, 
                            QProgressBar, QStatusBar, QGroupBox, QGridLayout, 
                            QSplitter, QFrame, QTabWidget, QMessageBox, 
                            QInputDialog, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from hero import HeroDog
from enemies import SmallEnemy, BigEnemy, SkilledEnemy, Boss
from inventory import Inventory

class MainWindow(QWidget):
    """
    Главное окно приложения.
    Отображает информацию о герое и предоставляет кнопки для основных игровых действий.
    """
    def __init__(self):
        """Инициализация главного окна."""
        super().__init__()
        # Создаем героя
        self.hero = HeroDog("Аркадий", 100)
        self.hero.initialize_inventory()
        self.hero.inventory.add_item("Лечебное зелье", 3)

        # Если у героя нет атрибута exp_to_level, добавляем его
        if not hasattr(self.hero, 'exp_to_level'):
            self.hero.exp_to_level = 10 * self.hero.level

        # Журнал боя
        self.battle_log = []
        self.initUI()

    def initUI(self):
        """
        Настройка пользовательского интерфейса.
        Создает таблицу с характеристиками героя и кнопки для игровых действий.
        """
        self.setWindowTitle('Арена')
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial;
                color: #333;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #3a76d8;
                border: 1px solid #2a66c8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
            QGroupBox {
                border: 2px solid #4a86e8;
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #4a86e8;
            }
            QProgressBar {
                border: 1px solid #bdbdbd;
                border-radius: 5px;
                text-align: center;
                height: 20px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4a86e8;
                width: 10px;
                margin: 0.5px;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
                selection-background-color: #4a86e8;
                border: 1px solid #bdbdbd;
                border-radius: 5px;
            }
            QLabel {
                font-size: 14px;
            }
            QStatusBar {
                background-color: #e0e0e0;
                color: #333;
                font-weight: bold;
            }
            QListWidget {
                border: 1px solid #bdbdbd;
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff;
            }
        """)

        # Основной макет
        self.main_layout = QVBoxLayout()

        # Заголовок игры с декоративными элементами
        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: #4a86e8; border-radius: 10px;")
        title_layout = QVBoxLayout(title_frame)
        title_label = QLabel("АРЕНА - БИТВА ВОИНОВ")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setStyleSheet("color: white; margin: 10px;")
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("Приключения Аркадия")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #f0f0f0; margin-bottom: 10px;")
        title_layout.addWidget(subtitle_label)

        self.main_layout.addWidget(title_frame)

        # Кнопка "Старт"
        self.start_button = QPushButton("Старт")
        self.start_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.start_button.clicked.connect(self.show_main_menu)
        self.main_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        # Устанавливаем основной макет для окна
        self.setLayout(self.main_layout)

    def show_main_menu(self):
        """
        Отображает меню с характеристиками героя и кнопками для действий.
        """
        # Удаляем кнопку "Старт"
        self.start_button.hide()
        # Создаем разделитель для информации о герое и действий
        content_layout = QHBoxLayout()

        # Левая панель - информация о герое
        hero_group = QGroupBox("Информация о герое")
        hero_layout = QVBoxLayout()

        # Имя героя с иконкой
        name_layout = QHBoxLayout()
        hero_icon_label = QLabel()
        # Здесь можно добавить иконку героя, если она есть
        # hero_icon_label.setPixmap(QPixmap("hero_icon.png").scaled(40, 40))
        name_layout.addWidget(hero_icon_label)
        name_label = QLabel(f"Имя: {self.hero.name}")
        name_label.setFont(QFont("Arial", 16, QFont.Bold))
        name_label.setStyleSheet("color: #4a86e8;")
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        hero_layout.addLayout(name_layout)

        # Уровень и опыт с улучшенным отображением
        level_layout = QHBoxLayout()
        level_label = QLabel(f"Уровень: {self.hero.level}")
        level_label.setFont(QFont("Arial", 14, QFont.Bold))
        level_layout.addWidget(level_label)
        hero_layout.addLayout(level_layout)

        exp_layout = QHBoxLayout()
        exp_label = QLabel("Опыт:")
        exp_layout.addWidget(exp_label)
        self.exp_progress = QProgressBar()
        self.exp_progress.setRange(0, self.hero.exp_to_level)
        self.exp_progress.setValue(self.hero.exp)
        self.exp_progress.setFormat("%v/%m XP")
        self.exp_progress.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #FFD700;
            }
        """)
        exp_layout.addWidget(self.exp_progress)
        hero_layout.addLayout(exp_layout)

        # Здоровье с улучшенным отображением
        health_layout = QHBoxLayout()
        health_label = QLabel("Здоровье:")
        health_layout.addWidget(health_label)

        self.health_progress = QProgressBar()
        self.health_progress.setRange(0, self.hero.max_hp)
        self.health_progress.setValue(self.hero.hp)
        self.health_progress.setFormat("%v/%m HP")
        self.health_progress.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        health_layout.addWidget(self.health_progress)
        hero_layout.addLayout(health_layout)

        hero_group.setLayout(hero_layout)
        content_layout.addWidget(hero_group)

        # Правая панель - кнопки действий
        actions_group = QGroupBox("Действия")
        actions_layout = QVBoxLayout()

        start_journey_button = QPushButton("Начать свой путь")
        settings_button = QPushButton("Настройки")
        tutorial_button = QPushButton("Обучение")
        authors_button = QPushButton("Авторы")

        actions_layout.addWidget(start_journey_button)
        actions_layout.addWidget(settings_button)
        actions_layout.addWidget(tutorial_button)
        actions_layout.addWidget(authors_button)

        actions_group.setLayout(actions_layout)
        content_layout.addWidget(actions_group)

        self.main_layout.addLayout(content_layout)

def main():
    """
    Основная функция запуска приложения.
    Создает экземпляр приложения и главного окна, запускает цикл обработки событий.
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()