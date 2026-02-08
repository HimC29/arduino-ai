void setup() {
  Serial.begin(9600);
}

void output(String args) {
  int len = args.length();
  if (len < 2) return;

  char state = args[len - 1];
  int pin = args.substring(0, len - 1).toInt();

  if (pin >= 0 && pin <= 13) {
    pinMode(pin, OUTPUT);
    if (state == 'h' || state == 'H') {
      digitalWrite(pin, HIGH);
    } else if (state == 'l' || state == 'L') {
      digitalWrite(pin, LOW);
    }
  }
}

void input(String args) {
  int pin = args.toInt();
  if (pin >= 0 && pin <= 13) {
    pinMode(pin, INPUT);
    int value = digitalRead(pin); 
    
    Serial.print("PIN_");
    Serial.print(pin);
    Serial.print(":");
    Serial.println(value == HIGH ? "HIGH" : "LOW");
  }
}

void loop() {
  if (Serial.available() > 0) {
    String fullCmd = Serial.readStringUntil('\n');
    fullCmd.trim();

    if (fullCmd.length() < 2) return;

    char type = fullCmd.charAt(0);
    String args = fullCmd.substring(1);

    if (type == 'o') {
      output(args);
    } else if (type == 'i') {
      input(args);
    }
  }
}