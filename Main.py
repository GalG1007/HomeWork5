import csv
import os
import subprocess
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QSlider,
    QDoubleSpinBox,
    QPushButton,
    QFrame,
    QAbstractSpinBox,
    QComboBox,
    QMessageBox,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Body import Body



class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About - Heat Transfer")
        self.setFixedSize(420, 400)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Heat Conduction Simulation")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #0F172A;")
        layout.addWidget(title_label)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_path = os.path.join(os.path.dirname(__file__), "heat_conduction.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                320, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("[ Place heat_conduction.png in HomeWork5 ]")
            image_label.setStyleSheet(
                "border: 1px dashed #94A3B8; padding: 28px; color: #64748B; border-radius: 8px;"
            )
        layout.addWidget(image_label)

        desc_label = QLabel(
            "Physics on Computer - Heat Transfer Project\n"
            "Created by: Gal Greenhouse\n"
            "Simulates conductive heat transfer between two physical bodies."
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        
        github_url = "https://github.com/GalG1007/HomeWork5"
        link_label = QLabel(
            f'<a href="{github_url}" style="color: #2563EB; font-weight: bold;">'
            f"GitHub Project Repository</a>"
        )
        link_label.setAlignment(Qt.AlignCenter)
        link_label.setOpenExternalLinks(True)
        layout.addWidget(link_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)



class GraphWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Graph Window")
        self.resize(740, 480)
        self.setupUI()

    def setupUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self._format_axes()
        main_layout.addWidget(self.canvas, stretch=3)

        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(12)

        self.body_selector = QComboBox()
        self.body_selector.addItems(["Body 1", "Body 2"])
        controls_layout.addWidget(self.body_selector)

        self.draw_button = QPushButton("Draw")
        self.draw_button.clicked.connect(self.draw_graph)
        controls_layout.addWidget(self.draw_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_graph)
        controls_layout.addWidget(self.clear_button)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        controls_layout.addWidget(self.export_button)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout, stretch=1)

    def _format_axes(self):
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.figure.tight_layout()

    def draw_graph(self):
        
        pass

    def clear_graph(self):
        
        pass

    def export_to_csv(self):
        
        pass



class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heat Transfer")
        self.setFixedSize(620, 440)

        
        self.graph_window = GraphWindow(self)
        self.about_window = AboutWindow()

        
        self.body1 = None
        self.body2 = None
        self.dt = 0.05
        self.elapsed_time = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

       
        self.timer = QTimer(self)
        self.timer.setInterval(int(self.dt * 1000))
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        
        top_layout = QHBoxLayout()
        top_layout.setSpacing(14)

        self.left_temp_slider = QSlider(Qt.Vertical)
        self.left_temp_slider.setRange(0, 200)
        self.left_temp_slider.setValue(200)
        self.left_temp_slider.setFixedHeight(170)
        self.left_temp_slider.valueChanged.connect(self.left_temperature_changed)
        top_layout.addWidget(self.left_temp_slider)

        self.left_body_frame = QFrame()
        self.left_body_frame.setFixedSize(115, 170)
        self.left_body_frame.setStyleSheet(
            "background-color: rgb(255, 0, 0); border-radius: 8px; border: 1px solid #334155;"
        )
        top_layout.addWidget(self.left_body_frame)

        center_top_layout = QVBoxLayout()
        center_top_layout.setAlignment(Qt.AlignCenter)
        center_top_layout.setSpacing(10)

        cond_label = QLabel("Conductivity")
        cond_label.setAlignment(Qt.AlignCenter)
        cond_label.setObjectName("sectionTitle")
        center_top_layout.addWidget(cond_label)

        self.conductivity_spinbox = QDoubleSpinBox()
        self.conductivity_spinbox.setRange(0.01, 1000.0)
        self.conductivity_spinbox.setDecimals(2)
        self.conductivity_spinbox.setSingleStep(0.1)
        self.conductivity_spinbox.setValue(1.00)
        self.conductivity_spinbox.setSuffix(" J/s°C")
        self.conductivity_spinbox.setFixedWidth(120)
        center_top_layout.addWidget(self.conductivity_spinbox, alignment=Qt.AlignCenter)

        self.conductor_bar = QFrame()
        self.conductor_bar.setObjectName("conductorBar")
        self.conductor_bar.setFixedSize(170, 28)
        center_top_layout.addWidget(self.conductor_bar, alignment=Qt.AlignCenter)

        top_layout.addLayout(center_top_layout)

        self.right_body_frame = QFrame()
        self.right_body_frame.setFixedSize(115, 170)
        self.right_body_frame.setStyleSheet(
            "background-color: rgb(0, 0, 0); border-radius: 8px; border: 1px solid #334155;"
        )
        top_layout.addWidget(self.right_body_frame)

        self.right_temp_slider = QSlider(Qt.Vertical)
        self.right_temp_slider.setRange(0, 200)
        self.right_temp_slider.setValue(0)
        self.right_temp_slider.setFixedHeight(170)
        self.right_temp_slider.valueChanged.connect(self.right_temperature_changed)
        top_layout.addWidget(self.right_temp_slider)

        main_layout.addLayout(top_layout)


        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        left_params = QGridLayout()
        left_params.setVerticalSpacing(10)
        left_params.setHorizontalSpacing(10)

        self.left_temp_display = self._create_temp_display(200.0)
        self.left_mass_spinbox = self._create_param_spinbox(10.00, " kg")
        self.left_hcap_spinbox = self._create_param_spinbox(0.40, " J/kg°C")

        left_params.addWidget(QLabel("Temp."), 0, 0)
        left_params.addWidget(self.left_temp_display, 0, 1)
        left_params.addWidget(QLabel("Mass"), 1, 0)
        left_params.addWidget(self.left_mass_spinbox, 1, 1)
        left_params.addWidget(QLabel("H. Cap."), 2, 0)
        left_params.addWidget(self.left_hcap_spinbox, 2, 1)
        bottom_layout.addLayout(left_params)

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setAlignment(Qt.AlignCenter)

        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setObjectName("startStopButton")
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.setFixedWidth(130)
        self.start_stop_button.toggled.connect(self.start_stop_button_method)
        buttons_layout.addWidget(self.start_stop_button)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setFixedWidth(130)
        self.graphs_button.clicked.connect(self.open_graph_window)
        buttons_layout.addWidget(self.graphs_button)

        self.about_button = QPushButton("About")
        self.about_button.setFixedWidth(130)
        self.about_button.clicked.connect(self.open_about_window)
        buttons_layout.addWidget(self.about_button)

        bottom_layout.addLayout(buttons_layout)

        right_params = QGridLayout()
        right_params.setVerticalSpacing(10)
        right_params.setHorizontalSpacing(10)

        self.right_temp_display = self._create_temp_display(0.0)
        self.right_mass_spinbox = self._create_param_spinbox(10.00, " kg")
        self.right_hcap_spinbox = self._create_param_spinbox(0.40, " J/kg°C")

        right_params.addWidget(self.right_temp_display, 0, 0)
        right_params.addWidget(QLabel("Temp."), 0, 1)
        right_params.addWidget(self.right_mass_spinbox, 1, 0)
        right_params.addWidget(QLabel("Mass"), 1, 1)
        right_params.addWidget(self.right_hcap_spinbox, 2, 0)
        right_params.addWidget(QLabel("H. Cap."), 2, 1)
        bottom_layout.addLayout(right_params)

        main_layout.addLayout(bottom_layout)

    def _create_temp_display(self, default_val: float) -> QDoubleSpinBox:
        box = QDoubleSpinBox()
        box.setRange(0.0, 200.0)
        box.setDecimals(1)
        box.setValue(default_val)
        box.setSuffix(" °C")
        box.setReadOnly(True)
        box.setButtonSymbols(QAbstractSpinBox.NoButtons)
        box.setFixedWidth(115)
        return box

    def _create_param_spinbox(self, default_val: float, suffix: str) -> QDoubleSpinBox:
        box = QDoubleSpinBox()
        box.setRange(0.01, 10000.0)
        box.setDecimals(2)
        box.setSingleStep(0.1)
        box.setValue(default_val)
        box.setSuffix(suffix)
        box.setFixedWidth(115)
        return box

    def update_body_color(self, frame: QFrame, temperature: float):
        
        pass

    def left_temperature_changed(self):
        
        pass

    def right_temperature_changed(self):
        
        pass

    def start_stop_button_method(self):
        
        pass

    def timer_method(self):
        
        pass

    def open_graph_window(self):
        self.graph_window.show()
        self.graph_window.raise_()

    def open_about_window(self):
        self.about_window.show()
        self.about_window.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as style_file:
            app.setStyleSheet(style_file.read())

    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())