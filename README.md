# **SketchSense AI** 
**Transform Images into Pencil Sketches and Detect Objects Using AI!**


## **Overview**
**SketchSense AI** is a web-based application designed to make image processing fun and intelligent. With just a simple image upload, users can:  
1. **Generate a pencil sketch** of the image.  
2. **Detect objects** in the image using state-of-the-art AI models.  


## **Features**
- **Pencil Sketch Generator:** Converts your uploaded images into stunning pencil sketches using advanced image processing techniques.  
- **Object Detection:** Identifies and labels objects in images using the powerful YOLOv8 model.  


## **Technologies Used**
### **Frontend**
- **HTML5** and **CSS3** for a responsive and visually appealing interface.  
- A dynamic and user-friendly layout that resonates with the artistic vibe of SketchSense AI.  

### **Backend**
- **Flask** to handle server-side logic, routing, and API integration.  

### **AI/ML**
- **OpenCV:** For grayscale conversion, color inversion, blurring, and blending techniques.  
- **Ultralytics YOLOv8:** A pre-trained model for real-time object detection.  
- **PyTorch:** To support YOLOv8 computations and efficient AI modeling.  

### **Utilities**
- **Pillow** and **NumPy** for image handling and processing.  


## **How It Works**
### **Pencil Sketch Generation**
1. **Convert to Grayscale**: Focus on intensity levels of the image.  
2. **Invert Colors**: Create a "negative" of the grayscale image.  
3. **Apply Gaussian Blur**: Smooth the image for a natural pencil stroke effect.  
4. **Blend Images**: Combine the grayscale and blurred images using a dodge blend technique.  

### **Object Detection**
1. Upload an image for processing.  
2. YOLOv8 model detects objects, annotating them with bounding boxes and confidence scores.  
3. The processed image is displayed back to the user.  

## **Screenshots**
### **Landing Page**
![Landing Page](screenshots/landing.png "Landing Page")

### **Result**
![Result](screenshots/result.png "Result")


## **Getting Started**
### **Prerequisites**
- Python 3.7+  
- Git  

### **Installation**
1. Clone the repository:  
   ```bash
   git clone https://github.com/anjaliheda/SketchSense-AI.git
   cd SketchSense-AI
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the application:  
   ```bash
   python app.py
   ```  
4. Open `http://127.0.0.1:5000` in your browser.  


## **Contributing**
Feel free to fork the repository and submit a pull request. Suggestions and improvements are always welcome!  


## **Acknowledgments**
- Thanks to [Ultralytics](https://github.com/ultralytics) for the YOLOv8 model.  
- Inspiration and guidance from OpenCV tutorials and Flask documentation.  
