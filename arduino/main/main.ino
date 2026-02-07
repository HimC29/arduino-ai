void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    int len = cmd.length();
    if(len < 2) return;

    char state = cmd[len - 1];
    int pin = cmd.substring(0, len - 1).toInt();

    if(pin >= 0 && pin <= 13) {
      if(state == 'h' || state == 'H') {
        digitalWrite(pin, HIGH);
      }
      else if(state == 'l' || state == 'L') {
        digitalWrite(pin, LOW);
      }
    }
  }
}
