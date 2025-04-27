# Hand Draw Drawing Pad ✍️🖐️🎨  
**Hand Draw Drawing Pad** is a real-time, gesture-controlled drawing application built using **computer vision and hand tracking**.  
It allows users to **draw, erase, select shapes, colors, and text** completely in the air — using simple hand gestures without touching any device.

Have a look at how it works:  
https://www.linkedin.com/posts/vijinigiri-gowri-shankar_computervision-opencv-gesturecontrol-activity-7305864016478777344-0XY9?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEOGt5gB-inZKogxJE16RC3MCMV8L40E30M

## 🔧 Features

- ✍️ **Draw in the air** using pinch gestures via webcam  
- 🎨 **Select colors**, **change pen thickness**, and **use eraser** with gestures  
- 📝 **Insert text** onto the canvas using hand controls  
- ↩️ **Undo actions** and **clear screen** gestures  
- 📐 **Shape detection** and **auto-correction** for perfect lines and circles (95% accuracy)  
- 📸 **Save your artwork** directly from the interface  
- ⚙️ Real-time hand tracking using **MediaPipe** and **OpenCV**  
- 🖐️ Fully touchless, intuitive experience  

## 📦 Tech Stack

- **Python**  
- **OpenCV**  
- **MediaPipe** (for hand tracking)  
- **NumPy**  
- **CVZone** (for easier hand landmark handling)  

## 📁 Project Structure

- `app.py`: Main script handling drawing, gesture control, and canvas rendering  
- `utils/`: Helper functions for shape recognition, undo stack, and screen management  
- `assets/`: (Optional) Images or tool icons used for the interface  

## 🚀 Usage

1. Connect your webcam and run the application:  
   ```bash
   python app.py
   ```
2. Use the **pinch gesture** (thumb and index finger) to start drawing.  
3. Show different gestures to switch between tools (eraser, color picker, text, undo, etc.).  
4. Draw shapes naturally — the app automatically corrects them into perfect lines or circles.  
5. Save your final drawing if needed.

## 📌 Notes

- Ensure good lighting conditions for better hand tracking.  
- Keep gestures steady while selecting tools.  
- Ideal for digital whiteboards, educational tools, futuristic drawing interfaces, and air gesture control systems.

## 🏷️ Tags

#ComputerVision #HandTracking #OpenCV #DrawingPad #GestureControl #PythonProjects #AIProjects #TouchlessDrawing #AirDrawing #MachineLearning
