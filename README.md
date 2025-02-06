# Aquaeye: Detecting Debris Pollution in Aquatic Systems  

<p align="center">
    <img src="https://github.com/user-attachments/assets/8918405f-55c9-4299-9655-64c3efdf0d04" width="45%" height="250px" style="object-fit: cover;">
    <img src="https://github.com/user-attachments/assets/604bce6b-601c-4cf0-af2d-288efc81a366" width="45%" height="250px" style="object-fit: cover;">
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/cf2e3094-09a9-454e-aa76-e1d3f62c1eac" width="45%" height="250px" style="object-fit: cover;">
    <img src="https://github.com/user-attachments/assets/d248de4c-97ea-4869-a82f-0a6f8b71490a" width="45%" height="250px" style="object-fit: cover;">
</p>

## Overview  

Managing waste effectively in aquatic systems is crucial for preserving marine life, ecosystems, and biodiversity. **Aquaeye** uses deep learning techniques to detect and classify submerged debris, including rare and hard-to-spot types, thereby promoting a cleaner and more sustainable environment.  

## What Aquaeye Does  

✅ **Debris Detection** – Uses state-of-the-art AI models to identify and classify rare debris submerged underwater.  
✅ **Environmental Insights** – Provides data and insights for better decision-making regarding underwater cleanup and conservation.  

## Why Aquaeye?  

- **Environmental Impact:** Contributes to preserving marine life and reducing underwater pollution.  
- **Advanced Technology:** Employs cutting-edge AI models for superior detection in challenging underwater environments.  
- **Scientific Benefits:** Supports researchers, conservationists, and policymakers with valuable insights and data visualization tools.  


## Key Features  

1. **High Precision Detection:** Employs YOLOv5-based deep learning models to identify submerged debris.  
2. **Data Visualization:** Uses Tableau to present a **quantification, degradation factor, and classification dashboard** for better pollution analysis.  
3. **Real-time Processing:** Handles **live detection** of underwater plastic pollution.  


## How We Are Building It  

| **Component**           | **Technology Stack**                          |
|------------------------|----------------------------------------------|
| **Programming Language** | Python                                      |
| **Backend Frameworks**   | Flask, PyTorch, Roboflow                    |
| **Frontend Development** | HTML, CSS, JavaScript                       |
| **Deep Learning Model**  | YOLOv5, YOLOv11, YOLONAS                     |
| **Data Visualization**   | Plotly, Dash                                |
| **Hardware**             | Google Colab TPU                            |


## Getting Started  

### Backend Setup  
_To be added_  

### Frontend Setup  
_To be added_  


## Challenges Faced  

- **Data Availability:** Limited and diverse underwater datasets made training challenging.  
- **Noisy Environments:** Dealing with **low-visibility underwater settings** required advanced pre-processing techniques.  
- **Computational Constraints:** Training deep learning models on large datasets required **optimization techniques**.  


## Overcoming Strategies  

✔ **Data Processing:** Cleaned and augmented datasets using advanced image pre-processing techniques.  
✔ **Noise Reduction:** Enhanced underwater images with **adaptive filtering methods** to improve clarity.  
✔ **Transfer Learning:** Leveraged **pre-trained models** to overcome data scarcity issues.  

## Accomplishments To Be Proud Of  

| **Milestone**              | **Description**                                |
|----------------------------|-----------------------------------------------|
| **Dataset Creation**       | Collected and processed large underwater plastic datasets. |
| **YOLO-based Model**       | Successfully trained **YOLOv5** for real-time debris detection. |
| **Visualization Dashboard**| Built **interactive dashboards** to analyze plastic pollution trends. |
| **Noise Reduction**        | Developed **image enhancement** techniques to improve accuracy. |

## Lessons Learned  

- **Importance of Data Preprocessing** – Cleaning and augmenting datasets significantly improved model accuracy.  
- **Balancing Speed and Accuracy** – Real-time underwater detection requires an **optimized model** with **fast inference**.  
- **Handling Low Visibility** – Underwater images often have **noise and distortion**, requiring **adaptive filtering** techniques.  
- **Transfer Learning is Key** – Pre-trained models helped overcome dataset limitations in detecting rare debris types.  

## What's Next for Aquaeye?  

- **Expanding Dataset** – Collect and diversify the training data for better generalization.  
- **Improving Processing Speed** – Optimize real-time detection for faster inference.  
- **Trying More Models** – Experiment with **YOLOv8, EfficientDet, and Transformer-based models**.  
- **Enhancing Accuracy** – Fine-tune models to improve **precision, recall, and F1 score**.  

## Research & References

- Tianlong Jia, Zoran Kapelan, Rinze de Vries, Paul Vriend, Eric Copius Peereboom, Imke Okkerman, Riccardo Taormina, "Deep learning for detecting macroplastic litter in water bodies: A review", Water Research, Volume 231, 2023, 119632, ISSN 0043-1354, [https://doi.org/10.1016/j.watres.2023.119632](https://doi.org/10.1016/j.watres.2023.119632).  

- Abdelaadim Khriss, Aissa Kerkour Elmiad, Mohammed Badaoui, Alae-Eddine Barkaoui, Yassine Zarhloule, "Exploring Deep Learning for Underwater Plastic Debris Detection and Monitoring", Journal of Ecological Engineering, Volume 25, Issue 7, 2024, ISSN 2299-8993, [https://doi.org/10.12911/22998993/187970](https://doi.org/10.12911/22998993/187970).  

- Gautam Tataa, Jay Lowe, Olivier Poirion, Sarah-Jeanne Royer, "A Robotic Approach towards Quantifying Epipelagic Bound Plastic Using Deep Visual Models", California State University, Monterey Bay, The Jackson Laboratory, Scripps Institution of Oceanography, The Ocean Cleanup Foundation, Center for Marine Debris Research, 2021, [http://arxiv.org/pdf/2105.01882](http://arxiv.org/pdf/2105.01882).  

## Datasets Used  

- **[DeepTrash V2.0](https://universe.roboflow.com/yolov5-thesis-paper/deeptrash-v2.0/dataset/4)** – A comprehensive dataset for training deep learning models on trash classification.  

- **[Neural Ocean Dataset](https://universe.roboflow.com/neural-ocean/neural_ocean)** – Designed for underwater object detection and classification, aiding marine research and pollution monitoring.  

- **[Roboflow Trashcan Dataset](https://universe.roboflow.com/applied-machine-learning/trashcan-dataset)** – A diverse dataset for identifying various types of waste materials in aquatic environments.  

- **[SeaScanner Dataset](https://universe.roboflow.com/hbjl/seascanner)** – Focused on marine debris detection to enhance environmental monitoring efforts.  


---
 **Aquaeye is committed to leveraging AI for a cleaner ocean!** 🌊♻  
