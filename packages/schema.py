from pydantic import BaseModel, EmailStr
from PySide6.QtCore import QThread, Signal, QDateTime
from PySide6.QtGui import QImage
import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import distance
from ultralytics import YOLO

class UtilisateurCreate(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True  # Remplacer 'orm_mode' par 'from_attributes'

class User:
    def __init__(self,email:str,id_user:int):
        self.email =email
        self.id = id_user
    
    def get_user_id(self):
        return self.id
    
    def get_user_email(self):
        return self.email
    
    def set_user_id(self,id:int):
        self.id = id
        
    def set_user_email(self,email:str):
        self.email=email

class TimeThread(QThread):
    # Signal pour mettre à jour l'interface utilisateur avec l'heure actuelle
    time_signal = Signal(str)
    def run(self):
        while True:
            # Obtenir l'heure actuelle au format souhaité
            current_time = QDateTime.currentDateTime().toString("MMM d yyyy      hh:mm:ss")
            # Émettre le signal pour mettre à jour l'interface utilisateur
            self.time_signal.emit(current_time)
            # Attendre 1 seconde avant de continuer (ne pas bloquer l'interface)
            self.msleep(1000)
            
class VideoCaptureThread(QThread):
    frame_signal = Signal(QImage)
    def __init__(self, video_path=None, frame_queue=None):
        super().__init__()
        self.video_path = video_path
        self.frame_queue = frame_queue
        self.running = True
        self.cap = None
        self.frame_count = 0
        self.frame_interval=11
        
    def run(self):
        # Ouvrir la webcam ou la vidéo
        self.cap = cv2.VideoCapture(self.video_path if self.video_path else 0)
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                if self.frame_count % self.frame_interval == 0:   
                    print("Adding frame to queue")
                    self.frame_queue.put(frame)
            else:
                break
            # self.msleep(30)  # Attendre environ 30 ms pour atteindre 30 FPS
        self.frame_queue.put(None)  # Signal the end of the video

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

class VideoCaptureThread2(QThread):
    frame_signal = Signal(QImage)
    def __init__(self, video_path=None):
        super().__init__()
        self.video_path = video_path
        self.running = True
        self.cap = None
    def run(self):
        # Ouvrir la webcam ou la vidéo
        self.cap = cv2.VideoCapture(self.video_path if self.video_path else 0)
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.frame_signal.emit(img)
            else:
                break

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
 
            

    
class VideoProcessorThread(QThread):
    processed_cars_signal = Signal(list)

    def __init__(self,frame_queue):
        super().__init__()
        self.yolo=YOLO("yolov8s.pt")
        self.frame_queue = frame_queue
        self.running = True

    def run(self):
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                if frame is None:
                    print("End of video signal received")
                    break  # Fin du signal de la vidéo
                print("Processing frame")
                car_boxes = detect_cars(self.yolo, frame)
                car_images = annotate_and_extract(frame, car_boxes)
                # Emit the list of car images and details
                self.processed_cars_signal.emit(car_images)

    def stop(self):
        self.running = False
        #self.wait()

def detect_cars(model, image):
    results = model(image, save=False)
    car_boxes = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0].item())
            class_name = model.names[class_id]

            if class_name == "car":
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                if (x_max - x_min) > 400 and (y_max - y_min) > 380:
                    car_boxes.append((box.xyxy[0].tolist(), box.conf[0].item()))
    return car_boxes

def annotate_and_extract(frame, car_boxes):
    car_images = []
    for (box, confidence) in car_boxes:
        x_min, y_min, x_max, y_max = map(int, box)
        car_image = frame[y_min:y_max, x_min:x_max]
        car_image_rgb = cv2.cvtColor(car_image, cv2.COLOR_BGR2RGB)
        car_images.append({
            "image": car_image_rgb,
            "confidence": confidence,
            "bounding_box": (x_min, y_min, x_max, y_max)
        })
    return car_images


# Dictionnaire de couleurs CSS3
CSS3_COLORS = {
    'Blanc': (255, 255, 255),
    'Noir': (0, 0, 0),
    'Argent': (192, 192, 192),
    'Gris métallisé': (169, 169, 169),
    'Rouge': (255, 0, 0),
    'Bleu': (0, 0, 255),
    'Bleu métallisé': (0, 0, 128),
    'Vert': (0, 255, 0),
    'Jaune': (255, 255, 0),
    'Bronze': (205, 127, 50),
    'Beige': (245, 245, 220),
    'Marron': (139, 69, 19),
    'Orange': (255, 165, 0),
    'Violet': (128, 0, 128),
    'Or': (255, 215, 0),
    'Rose': (255, 192, 203)
}

# Convertir RGB en Lab
def rgb_to_lab(rgb):
    rgb_normalized = np.array(rgb) / 255.0
    rgb_linear = np.where(rgb_normalized <= 0.04045, rgb_normalized / 12.92, ((rgb_normalized + 0.055) / 1.055) ** 2.4)
    rgb_linear = rgb_linear * 100
    x = rgb_linear[0] * 0.4124564 + rgb_linear[1] * 0.3575761 + rgb_linear[2] * 0.1804375
    y = rgb_linear[0] * 0.2126729 + rgb_linear[1] * 0.7151522 + rgb_linear[2] * 0.0721750
    z = rgb_linear[0] * 0.0193339 + rgb_linear[1] * 0.1191920 + rgb_linear[2] * 0.9503041
    xyz = np.array([x, y, z])
    
    x = xyz[0] / 95.047
    y = xyz[1] / 100.0
    z = xyz[2] / 108.883
    
    x = x / 100.0
    y = y / 100.0
    z = z / 100.0
    
    return (116 * y - 16, 500 * (x - y), 200 * (y - z))

def get_closest_color_name(rgb_color):
    """
    Trouve la couleur la plus proche dans un dictionnaire de couleurs CSS3 en utilisant Lab et un seuil.
    
    :param rgb_color: La couleur à tester (tuple RGB).
    :return: Le nom de la couleur la plus proche.
    """
    min_distance = float('inf')
    closest_color_name = None
    
    # Convertir la couleur RGB en Lab pour une comparaison perceptuelle
    target_lab = rgb_to_lab(rgb_color)
    
    for name, rgb in CSS3_COLORS.items():
        # Convertir les couleurs CSS3 en Lab
        color_lab = rgb_to_lab(rgb)
        
        # Calculer la distance dans l'espace Lab
        dist = np.linalg.norm(np.array(target_lab) - np.array(color_lab))
        
        # Si la distance est plus petite que celle précédemment trouvée, mettre à jour la couleur la plus proche
        if dist < min_distance:
            min_distance = dist
            closest_color_name = name
    
    # Si la distance est trop grande, considérer comme une couleur inconnue
    if min_distance > 40:  # Vous pouvez ajuster ce seuil selon vos besoins
        return "Couleur inconnue"
    
    return closest_color_name

def extract_dominant_color(image, n_clusters=50):
    """
    Extrait la couleur dominante d'une image entière et trouve son nom proche.
    
    :param image: Image d'entrée (numpy array).
    :param n_clusters: Nombre de clusters pour KMeans (défaut : 3).
    :return: Couleur dominante sous la forme (B, G, R) et le nom de la couleur.
    """
    if image is None:
        raise ValueError("L'image est vide ou introuvable. Vérifiez le chemin d'accès.")

    # Convertir l'image en HSV pour une meilleure détection de la couleur dominante
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Réduire la taille de l'image pour accélérer le traitement (optionnel)
    resized_image = cv2.resize(image_hsv, (32,32))  # Redimensionner à 100x100
    pixels = resized_image.reshape((-1, 3))  # Convertir en une liste de pixels

    # Utiliser KMeans pour trouver les couleurs dominantes
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(pixels)

    # Trouver la couleur dominante (le cluster avec la plus grande taille)
    cluster_sizes = np.bincount(kmeans.labels_)
    dominant_cluster = np.argmax(cluster_sizes)
    dominant_color_hsv = kmeans.cluster_centers_[dominant_cluster].astype(int)

    # Convertir la couleur dominante de HSV à RGB
    dominant_color_bgr = cv2.cvtColor(np.uint8([[dominant_color_hsv]]), cv2.COLOR_HSV2BGR)[0][0]
    dominant_color_rgb = tuple(reversed(dominant_color_bgr))  # Convertir BGR en RGB

    # Trouver le nom de la couleur proche dans le dictionnaire
    closest_name = get_closest_color_name(dominant_color_rgb)
    
    return dominant_color_rgb, closest_name



# import cv2
# import numpy as np

# # Exemple d'utilisation
# image_path = r"C:\Users\farya\Pictures\Screenshots\vlv.png" # Remplacez par le chemin de votre image
# image = cv2.imread(image_path)

# if image is not None:
#     dominant_color, closest_name = extract_dominant_color(image)
#     print(f"Couleur dominante (RGB): {dominant_color}")
#     print(f"Nom de la couleur la plus proche: {closest_name}")
# else:
#     print("Erreur : l'image n'a pas pu être chargée.")
