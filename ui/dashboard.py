from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from reports.report_generator import create_pdf_report
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QDialog
import json
import os

from scanner.file_scanner import scan_directory
from scanner.pdf_reader import extract_pdf_text
from scanner.regex_detector import detect_sensitive_data
from scanner.ai_detector import detect_sensitive_entities


class Card(QFrame):

    def __init__(self, title, value, icon):
        super().__init__()

        self.setObjectName("card")
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        name = QLabel(f"{icon} {title}")
        self.value = QLabel(value)

        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            color:#d0d7de;
            """
        )

        layout.addWidget(name)
        layout.addWidget(self.value)

        self.setLayout(layout)



class Chart(QFrame):
    def __init__(self,title):
        super().__init__()
        self.setObjectName("card")
        self.setFixedHeight(170)
        layout=QVBoxLayout()
        label=QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.figure=Figure(figsize=(3,2), facecolor="#161b22")
        self.canvas=FigureCanvasQTAgg(self.figure)
        self.canvas.setStyleSheet("background:#161b22;")
        layout.addWidget(label)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def draw(self,values,labels,donut=False):
        self.figure.clear()
        ax=self.figure.add_subplot(111)
        ax.set_facecolor("#161b22")
        if donut:
            ax.pie(values,wedgeprops={"width":0.35})
        else:
            ax.pie(values,labels=labels)
        for t in ax.texts:
            t.set_color("#e6edf3")
        ax.axis("equal")
        self.canvas.draw()


class GhostTraceDashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.files = 0
        self.threats = 0
        self.risky = 0
        self.risk_score = 0
        self.categories = {}
        self.load_settings()

        self.setWindowTitle(
            "GhostTrace - Local Privacy Auditor"
        )

        self.resize(1300,750)

        self.create_ui()
    
    def load_settings(self):

        default = {
            "scan_mode":"Deep",

            "file_types":[
                "PDF",
                "TXT",
                "DOCX",
                "CSV",
                "JSON",
                "PY"
            ],

            "risk_level":5,

            "include_graphs":True,

            "include_ai":True,

            "theme":"Grey Professional"
        }

        if os.path.exists("settings.json"):

            with open(
                "settings.json",
                "r"
            ) as file:

                self.settings = json.load(file)

        else:

            self.settings = default

            self.save_settings_file()

    def save_settings_file(self):
        with open(
            "settings.json",
            "w"
        ) as file:
            json.dump(
                self.settings,
                file,
                indent=4
            )

    def create_ui(self):

        root = QHBoxLayout()

        # sidebar

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        side_layout = QVBoxLayout()


        logo = QLabel(
            "👻\nGhostTrace\nLocal Privacy Auditor"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo.setStyleSheet(
            """
            color:#d0d7de;
            font-size:18px;
            font-weight:bold;
            """
        )


        side_layout.addWidget(logo)


        for item in [
            "🏠 Dashboard",
            "🔍 Scan",
            "📄 Results",
            "📊 Risk Analysis",
            "⚙ Settings"
        ]:
            btn = QPushButton(item)
            btn.setObjectName("sideBtn")

            if "Scan" in item:
                btn.clicked.connect(self.pick_folder)

            elif "Results" in item:
                btn.clicked.connect(self.show_results)

            elif "Risk" in item:
                btn.clicked.connect(self.show_risk)

            elif "Dashboard" in item:
                btn.clicked.connect(self.show_dashboard)

            elif "Settings" in item:
                btn.clicked.connect(self.show_settings)

            side_layout.addWidget(btn)


        side_layout.addStretch()

        sidebar.setLayout(side_layout)



        # main

        main = QVBoxLayout()

        main.setContentsMargins(
            25,15,25,15
        )

        main.setSpacing(10)



        title = QLabel("Dashboard")

        title.setFont(
            QFont(
                "Arial",
                26,
                QFont.Weight.Bold
            )
        )

        subtitle = QLabel(
            "Overview of your privacy scan"
        )

        subtitle.setStyleSheet(
            "color:gray;"
        )


        main.addWidget(title)
        main.addWidget(subtitle)



        grid = QGridLayout()


        self.c1 = Card(
            "Files Scanned",
            "0",
            "📁"
        )

        self.c2 = Card(
            "Threats",
            "0",
            "🚨"
        )

        self.c3 = Card(
            "Risky Files",
            "0",
            "⚠"
        )

        self.c4 = Card(
            "Risk Score",
            "0",
            "🛡"
        )


        for i,c in enumerate(
            [self.c1,self.c2,self.c3,self.c4]
        ):

            grid.addWidget(
                c,
                0,
                i
            )


        main.addLayout(grid)



        buttons = QHBoxLayout()
        buttons.setSpacing(15)

        scan = QPushButton(
            "Scan Folder"
        )

        scan.clicked.connect(
            self.pick_folder
        )


        clear = QPushButton(
            "Clear"
        )

        clear.clicked.connect(
            self.clear
        )


        export = QPushButton(
            "📄 Export Report"
        )

        export.clicked.connect(
            self.export_report
        )
        for b in [scan, clear, export]:
            b.setFixedHeight(45)
        buttons.addWidget(scan)
        buttons.addWidget(clear)
        buttons.addWidget(export)

        main.addLayout(buttons)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        chart_box = QHBoxLayout()

        self.risk_chart = Chart("🍩 Risk Overview")
        self.threat_chart = Chart("🥧 Threat Types")

        chart_box.addWidget(self.risk_chart)
        chart_box.addWidget(self.threat_chart)

        self.dashboard_widgets = [
            self.c1,
            self.c2,
            self.c3,
            self.c4,
            self.risk_chart,
            self.threat_chart
        ]

        main.addLayout(chart_box)

        main.addWidget(self.output, stretch=2)



        root.addWidget(sidebar)
        root.addLayout(main)

        self.setLayout(root)



        self.setStyleSheet(
"""
QWidget{
background:#0b0f14;
color:#e6edf3;
font-family:Arial;
}

#sidebar{
background:#11161d;
border-radius:18px;
border:1px solid #30363d;
}

#card{
background:#161b22;
border-radius:18px;
border:1px solid #343b45;
}

#card:hover{
background:#1c232d;
}

QLabel{
border:none;
background:transparent;
}

QPushButton{
background:#2b313a;
color:#e6edf3;
border:1px solid #444c56;
border-radius:12px;
padding:12px;
font-size:14px;
font-weight:bold;
}

QPushButton:hover{
background:#3d444d;
border:1px solid #768390;
}

QPushButton:pressed{
background:#555d66;
}

#sideBtn{
text-align:left;
padding-left:18px;
}

QTextEdit{
background:#161b22;
color:#d0d7de;
border-radius:15px;
padding:14px;
font-size:12px;
border:1px solid #444c56;
}

QScrollBar:vertical{
background:#161b22;
width:10px;
}

QScrollBar::handle:vertical{
background:#555d66;
border-radius:5px;
}
"""
        )



    def show_dashboard(self):
        self.output.hide()

        for widget in self.dashboard_widgets:
            widget.show()

    def show_results(self):
        self.output.setFocus()

        for widget in self.dashboard_widgets:
            widget.hide()

        self.output.show()

    def show_risk(self):
        window = QDialog(self)
        window.setWindowTitle("GhostTrace - Risk Analysis")
        window.resize(800,500)

        layout = QVBoxLayout()

        title = QLabel("📊 Advanced Risk Analysis")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        color:#d0d7de;
        """)

        layout.addWidget(title)


        figure = Figure(
            figsize=(7,4),
            facecolor="#161b22"
        )

        canvas = FigureCanvasQTAgg(figure)

        ax = figure.add_subplot(111)

        ax.set_facecolor("#161b22")


        names = [
            "Risk Score",
            "Safe Score",
            "Threats",
            "Risky Files"
        ]

        values = [
            self.risk_score,
            max(0,1000-self.risk_score),
            self.threats,
            self.risky
        ]


        ax.bar(
            names,
            values
        )


        ax.tick_params(
            axis="x",
            labelrotation=20,
            colors="#e6edf3"
        )

        ax.tick_params(
            axis="y",
            colors="#e6edf3"
        )


        ax.set_title(
            "Security Analysis Graph",
            color="#e6edf3"
        )


        canvas.draw()


        layout.addWidget(canvas)

        window.setLayout(layout)


        window.setStyleSheet("""
        QDialog{
            background:#0b0f14;
        }
        """)


        window.exec()

    def show_settings(self):

        window = QDialog(self)

        window.setWindowTitle(
            "GhostTrace Settings"
        )

        window.resize(
            650,
            600
        )

        main_layout = QVBoxLayout(window)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)

        title = QLabel(
            "⚙ GhostTrace Control Center"
        )
        
        layout.setSpacing(15)

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        layout.addWidget(title)

        # SCAN MODE

        scan_box = QGroupBox(
            "🔍 Scan Mode"
        )

        scan_layout = QVBoxLayout()

        quick = QRadioButton(
            "Quick Scan"
        )

        deep = QRadioButton(
            "Deep Scan"
        )

        ai = QRadioButton(
            "AI Scan"
        )

        deep.setChecked(True)

        scan_layout.addWidget(quick)
        scan_layout.addWidget(deep)
        scan_layout.addWidget(ai)

        scan_box.setLayout(
            scan_layout
        )

        layout.addWidget(
            scan_box
        )

        # FILE TYPES

        file_box = QGroupBox(
            "📂 File Types"
        )

        file_layout = QVBoxLayout()
        file_checks = {}
        for item in [
            "PDF",
            "TXT",
            "DOCX",
            "CSV",
            "JSON",
            "PY"
        ]:

            check = QCheckBox(
                item
            )

            check.setChecked(True)
            file_checks[item] = check

            file_layout.addWidget(
                check
            )

        file_box.setLayout(
            file_layout
        )

        layout.addWidget(
            file_box
        )

        # DETECTION

        detect_box = QGroupBox(
            "🛡 Detection"
        )

        detect_layout = QVBoxLayout()

        for item in [
            "Passwords",
            "API Keys",
            "Emails",
            "Phone Numbers",
            "Credit Cards",
            "Personal Information"
        ]:

            check = QCheckBox(
                item
            )

            check.setChecked(True)

            detect_layout.addWidget(
                check
            )

        detect_box.setLayout(
            detect_layout
        )

        layout.addWidget(
            detect_box
        )

        # RISK

        risk_box = QGroupBox(
            "🚨 Risk Sensitivity"
        )

        risk_layout = QVBoxLayout()

        slider = QSlider(
            Qt.Orientation.Horizontal
        )

        slider.setMinimum(1)
        slider.setMaximum(10)
        slider.setValue(5)

        risk_layout.addWidget(
            slider
        )

        risk_box.setLayout(
            risk_layout
        )

        layout.addWidget(
            risk_box
        )

        # REPORT

        report_box = QGroupBox(
            "📄 Reports"
        )

        report_layout = QVBoxLayout()

        graphs = QCheckBox(
            "Include Graphs"
        )

        ai_result = QCheckBox(
            "Include AI Results"
        )

        graphs.setChecked(True)
        ai_result.setChecked(True)

        report_layout.addWidget(
            graphs
        )

        report_layout.addWidget(
            ai_result
        )

        report_box.setLayout(
            report_layout
        )

        layout.addWidget(
            report_box
        )

        # THEME

        theme_box = QGroupBox(
            "🎨 Theme"
        )

        theme_layout = QVBoxLayout()

        theme = QComboBox()

        theme.addItems(
            [
                "Dark",
                "Light",
                "Cyber Green",
                "Grey Professional"
            ]
        )

        theme_layout.addWidget(
            theme
        )

        theme_box.setLayout(
            theme_layout
        )

        layout.addWidget(
            theme_box
        )

        save = QPushButton(
            "💾 Save Settings"
        )

        def apply_settings():
            if quick.isChecked():
                mode = "Quick"

            elif deep.isChecked():
                mode = "Deep"

            else:
                mode = "AI"


            self.settings = {

                "scan_mode": mode,


                "file_types":[
                    name
                    for name,box
                    in file_checks.items()
                    if box.isChecked()
                ],


                "risk_level":
                    slider.value(),


                "include_graphs":
                    graphs.isChecked(),


                "include_ai":
                    ai_result.isChecked(),


                "theme":
                    theme.currentText()
            }


            self.save_settings_file()


            QMessageBox.information(
                window,
                "Saved",
                "Settings Saved Successfully"
            )


            window.close()


        save.clicked.connect(
            apply_settings
        )

        layout.addWidget(
            save
        )
        # connect settings page to scrollbar

        scroll.setWidget(
            scroll_widget
        )

        main_layout.addWidget(
            scroll
        )
        
        
        window.setStyleSheet("""
        
        QDialog{
            background:#0b0f14;
            color:white;
        }
        
        QScrollArea{
    border:none;
    background:#0b0f14;
}


QScrollBar:vertical{
    background:#161b22;
    width:12px;
}


QScrollBar::handle:vertical{
    background:#555d66;
    border-radius:6px;
}

        QGroupBox{
            background:#161b22;
            border:1px solid #444c56;
            border-radius:12px;
            margin-top:10px;
            padding:15px;
        }

        QPushButton{
            background:#2b313a;
            border-radius:10px;
            padding:10px;
        }

        QPushButton:hover{
            background:#3d444d;
        }

        """)

        window.exec()



    def pick_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self
        )

        if folder:
            self.scan(folder)



    def scan(self, folder):

        self.clear()


        files = scan_directory(folder)

        self.files = len(files)


        for f in files:

            try:

                if f.endswith(".pdf"):

                    text = extract_pdf_text(f)

                else:

                    text = open(
                        f,
                        errors="ignore"
                    ).read()


            except:
                continue


            regex,score = detect_sensitive_data(text)

            ai = detect_sensitive_entities(text)



            if regex:

                for k,v in regex.items():
                    self.categories[k]=self.categories.get(k,0)+len(v)

                self.risky += 1
                self.risk_score += score

                self.threats += sum(
                    len(x)
                    for x in regex.values()
                )


                self.output.append(
f"""

━━━━━━━━━━━━━━━━━━━━

📄 {f}

🛡 Risk:
{score}

🔎 Sensitive:
{regex}

🤖 AI:
{ai}

"""
                )


        level = (
            "CRITICAL"
            if self.risk_score >= 500
            else "HIGH"
            if self.risk_score >= 200
            else "LOW"
        )

        self.output.append(
f"""

━━━━━━━━━━━━━━━━━━━━

📊 SCAN SUMMARY

Files scanned : {self.files}
Risky files   : {self.risky}
Threats       : {self.threats}
Risk score    : {self.risk_score}/1000

Risk Level:
{level}


🛡 SECURITY RECOMMENDATIONS

• Rotate exposed passwords/API keys
• Remove sensitive files from public folders
• Use encrypted storage
• Review privacy exposure regularly

"""
        )


        self.update_stats()



    def update_stats(self):

        self.c1.value.setText(
            str(self.files)
        )

        self.c2.value.setText(
            str(self.threats)
        )

        self.c3.value.setText(
            str(self.risky)
        )


        if self.risk_score >= 500:
            level="CRITICAL 🔴"

        elif self.risk_score >= 200:
            level="HIGH 🟠"

        else:
            level="LOW 🟢"


        self.c4.value.setText(
            f"{self.risk_score}/1000\n{level}"
        )

        if hasattr(self,"risk_chart"):
            self.risk_chart.draw([self.risk_score,max(0,1000-self.risk_score)],["Risk","Safe"],True)
            self.threat_chart.draw(list(self.categories.values()) or [1],list(self.categories.keys()) or ["Safe"])




    def export_report(self):

        level = (
            "CRITICAL"
            if self.risk_score >= 500
            else "HIGH"
            if self.risk_score >= 200
            else "LOW"
        )

        self.risk_chart.figure.savefig(
            "risk_graph.png",
            facecolor="#161b22"
        )

        self.threat_chart.figure.savefig(
            "threat_graph.png",
            facecolor="#161b22"
        )

        file = create_pdf_report(
            {
                "risk_graph":"risk_graph.png",
                "threat_graph":"threat_graph.png",
                "files": self.files,
                "threats": self.threats,
                "risky": self.risky,
                "score": self.risk_score,
                "level": level
            }
        )

        QMessageBox.information(
            self,
            "Report Generated",
            f"Audit report saved:\n{file}"
        )



    def clear(self):

        self.files = 0
        self.threats = 0
        self.risky = 0
        self.risk_score = 0
        self.categories = {}

        self.output.clear()

        self.update_stats()