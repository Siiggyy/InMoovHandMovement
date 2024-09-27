#include <Servo.h>

Servo servothumb;          // Define thumb servo
Servo servoindex;          // Define index servo
Servo servomajeure;
Servo servoringfinger;
Servo servopinky;
Servo servowrist;
Servo servobiceps;
Servo servorotate;
Servo servoshoulder;
Servo servoomoplat;
Servo servoneck;
Servo servorothead;
int incomingByte = 0; // for incoming serial data

void setup() { 
  servothumb.attach(2);  // Set thumb servo to digital pin 2
  servoindex.attach(3);  // Set index servo to digital pin 3
  servomajeure.attach(4);
  servoringfinger.attach(5);
  servopinky.attach(6);
  servowrist.attach(7);
  servobiceps.attach(8);
  servorotate.attach(9);
  servoshoulder.attach(10);
  servoomoplat.attach(11);
  servoneck.attach(12);
  servorothead.attach(13);
  Serial.begin(9600);
  alltovirtual();   
  
} 

void loop() {            // Loop through motion tests
  //alltovirtual();        // Example: alltovirtual
  //servothumbSweep();
  //fingerSweepWithOffsetAndReverse();
  //delay(4000);           // Wait 4000 milliseconds (4 seconds)
//alltorest();           // Uncomment to use this
//delay(4000);           // Uncomment to use this
//alltomax();            // Uncomment to use this
//delay(2000);           // Uncomment to use this

  if (Serial.available() > 0) {
    // Read the incoming byte
    incomingByte = Serial.parseInt(); // Using parseInt to handle multiple bytes as integer
    Serial.println(incomingByte);
    // Say what you got
    //Serial.print("I received: ");
    //Serial.println(incomingByte, DEC);

    // Call the new function to map the input to the correct finger
    controlFingerBySerialInput(incomingByte);
  }
  
 
}

void fingerSweepWithOffsetAndReverse() {
  int totalRange = 150;    // Total range of motion for servos
  int offset = totalRange / 5;  // Each finger will start after thumb moves 1/5 of its range

  // Sweep servos with offset (move to 180)
  for (int pos = 0; pos <= totalRange; pos++) {
    // Thumb starts immediately
    //servothumb.write(pos);
    
    // Each finger starts with an increasing offset but all reach 180
    if (pos >= offset) {
      servoindex.write(map(pos, offset, totalRange, 0, totalRange));
    }
    
    if (pos >= 2 * offset) {
      servomajeure.write(map(pos, 2 * offset, totalRange, 0, totalRange));
    }
    
    if (pos >= 3 * offset) {
      servoringfinger.write(map(pos, 3 * offset, totalRange, 0, totalRange));
    }
    
    if (pos >= 4 * offset) {
      servopinky.write(map(pos, 4 * offset, totalRange, 0, totalRange));
    }

    delay(15);  // Delay for smooth motion
  }

  delay(1000);  // Pause before reversing the motion
  
  // Reverse motion (move back to 0 in reverse order)
  for (int pos = totalRange; pos >= 0; pos--) {
    // Pinky moves first in reverse
    if (pos <= 4 * offset) {
      servopinky.write(map(pos, 0, 4 * offset, 0, totalRange));
    }
    
    // Ring finger moves next
    if (pos <= 3 * offset) {
      servoringfinger.write(map(pos, 0, 3 * offset, 0, totalRange));
    }
    
    // Middle finger moves next
    if (pos <= 2 * offset) {
      servomajeure.write(map(pos, 0, 2 * offset, 0, totalRange));
    }
    
    // Index finger moves next
    if (pos <= offset) {
      servoindex.write(map(pos, 0, offset, 0, totalRange));
    }
    
    // Thumb moves last
    //servothumb.write(pos);  // Thumb moves back last
    
    delay(15);  // Delay for smooth motion
  }
}

void controlFingerBySerialInput(int input) {
  // The input value should correspond to a specific finger and its position
  // Let's say:
  // 1-180 -> Thumb position (1 to 180 degrees)
  // 181-360 -> Index finger (1 to 180 degrees)
  // 361-540 -> Middle finger (1 to 180 degrees)
  // 541-720 -> Ring finger (1 to 180 degrees)
  // 721-900 -> Pinky finger (1 to 180 degrees)

  if (input >= 1 && input <= 180) { //85
    int mappedInput = map(input, 1, 180, 1, 85);
    servothumb.write(mappedInput);  // Control thumb
    //Serial.println("Thumb moved");
  } 
  else if (input >= 181 && input <= 360) { //330
    int mappedInput = map(input, 181, 360, 1, 150);  // Map to 330 max for index finger
    servoindex.write(mappedInput);
    //servoindex.write(input - 180);  // Control index finger
    //Serial.println("Index finger moved");
  } 
  else if (input >= 361 && input <= 540) { //490
    int mappedInput = map(input, 361, 540, 1, 130);
    servomajeure.write(mappedInput);  // Control middle finger
    //Serial.println("Middle finger moved");
  } 
  else if (input >= 541 && input <= 720) { //700
  int mappedInput = map(input, 541, 720, 1, 160);
    servoringfinger.write(mappedInput);  // Control ring finger
    //Serial.println("Ring finger moved");
  } 
  else if (input >= 721 && input <= 900) { //875
  int mappedInput = map(input, 721, 900, 1, 155);
    servopinky.write(mappedInput);  // Control pinky finger
    //Serial.println("Pinky finger moved");
  } else if (input = 0) {}
  else {
    Serial.println("Invalid input");
  }
}


void servothumbSweep() {
  // Sweep from 0 to 180 degrees
  for (int pos = 0; pos <= 100; pos += 1) { // Increment by 1 degree
    servothumb.write(pos);                  // Move servo to 'pos'
    servoringfinger.write(pos);
    //servopinky.write(pos);
    delay(15);                              // Delay for smooth motion
  }

  // Sweep back from 180 to 0 degrees
  for (int pos = 100; pos >= 0; pos -= 1) { // Decrement by 1 degree
    servothumb.write(pos);                  // Move servo to 'pos'
    servoringfinger.write(pos);
    //servopinky.write(pos);
    delay(15);                              // Delay for smooth motion
  }
}

// Motion to set the servo into "virtual" 0 position: alltovirtual
void alltovirtual() {         
  servothumb.write(0);
  servoindex.write(0);
  servomajeure.write(0);
  servoringfinger.write(0);
  servopinky.write(0);
  servowrist.write(0);
  servobiceps.write(0);  
  servorotate.write(20);    //Never less then (20 degree)
  servoshoulder.write(30);  //Never less then (30 degree)
  servoomoplat.write(10);   //Never less then (10 degree)
  servoneck.write(0);
  servorothead.write(0);
}
// Motion to set the servo into "rest" position: alltorest
void alltorest() {         
   servothumb.write(0);
  servoindex.write(0);
  servomajeure.write(0);
  servoringfinger.write(0);
  servopinky.write(0);
  servowrist.write(0);
  servobiceps.write(0);     
  servorotate.write(90);    //Never less then (20 degree)
  servoshoulder.write(30);  //Never less then (30 degree)
  servoomoplat.write(10);   //Never less then (10 degree)
  servoneck.write(90);
  servorothead.write(90);
}



// Motion to set the servo into "max" position: alltomax
void alltomax() {
  servothumb.write(180);
  servoindex.write(180);
  servomajeure.write(180);
  servoringfinger.write(180);
  servopinky.write(180);
  servowrist.write(180);
  servobiceps.write(85);      //Never more then (85 or 90degree)
  servorotate.write(110);     //Never more then (110 degree)
  servoshoulder.write(130);   //Never more then (130 degree)
  servoomoplat.write(70);     //Never more then (70 degree)
  servoneck.write(180);
  servorothead.write(180);
 
}
