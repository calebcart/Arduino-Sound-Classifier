# Arduino-Sound-Classifier
This is my first project for IT 254, it receives audio input from a microphone and classifies that audio as either loud or quiet. Then, it sends that information to the Arduino to indicate the result with an LED.
## **Hardware & Software Requirements**
### **Hardware**
-  **PC/Laptop** (for running AI model)
-  **Microphone** (built-in or external)
-  **Arduino Mega 2560 R3** (or any Arduino with Serial support)
-  **LED** (if using an external LED)

### **Software**
-  **Python 3.9+** 
-  **TensorFlow, Librosa, Numpy, Serial** 
-  **Sounddevice** (for microphone input)
-  **Arduino IDE** (for programming the Arduino)
-  **Teachable Machine** (for training the AI model)

### **How It Works**
Step 1: Capture Live Audio: The PC microphone records audio in real-time. The audio is preprocessed into MFCC features (Mel Frequency Cepstral Coefficients). The AI model (trained using Teachable Machine) classifies the sound.
Step 2: Send Classification to Arduino: The Python script sends "LOUD" or "QUIET" to the Arduino over Serial.
Step 3: Arduino Controls LED: If "LOUD" is detected → LED Blinks If "QUIET" is detected → LED Turns Off.

### **Model conversion**
To use the teachable machine AI model with Python you need to convert it to a Keras file which you can do here. 
link to google colab: https://colab.research.google.com/drive/136izxZaAaGeL8-204RvE6p6p1DE9sZnD?usp=sharing

### **Explanation Video**
https://drive.google.com/file/d/1U_xbUGCU4PvaBjzvCqjvc_vrA6r-eSsr/view?usp=sharing
