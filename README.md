
# AutoScan
## Overview
AutoScan is a platform designed for **automated license plate detection and car recognition**. It enables real-time monitoring, data extraction, and analysis, making it an ideal solution for:

- **Traffic surveillance** : Enhancing road safety.
- **Automated parking management** : Facilitating seamless car identification for access control and payment automation.
- **Secure facility access** : Restricting and monitoring entry based on vehicle authorization.

## Features
- Real-Time Car Detection: Uses YOLOv8 to identify cars in video streams.

- License Plate Recognition: Extracts and deciphers text from detected license plates.

- Car Attribute Analysis: Identifies car color and brand.

- User-Friendly Interface: Provides an interactive dashboard for seamless monitoring and data retrieval.

- Multi-Camera Support: Processes multiple video sources concurrently.

- Data Export: Stores detected information for further analysis.

## User Interface
The AutoScan interface is designed for ease of use and efficient navigation.

### Login Interface
- Secure authentication via **email login**.
- Grants access to the **main monitoring dashboard**.
<p align="center">
  <img src="https://github.com/user-attachments/assets/b0044c08-d141-4cfb-b0a0-67f200326840" />
</p>

###  Dashboard Overview
- **Camera Selection:** Select from available video sources.
- **Live Video Feed:** Displays real-time footage from the selected camera.
- **Car Panel:** Shows images of detected cars.
- **Car Information Panel:** Displays extracted license plate data, including the plate number, vehicle color, brand, and timestamp of each detected car.
- **Data Export Options:** Allows users to download detection results in CSV format for record-keeping.
<p align="center">
  <img src="https://github.com/user-attachments/assets/b436584d-b263-4d24-b86b-3f86248b80e7" />
</p>



## System Architecture
AutoScan is built on a multi-threaded architecture optimized for real-time video processing and car recognition.

### Thread Management
To ensure high performance and smooth execution, AutoScan uses multiple parallel threads :

**1. Timer Thread :** Continuously updates the time to synchronize frame processing.

**2. Video Capture Thread :** Reads frames in real-time from the video source.

**3. Frame Processing Thread :** Stores captured frames in a queue.

**4. Vehicle Detection Thread :**
- Retrieves frames from the queue.
- Applies the **YOLOv8s** model to detect vehicles.
- Filters and stores only the detected cars in a list.

Each detected car is then processed individually to extract its attributes.

### Car Detection and Recognition
- License Plate Detection : Once a car is detected, AutoScan applies a **YOLOv8 License Plate Detector** to locate and extract the license plate (license_plate_detector.pt).

- License Number Recognition : The plate text is extracted using **OCR Tesseract**, allowing precise retrieval of the license number.

- Vehicle Color Detection : A **K-Means Clustering model** have been trained to  analyzes pixel distributions in the car image, segments colors into clusters, and selects the dominant color.

- Vehicle Brand Identification : A custom **YOLOv8** model is used for vehicle brand classification.

  Since no public dataset was available, we manually collected and annotated images of the **12 most common car brands in Morocco:**

  **Hyundai, Mercedes, Renault, Toyota, Volvo, Range Rover, Ford, BMW, Dacia, Citroën, Kia, Volkswagen**.

  For each brand, we extracted and annotated logos from images of cars.

  ![Image](https://github.com/user-attachments/assets/4c6ad000-e3ab-4c4e-a153-67285f216dcf)

  Once detected, the logo is used to classify the car into its corresponding brand category.
## Run Locally

Clone the project

```bash
  git clone https://github.com/hibaaaaaaaaaaa/AutoScan.git
```

Go to the project directory

```bash
  cd AutoScan
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Make sure Tesseract OCR is installed on your system . then add its path (C:\Program Files\Tesseract-OCR) to the PATH environment variable.

Start the application:

```bash
  python main.py
```
## Authors

- [@hibasofyan](https://github.com/hibaaaaaaaaaaa)
- [@chantryolandaeyiba](https://github.com/aryadacademie)


