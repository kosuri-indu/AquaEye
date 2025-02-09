# Aquaeye: Detecting Debris Pollution in Aquatic Systems  

<p align="center">
    <img src="https://github.com/user-attachments/assets/8918405f-55c9-4299-9655-64c3efdf0d04" width="45%" height="250px" style="object-fit: cover;">
    <img src="https://github.com/user-attachments/assets/cf2e3094-09a9-454e-aa76-e1d3f62c1eac" width="45%" height="250px" style="object-fit: cover;">
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/5554bbbb-a68b-4cdd-8587-53b35d67ea3b" width="35%" height="250px" style="object-fit: cover;">
    <img src="https://github.com/user-attachments/assets/e6c3879e-9b61-45a7-bac4-79ebfe2b2efc" width="55%" height="250px" style="object-fit: cover;">
</p>

## Overview  

Managing waste effectively in aquatic systems is crucial for preserving marine life, ecosystems, and biodiversity. **Aquaeye** uses deep learning techniques to detect and classify submerged debris, including marine life thereby promoting a cleaner and more sustainable environment.  

## What Aquaeye Does  

✅ **Debris Detection** – Uses state-of-the-art AI models to identify and classify debris submerged underwater.  
✅ **Marine Life Detection** – Detects marine life to differentiate them with the debris.  
✅ **Environmental Insights** – Provides data and insights for better decision-making regarding underwater cleanup and conservation.  

## Why Aquaeye?  

- **Environmental Impact:** Contributes to preserving marine life and reducing underwater pollution.  
- **Advanced Technology:** Employs cutting-edge AI models for superior detection in challenging underwater environments.  
- **Scientific Benefits:** Supports researchers, conservationists, and policymakers with valuable insights and data visualization tools.  
## Key Features  

1. **High Precision Detection:** Employs various deep learning models to identify submerged debris.  
2. **Data Visualization:** Uses Dash to present a **quantification, degradation factor, and classification dashboard** for better pollution analysis.  
3. **Detection of Marine Life:** Identifies and classifies various marine species to aid in conservation efforts.  
4. **Degradation Tracker:** Monitors the degradation of detected debris over time.  
5. **Safety Level Checker:** Assesses the safety level of the detected debris for cleanup operations.  
6. **Detection in Low Visibility:** Capable of detecting debris and marine life even in low-visibility underwater environments.  

## Workflow

![WhatsApp Image 2025-02-08 at 09 31 39_dbeb3372](https://github.com/user-attachments/assets/8977f0fd-4a72-4354-b9f6-c9b047b1a1a8)


## How We Are Building It  

| **Component**           | **Technology Stack**                          |
|------------------------|----------------------------------------------|
| **Programming Language** | Python                                      |
| **Backend Frameworks**   | Flask, PyTorch, Roboflow                    |
| **Deep Learning Model**  | YOLOv5, YOLOv8 YOLOv11, Roboflowv3          |
| **Data Visualization**   | Plotly, Dash                                |
| **Hardware**             | Google Colab TPU                            |

## Challenges Faced  

- **Data Availability:** Limited and diverse underwater datasets made training challenging.  
- **Noisy Environments:** Dealing with **low-visibility underwater settings** required advanced pre-processing techniques.  
- **Computational Constraints:** Training deep learning models on large datasets required **optimization techniques**.  

## What's Next for Aquaeye?  

- **Expanding Dataset** – Collect and diversify the training data for better generalization.  
- **Improving Processing Speed** – Optimize real-time detection for faster inference.  
- **Trying More Models** – Experiment with **YOLOv8, EfficientDet, and Transformer-based models**.  
- **Enhancing Accuracy** – Fine-tune models to improve **precision, recall, and F1 score**.

## Team

| **Name**           | 
|--------------------|
| Kosuri Lakshmi Indu          | 
| Koppol Venkata Sai Sahithi         |
| Namratha Sriram      |  
| Anamitra Joshi          | 

## Research & References

- Tianlong Jia, Zoran Kapelan, Rinze de Vries, Paul Vriend, Eric Copius Peereboom, Imke Okkerman, Riccardo Taormina, "Deep learning for detecting macroplastic litter in water bodies: A review", Water Research, Volume 231, 2023, 119632, ISSN 0043-1354, [https://doi.org/10.1016/j.watres.2023.119632](https://doi.org/10.1016/j.watres.2023.119632).  

- Abdelaadim Khriss, Aissa Kerkour Elmiad, Mohammed Badaoui, Alae-Eddine Barkaoui, Yassine Zarhloule, "Exploring Deep Learning for Underwater Plastic Debris Detection and Monitoring", Journal of Ecological Engineering, Volume 25, Issue 7, 2024, ISSN 2299-8993, [https://doi.org/10.12911/22998993/187970](https://doi.org/10.12911/22998993/187970).  

- Gautam Tataa, Jay Lowe, Olivier Poirion, Sarah-Jeanne Royer, "A Robotic Approach towards Quantifying Epipelagic Bound Plastic Using Deep Visual Models", California State University, Monterey Bay, The Jackson Laboratory, Scripps Institution of Oceanography, The Ocean Cleanup Foundation, Center for Marine Debris Research, 2021, [http://arxiv.org/pdf/2105.01882](http://arxiv.org/pdf/2105.01882).  

## Datasets Used  

- **[DeepTrash V2.0](https://universe.roboflow.com/yolov5-thesis-paper/deeptrash-v2.0/dataset/4)** – A comprehensive dataset for training deep learning models on trash classification.  

- **[Neural Ocean Dataset](https://universe.roboflow.com/neural-ocean/neural_ocean)** – Designed for underwater object detection and classification, aiding marine research and pollution monitoring.  

- **[Underwater Marine Species Dataset](https://universe.roboflow.com/california-state-university-east-bay-wkf0d/underwater-marine-species/model/6)** – A diverse dataset for identifying various types of waste materials in aquatic environments.  

- **[SeaScanner Dataset](https://universe.roboflow.com/hbjl/seascanner)** – Focused on marine debris detection to enhance environmental monitoring efforts.


