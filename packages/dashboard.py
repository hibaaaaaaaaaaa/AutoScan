from PySide6.QtWidgets import QWidget,QFileDialog, QVBoxLayout,QPushButton, QLabel, QScrollArea,QTreeWidget, QTreeWidgetItem, QRadioButton
from schema import TimeThread,VideoCaptureThread,VideoProcessorThread,VideoCaptureThread2
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap,QFont, QFontDatabase,QImage
from queue import Queue
import numpy as np

voitures_detected = np.array([]) 
frame_queue = Queue()

color_model_ = None
class Dashboard(QWidget):
    def __init__(self,user,parent):
        super().__init__()
        self.user = user
        self.parent = parent
        self.id_v=1
        # Initialisation de la fenêtre
        self.setFixedSize(1200, 600)
        font_id = QFontDatabase.addApplicationFont('C:/Users/farya/Desktop/OpenCv_2K25_Plate/packages/fonts/Manrope-VariableFont_wght.ttf')
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        back_view = QLabel(self)
        back_view.setPixmap(QPixmap("packages/icons/dash_baz.png").scaled(1200,600))
        back_view.setGeometry(0,0,1200,600)
        
        back_view.setStyleSheet("""
            opacity:0.24px;
            background: rgba(1, 1, 1, 1);""")
        self.parent.set_win_title("Dashboard")
         
        self.top_panel()
        self.left_panel()
        self.right_panel()
        self.bottom_panel()
        self.sub_top_panel()
    
  
    def top_panel(self):
        win = QWidget(self)
        win.setGeometry(46, 27,1114,43)
        win.setStyleSheet("""background:transparent;""")
        
        
        info = QPushButton("Information",self)
        
        
        
        
        info.setStyleSheet("""
font-family: Manrope;
font-size: 16px;
font-weight: 600;
background:transparent;
color: rgba(76, 205, 153, 1);
line-height: 19.2px;
letter-spacing: 0.03em;
text-align: center;        
                """)
        info.setGeometry(1008, 38,152,27)
        
        moni = QLabel("Monitor",self)
        moni.setStyleSheet("""
font-family: Manrope;
font-size: 16px;
background:transparent;
font-weight: 600;
color: rgba(76, 205, 153, 1);
line-height: 19.2px;
letter-spacing: 0.03em;
text-align: center;""")
        moni.setGeometry(856, 38,152,27)
        
        logo = QLabel(self)
        logo.setGeometry(62, 34,22,25)
        logo.setStyleSheet("""
                    background:transparent;
                """)
        logo.setPixmap(QPixmap("packages/icons/icon_logo.png").scaled(22,25))
        
        clok = QLabel(self)
        clok.setGeometry(956, 79,20,20)
        clok.setPixmap(QPixmap("packages/icons/clock.png").scaled(20,20))
        
        self.time_now = QLabel(self)
        self.time_now.setText(f"Jan 2 2025      20:07:45")
        self.time_now.setGeometry(985, 78,466,21)
        self.time_now.setStyleSheet("""
font-family: Manrope;
font-size: 16px;
font-weight: 500;
background:transparent;
line-height: 19.2px;
letter-spacing: 0.03em;
text-align: center;
                            """)
       # Créer le thread pour la mise à jour du temps
        self.time_thread = TimeThread()
        self.time_thread.time_signal.connect(self.update_time)  # Connecter le signal à la fonction qui met à jour l'heure
        self.time_thread.start()  # Démarrer le thread

    def update_time(self, current_time):
        # Mettre à jour le QLabel avec l'heure actuelle
        self.time_now.setText(current_time)
        
    def left_panel(self):
        win = QWidget(self)
        win.setGeometry(47, 99,160,464)
        win.setStyleSheet("""background:transparent;""")
        
        layout = QVBoxLayout()
        tree_widget = QTreeWidget()
        tree_widget.setFont(QFont(self.font_family, 10, QFont.Weight.Bold))
        tree_widget.setStyleSheet(
        """
        QTreeWidget::branch:has-children:closed {
        image: url('packages/icons/close.png');}
        QTreeWidget{
        color:rgba(76, 205, 153, 1);
        border: none;
        background:transparent;}
        QTreeWidget::branch:has-children:open {
        image: url('packages/icons/open.png');}
        QTreeView::branch {
        border: none;
        background:transparent;}
        """
        )   
        tree_widget.setHeaderHidden(True)  # Cache l'en-tête
        # Création des flux de caméra avec sous-éléments
        for i in range(1, 10):
            parent_item = QTreeWidgetItem(tree_widget)
            parent_item.setText(0, f"caméra-flux-{i}")
        
            radio_button1 = QRadioButton("local video-1")
            radio_button1.setFont(QFont(self.font_family, 12, QFont.Weight.Bold))
            radio_button2 = QRadioButton("local video-2")
            radio_button2.setFont(QFont(self.font_family, 12, QFont.Weight.Bold))
            radio_button1.setStyleSheet(
        """
        QRadioButton{
        font-family: Manrope;
        font-size: 12px;
        font-weight: 500;
        line-height: 15.6px;
        letter-spacing: 0.03em;
        border:none;}
        QRadioButton::indicator {
        color:white;
        }
        """
        )
            radio_button2.setStyleSheet(
        """
        QRadioButton{
        font-family: Manrope;
        font-size: 12px;
        font-weight: 500;
        line-height: 15.6px;
        letter-spacing: 0.03em;
        border:none;}
        QRadioButton::indicator {
        color: white;}
        """
        )
            child_widget1 = QWidget()
            child_widget1.setStyleSheet("""border:none;""")
            child_layout1 = QVBoxLayout()
            child_layout1.addWidget(radio_button1)
            child_layout1.addWidget(radio_button2)
            child_layout1.setContentsMargins(0, 0, 0, 0)
            child_widget1.setLayout(child_layout1)
            # Connecter les radio boutons à des écouteurs uniques
            radio_button1.toggled.connect(lambda checked, idx=i: self.radio_toggled(checked, idx, "video-1"))
            radio_button2.toggled.connect(lambda checked, idx=i: self.radio_toggled(checked, idx, "video-2"))
            child_item = QTreeWidgetItem(parent_item)
            tree_widget.setItemWidget(child_item, 0, child_widget1)
            
        layout.addWidget(tree_widget)
        win.setLayout(layout)
        self.video_reader_thread = None
        self.video_reader_thread2 = None
        self.video_processor_thread=None
        
        
    
    def radio_toggled(self, checked, idx, video_type):
        if checked:
            if(idx==1 and video_type=="video-1"):
                self.start_video_thread()
            elif(idx==1 and video_type=="video-2"):
                self.load_video()
            
        
    def right_panel(self):
        win = QWidget(self)
        win.setGeometry(766, 103,400,465)
        win.setStyleSheet("background:transparent;")
        
        cap = QLabel(win)
        cap.setGeometry(20,15,32,32)
        cap.setPixmap(QPixmap("packages/icons/capture.png").scaled(32,32))
        title_ = QLabel("Voiture Capturée",win)
        title_.setGeometry(60,15,149,32) 
    
        self.scroll_area_voiture = QScrollArea(win)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color:transparent;")
        self.scroll_layout_voiture = QVBoxLayout()
        scroll_widget.setLayout(self.scroll_layout_voiture)
        self.scroll_area_voiture.setWidget(scroll_widget)
        self.scroll_area_voiture.setWidgetResizable(True)
        self.scroll_area_voiture.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_voiture.setGeometry(10, 50, 380, 405)
        self.scroll_layout_voiture.setSpacing(10)
        
        



        
        
        cap.setStyleSheet(
            """
            border:none;
            background:transparent;
            """
        )
        
        
        title_.setStyleSheet(
            """
            font-family: Manrope;
            font-size: 14px;
            font-weight: 700;
            line-height: 22px;
            border:none;
            background:transparent;
            """
        )
        
        
        self.scroll_area_voiture.setStyleSheet("""
    QScrollBar:vertical {
        border: none;
        background: rgba(56, 124, 96, 0.3);  /* Couleur de fond de la scrollbar */
        width: 4px;
        border-radius: 2px;
    }
    QScrollBar::handle:vertical {
        background: rgba(76, 205, 153, 1);  /* Couleur de la poignée de la scrollbar */
        min-height: 27px;
        border-radius: 2px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background:transparent;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background:transparent;
    }
""")
        
        
    
        

    def bottom_panel(self):
        # Correction du style CSS
        ico_info = QLabel(self)
        ico_info.setGeometry(273, 338, 24, 24)
        ico_info.setPixmap(QPixmap("packages/icons/info.png").scaled(24,24))
        ico_info.setStyleSheet("""background:transparent;""")
        
        lin = QLabel(self)
        lin.setPixmap(QPixmap("packages/icons/line_bottom.svg").scaled(1,89))
        lin.setGeometry(484,451,1,89)
        
        info = QLabel("Infomations",self)
        info.setStyleSheet("""font-family: Manrope;
                            font-size: 14px;
                            background:transparent;
                            font-weight: 700;
                            line-height: 22.4px;""")
        info.setGeometry(305, 340, 282, 23)
        
        lab_matricule = QLabel("Immatriculation",self)
        lab_matricule.setStyleSheet("""
                            font-family: Manrope;
                            font-size: 14px;
                            background:transparent;
                            font-weight: 400;
                            line-height: 22.4px;""")
        lab_matricule.setGeometry(312, 496, 113, 19)
        
        lab_marque =QLabel("Marque",self)
        lab_marque.setStyleSheet("""
                            font-family: Manrope;
                            font-size: 14px;
                            background:transparent;
                            font-weight: 400;
                            line-height: 22.4px;""")
        lab_marque.setGeometry(312, 451, 60, 19)
        
        lab_couleur =QLabel("Couleur",self)
        lab_couleur.setStyleSheet("""
                    font-family: Manrope;
                    font-size: 14px;
                    background:transparent;
                    font-weight: 400;
                    line-height: 22.4px;""")
        lab_couleur.setGeometry(566, 451, 60, 19)
        
        lab_time =QLabel("Heure de capture",self)
        lab_time.setStyleSheet("""
                    font-family: Manrope;
                    font-size: 14px;
                    background:transparent;
                    font-weight: 400;
                    line-height: 22.4px;""")
        lab_time.setGeometry(566, 495, 127, 19)
        
        lab_id =QLabel("Voiture ID :",self)
        lab_id.setStyleSheet("""
                    font-family: Manrope;
                    font-size: 13px;
                    background:transparent;
                    font-weight: 400;
                    line-height: 20.8px;""")
        lab_id.setGeometry(592, 340, 69, 19)
        
        self.view_id =QLabel(self)
        self.view_id.setStyleSheet("""
                    color:rgba(255, 244, 85, 0.6);
                    font-family: Manrope;
                    font-size: 13px;
                    font-weight: 400;
                    line-height: 20.8px;
                    background:transparent;""")
        self.view_id.setGeometry(657, 340, 30, 19)
        
        self.plat_view_ = QLabel(self)
        self.plat_view_.setGeometry(358,381,238,48)
        
        self.view_time =QLabel(self)
        self.view_time.setGeometry(566, 516, 107, 19)
        self.view_time.setStyleSheet("""
                                    background:transparent;
                                    """)
        
        self.view_matricule = QLabel(self)
        self.view_matricule.setGeometry(312,516, 107, 19)
        self.view_matricule.setStyleSheet("""
                                    background:transparent;
                                    """)
        
        self.view_marque =QLabel(self)
        self.view_marque.setGeometry(312, 468, 107, 19)
        self.view_marque.setStyleSheet("""
                                    background:transparent;
                                    """)
        
        self.view_couleur =QLabel(self)
        self.view_couleur.setGeometry(566, 466, 107, 19)
        self.view_couleur.setStyleSheet("""
                                    background:transparent;
                                    """)
        
        self.view_flag_color =QWidget(self)
        self.view_flag_color.setGeometry(620, 471, 15, 15)
        self.view_flag_color.setStyleSheet("background:transparent;border-radius:5px;")
        
        
    def update_view_info(self,id,time,matricule,marque,couleur,dominant_color):
        self.view_id.setText(id)
        self.view_time.setText(time)
        self.view_matricule.setText(matricule)
        self.view_marque.setText(marque)
        self.view_couleur.setText(couleur)
        color = f"background:rgb{dominant_color};"
        self.view_flag_color.setStyleSheet(color)
        
       

        
    def sub_top_panel(self):
        win = QWidget(self)
        win.setGeometry(260, 102, 448, 206)
        win.setStyleSheet("background:transparent;")
        
        self.video_flux = QLabel(win)
        self.video_flux.setPixmap(QPixmap("packages/icons/view_.png").scaled(448, 206))
        self.video_flux.setAlignment(Qt.AlignCenter)
        # Correction du style CSS
        

    def load_video(self):
        # Ouvrir une boîte de dialogue pour sélectionner un fichier vidéo
        file_path, _ = QFileDialog.getOpenFileName(self, "Charger une vidéo", "", "Videos (*.mp4 *.avi *.mkv)")
        if file_path:
            self.start_video_thread(file_path)
            
    def stop_all_thread(self):
        
        try:
        
            if self.video_reader_thread and self.video_reader_thread.isRunning():
                self.video_reader_thread.stop()
                # self.video_reader_thread.wait()
            
            if self.video_reader_thread2 and self.video_reader_thread2.isRunning():
                self.video_reader_thread2.stop()
                # self.video_reader_thread2.wait()
            
            if self.video_processor_thread and self.video_processor_thread.isRunning():
                self.video_processor_thread.stop()
                # self.video_processor_thread.wait()
            
            self.video_flux.setPixmap(QPixmap("packages/icons/view_.png").scaled(448, 206))
        except Exception as e:
            print(f"Erreur lors de l'arrêt des threads: {e}")

        
    def start_video_thread(self, source=None):
        # Arrêter tout thread vidéo en cours
        if self.video_reader_thread:
            self.video_reader_thread.stop()
            # self.video_reader_thread.wait()
        
        if self.video_reader_thread2:
            self.video_reader_thread2.stop()
            #self.video_reader_thread2.wait()

        if self.video_processor_thread:
            self.video_processor_thread.stop()
            #self.video_processor_thread.wait()
            
        self.video_reader_thread =VideoCaptureThread2(source)
        self.video_reader_thread2 =VideoCaptureThread(source, frame_queue)
        
        self.video_reader_thread.frame_signal.connect(self.update_video_frame)
        self.video_reader_thread.start()
        self.video_reader_thread2.start()

        self.video_processor_thread = VideoProcessorThread(frame_queue)
        self.video_processor_thread.processed_cars_signal.connect(self.update_liste_voitures)
        self.video_processor_thread.start()

    def update_video_frame(self, img):
        pixmap = QPixmap.fromImage(img)
        self.video_flux.setPixmap(pixmap.scaled(self.video_flux.size(), Qt.KeepAspectRatioByExpanding))
    

    def update_liste_voitures(self,car_images):
        for car in car_images:
            voiture = Voiture_View(self.id_v,car["image"],self)
            voiture.setStyleSheet("border: 1px solid rgba(56, 124, 96, 0.4);border-radius:15px;")
            self.scroll_layout_voiture.addWidget(voiture)
            self.scroll_area_voiture.widget().adjustSize()  # Ajuste la taille du widget contenu
            # self.scroll_area_voiture.verticalScrollBar().setValue(
            #     self.scroll_area_voiture.verticalScrollBar().maximum()
            # ) immatriculation
            self.id_v+=1
         

    def closeEvent(self, event):
        if self.video_reader_thread:
            self.video_reader_thread.stop()
            #self.video_reader_thread.wait()
            
        if self.video_reader_thread2:
            self.video_reader_thread2.stop()
            #self.video_reader_thread2.wait()
        
        if self.video_reader_thread2:
            self.video_reader_thread2.stop()
            #self.video_reader_thread2.wait()
            
        event.accept()
    
    

class Voiture_View(QWidget):
    def __init__(self,id,photo,parent):
        super().__init__()
        self.id = id
        self.photo = photo
        self.parent = parent
        
        
        self.parametres()
        self.display_image()
        self.infos_voitures()
        
        
        
    
    def parametres(self):
        self.setFixedSize(350, 160)
    
    def infos_voitures(self):# Informations sur la voiture
        info_ = QLabel("Voiture ID:",self)
        info_.setGeometry(10, 10, 149, 22)
        info_.setStyleSheet("""border:none;background:none;
                            font-family: Manrope;
                            font-size: 14px;
                            font-weight: 400;
                            color:rgba(255, 255, 255,1);
                            line-height: 22.4px;""")
        info_id = QLabel(str(self.id),self)
        info_id.setGeometry(10, 32, 149, 22)
        info_id.setStyleSheet("""border:none;background:none;
                                font-family: Amiri;
                                font-size: 14px;
                                font-weight: 400;
                                line-height: 22.4px;
                                color:rgba(255, 255, 255, 0.6);
                                """)
        # Bouton pour voir plus de détails
        more = QPushButton("Voir Détails",self)
        more.setStyleSheet("""
        QPushButton {
        background-color:rgba(76, 205, 153, 1);
        border-radius: 13px;
        color:rgba(1, 1, 1, 1);
        font-family: Manrope;
        font-size: 11px;
        font-weight: 500;
        line-height: 17.6px;
        text-align: center;
                    }
                    QPushButton:pressed {
                        background-color: rgba(56, 175, 130, 1);
                    }
                    QPushButton:hover {
                        background-color: rgba(86, 215, 153, 1);
                    }
        """)
        more.setCursor(Qt.PointingHandCursor)
        more.setGeometry(10, 100, 88, 27)
        
    def display_image(self):
        # Photo de la voiture
        photo_label = QLabel(self)
        h, w, ch = self.photo.shape
        bytes_per_line = ch * w
        qimage = QImage(self.photo.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        photo_label.setPixmap(pixmap.scaled(125, 125))
        photo_label.setGeometry(190, 10, 140, 140)
        photo_label.setAlignment(Qt.AlignCenter)
        photo_label.setWordWrap(True)
        photo_label.setStyleSheet("border: 1px solid rgba(56, 124, 96, 0.4);border-radius:15px;padding:2px;")
            
    
    # dominant_color, closest_name = extract_dominant_color(photo)
    # current_time = QDateTime.currentDateTime().toString("MMM d yyyy hh:mm:ss")
    # def display_info():
    #     id_ = info_id.text()
    #     matricule = "MKD1161"
    #     marque = "Marque"  # Données fictives, à ajuster
    #     self_parent.update_view_info(id_,current_time,matricule,marque,closest_name,dominant_color)
    
    # more.clicked.connect(display_info)
    