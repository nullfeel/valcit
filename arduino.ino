#import <Mouse.h>
char userInput;

void setup(){
	
	Serial.begin(9600);                        //  setup serial
	Mouse.begin();
}

void loop(){

if(Serial.available()> 0){ 
    
    userInput = Serial.read();               // read user input
      if(userInput == '1'){                  // if we get expected value 
		Mouse.click();
      } // if user input 'g' 
  } // Serial.available
} // Void Loop


