import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QDesktopWidget
)
from PyQt5.QtCore import Qt, QTimer


class ResizableButtonsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.all_cards = []
        self.is_dice_mode = True  # True — кубик, False — карта
        self.animation_timer = None
        self.animation_interval = 50  # стартовый интервал (мс)
        self.animation_max_interval = 500  # максимальный интервал (мс)
        self.animation_step = 20  # на сколько увеличиваем интервал
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Valorant Map Picker")
        available_rect = QDesktopWidget().availableGeometry()
        self.setGeometry(available_rect)
        self.show()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(40)

        # Верхние карты
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        top_images = ["Abyss", "Ascent", "Bind", "Breeze", "Corrode", "Fracture"]
        for name in top_images:
            btn = self.create_card_button(name)
            top_layout.addWidget(btn)
        main_layout.addLayout(top_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Центральная кнопка — кубик / карта
        self.middle_btn = QPushButton()
        self.middle_btn.setCursor(Qt.PointingHandCursor)
        self.middle_btn.clicked.connect(self.middle_click)
        self.set_dice_image()
        main_layout.addWidget(self.middle_btn, alignment=Qt.AlignCenter)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Нижние карты
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)
        bottom_images = ["Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"]
        for name in bottom_images:
            btn = self.create_card_button(name)
            bottom_layout.addWidget(btn)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def create_card_button(self, name):
        btn = QPushButton()
        btn.setFixedSize(300, 169)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-image: url(images/{name}.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain;
            }}
        """)
        btn.clicked.connect(lambda _, b=btn, n=name: self.toggle_black(b, n))
        self.all_cards.append({
            "btn": btn,
            "name": name,
            "normal": f"images/{name}.png",
            "black": f"images/{name}-black.png",
            "is_black": False
        })
        return btn

    def toggle_black(self, btn, name):
        for card in self.all_cards:
            if card["btn"] == btn:
                card["is_black"] = not card["is_black"]
                img = card["black"] if card["is_black"] else card["normal"]
                btn.setStyleSheet(f"""
                    QPushButton {{
                        border: none;
                        background-image: url({img});
                        background-repeat: no-repeat;
                        background-position: center;
                        background-size: contain;
                    }}
                """)
                break

    def set_dice_image(self):
        self.is_dice_mode = True
        self.middle_btn.setEnabled(True)
        self.middle_btn.setFixedSize(96, 96)
        self.middle_btn.setCursor(Qt.PointingHandCursor)
        self.middle_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(images/Dice.png);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

    def middle_click(self):
        if self.is_dice_mode:
            self.start_animation()
        else:
            self.set_dice_image()

    def start_animation(self):
        self.is_dice_mode = False
        self.middle_btn.setEnabled(False)
        self.animation_interval = 50

        # Все карты без черно-белых (исключаем заблокированные)
        self.animation_sequence = [c for c in self.all_cards if not c["is_black"]]
        if not self.animation_sequence:
            self.set_dice_image()
            return

        # Выбираем финальную карту случайно
        self.final_card = random.choice(self.animation_sequence)

        if self.animation_timer is None:
            self.animation_timer = QTimer()
            self.animation_timer.timeout.connect(self.animate_step)

        self.animation_timer.start(self.animation_interval)

    def animate_step(self):
        # Показываем случайную карту
        card = random.choice(self.animation_sequence)
        self.middle_btn.setFixedSize(300, 169)
        self.middle_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-image: url({card['normal']});
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain;
            }}
        """)
        self.middle_btn.setCursor(Qt.PointingHandCursor)

        # Плавное замедление
        if self.animation_interval < self.animation_max_interval:
            self.animation_interval += self.animation_step
            self.animation_timer.setInterval(self.animation_interval)
        else:
            # Останавливаем анимацию и показываем финальную карту
            self.animation_timer.stop()
            self.middle_btn.setEnabled(True)
            self.show_final_card(self.final_card)

    def show_final_card(self, card):
        self.middle_btn.setFixedSize(300, 169)
        self.middle_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-image: url({card['normal']});
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain;
            }}
        """)
        self.middle_btn.setCursor(Qt.PointingHandCursor)
        self.is_dice_mode = False
        self.middle_btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResizableButtonsWindow()
    window.show()
    sys.exit(app.exec_())
