#define LED_PIN 8  // Define the pin for the external LED on the breadboard

void setup() {
  Serial.begin(9600);         // Set baud rate to match your Python script
  pinMode(LED_PIN, OUTPUT);   // Configure LED pin as output
}

void loop() {
  if (Serial.available() > 0) {
    // Read a line of text from the serial buffer
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Control the LED based on the incoming command
    if (command == "LOUD") {
      digitalWrite(LED_PIN, HIGH); // Turn ON LED
    } else if (command == "QUIET") {
      digitalWrite(LED_PIN, LOW);  // Turn OFF LED
    }
  }
}

