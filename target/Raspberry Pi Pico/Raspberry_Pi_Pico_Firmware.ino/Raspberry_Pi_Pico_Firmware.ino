int i, j;
int dely;

void setup() {
  Serial.begin(115200);
  pinMode(22, OUTPUT);
  j=0;
  i=0;
}

void loop() {
  Serial.println(i+j);
  i++;
  digitalWrite(22, HIGH);
  for(dely = 10000000; dely > 0; dely--){
    j = dely;
  }   
  digitalWrite(22, LOW);
}
