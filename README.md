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
-  **TensorFlow & Librosa** (for AI processing)
-  **Sounddevice** (for microphone input)
-  **Arduino IDE** (for programming the Arduino)
-  **Teachable Machine** (for training the AI model)

### **How It Works**
-Step 1: Capture Live Audio The PC microphone records audio in real time. The audio is preprocessed into MFCC features (Mel Frequency Cepstral Coefficients). The AI model (trained using Teachable Machine) classifies the sound.
-Step 2: Send Classification to Arduino The Python script sends "LOUD" or "QUIET" to the Arduino over Serial.
-Step 3: Arduino Controls LED If "LOUD" is detected → LED Blinks If "QUIET" is detected → LED Turns Off
