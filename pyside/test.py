# coding: utf-8
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import Slider, CardWidget, ScrollArea, FluentWindow, FluentIcon, SubtitleLabel, BodyLabel


class DataMonitorInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('dataMonitorInterface')
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.sliders = {}

        self.__initWidget()
        self.__initLayout()

    def __initWidget(self):
        self.view.setObjectName('dataMonitorView')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(20)

    def __initLayout(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = SubtitleLabel('力控参数调节')
        layout.addWidget(title)

        channels = ['LF', 'LB', 'RF', 'RB']

        for channel in channels:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)

            label = BodyLabel(channel)
            label.setFixedWidth(30)

            slider = Slider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(0)

            self.sliders[channel] = slider
            slider.valueChanged.connect(lambda v, ch=channel: self.on_slider_changed(v, ch))

            row_layout.addWidget(label)
            row_layout.addWidget(slider)

            layout.addWidget(row)

        self.vBoxLayout.addWidget(card)

    def on_slider_changed(self, value, channel):
        print(f'{channel}: {value}')


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.__initWindow()
        self.__initNavigation()

    def __initWindow(self):
        self.resize(400, 300)
        self.setWindowTitle('滑动条测试')

    def __initNavigation(self):
        self.dataMonitorInterface = DataMonitorInterface(self)
        self.addSubInterface(
            self.dataMonitorInterface,
            FluentIcon.SPEED_HIGH,
            '测试'
        )


def main():
    app = QApplication(sys.argv)
    qss_file = Path(__file__).parent / 'resource' / 'light' / 'demo.qss'
    if qss_file.exists():
        with open(qss_file, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())

    w = MainWindow()
    w.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
