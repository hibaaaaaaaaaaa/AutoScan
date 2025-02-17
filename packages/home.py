from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QHBoxLayout
from schema import User
from dashboard import Dashboard
from PySide6.QtGui import QPixmap, QFont, QFontDatabase
from PySide6.QtCore import Qt


class Home(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.user = None
        # Initialisation de la fenêtre
        self.setFixedSize(1200, 600)
        self.parent.set_win_title("Accueil")
        
        # Charger la police depuis un fichier
        font_id = QFontDatabase.addApplicationFont('C:/Users/farya/Desktop/OpenCv_2K25_Plate/packages/fonts/Manrope-VariableFont_wght.ttf')
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # Définir l'image de fond
        back_view = QLabel(self)
        back_view.setPixmap(QPixmap("packages/icons/baz.png").scaled(1200, 600))
        back_view.setGeometry(0, 0, 1200, 600)
        
        # Bouton "Commencer"
        self.btn_start = QPushButton("Commencer", self)
        self.btn_start.setFont(QFont(self.font_family, 8, QFont.Weight.Bold))
        self.btn_start.setStyleSheet("text-align: center; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.2); background: rgba(255, 255, 255, 0.1);")
        self.btn_start.setGeometry(1018, 41, 120, 33)
        
        # Bouton "Vision en Temps Réel"
        btn_view = QPushButton("Vision en Temps Réel", self)
        btn_view.setFont(QFont(self.font_family, 8, QFont.Weight.Bold))
        btn_view.setGeometry(520, 144, 170, 33)
        btn_view.setStyleSheet("""
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(76, 205, 153, 0.4);
            background: rgba(255, 255, 255, 0.02);
            color: rgba(76, 205, 153, 0.4);
        """)

        # Label d'informations
        label_info = QLabel(self)
        label_info.setText("Transformez la route en données : Détection instantanée, reconnaissance de plaques, et identification des couleurs et \n marques en un clin d'œil !")
        label_info.setFont(QFont(self.font_family, 16, QFont.Weight.Bold))
        label_info.setGeometry(140, 485, 932, 96)
        label_info.setStyleSheet("""
            font-family: Manrope;
            font-size: 16px;
            font-weight: 400;
            line-height: 25.6px;
            text-align: center;
            background: transparent;
            color: rgba(255, 255, 255, 0.7);
        """)
        label_info.setAlignment(Qt.AlignCenter)  # Alignement du texte au centre

        self.decoration()
        self.entry_info()

    def entry_info(self):
        # Créer un QHBoxLayout pour la disposition horizontale
        flex_direction_win = QHBoxLayout()
        flex_direction_win.setSpacing(14)
        flex_direction_win.setContentsMargins(5, 5, 5, 5)
        
        # Créer une nouvelle fenêtre (QWidget) pour contenir les éléments
        win = QWidget(self)
        win.setGeometry(409, 350, 401, 50)
        win.setStyleSheet("border-radius: 24px; background: rgba(255, 255, 255, 0.2);")
        
        # Champ email
        self.email = QLineEdit(win)
        self.email.setPlaceholderText("Entrez votre email")
        self.email.setFixedSize(259, 22)
        self.email.setStyleSheet("""
            background-color: transparent;
            font-weight: 400;
            font-size: 14px;
            padding-left: 12px;
            font-family: Manrope;
        """)

        # Bouton de soumission (submit)
        self.submit = QPushButton("Connexion", win)
        self.submit.setFixedSize(110, 40)
        self.submit.setFont(QFont(self.font_family, 14, QFont.Weight.Bold))
        self.submit.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: rgba(76, 205, 153, 1);
                color: black;
                font-weight: 400;
                font-size: 14px;
                font-family: Manrope;
            }
            QPushButton:pressed {
                background-color: rgba(56, 175, 130, 1);
            }
            QPushButton:hover {
                background-color: rgba(86, 215, 153, 1);
            }
        """)
        self.submit.clicked.connect(self.connection)
        self.submit.setCursor(Qt.PointingHandCursor)

        # Ajouter les widgets au layout
        flex_direction_win.addWidget(self.email)
        flex_direction_win.addWidget(self.submit)

        # Appliquer le layout à la fenêtre
        win.setLayout(flex_direction_win)
        self.setStyleSheet("background: rgba(1, 1, 1, 1);")

    def decoration(self):
        title = QLabel(self)
        title.setText("Une solution intelligente pour la\n surveillance routière")
        title.setFont(QFont(self.font_family, 40, QFont.Weight.Bold))
        title.setGeometry(198, 204, 823, 117)
        title.setStyleSheet("""
            font-family: Manrope;
            font-size: 40px;
            font-weight: 600;
            line-height: 25.6px;
            text-align: center;
            color: rgba(255, 255, 255, 1);
            background: transparent;
        """)
        title.setAlignment(Qt.AlignCenter)  # Alignement du texte au centre
    
    def on_link_clicked(self, email, id_user):
        self.user = User(email, id_user)
        dashboard = Dashboard(self.user,self.parent)  # Correction de la création de l'objet Dashboard
        self.parent.setframe(dashboard)
        
    def connection(self):
        email = self.email.text().strip().lower()

        # Vérifier si l'email est fourni
        if not email:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un email valide.")
            return
        try:
            self.on_link_clicked(email, 0)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue s'est produite : {e}")
