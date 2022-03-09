#include <Arduino.h>
#include <Servo.h>
Servo m1;   //Top motor
Servo m2;   //Bottom motor
Servo s1;
Servo s2;
Servo s3;
Servo s4;

int pos = 0;

int eq1=100;
int eq2=80;
int eq3=90;
int eq4=80;

void set(int w, int x, int y, int z){
    s1.write(w+eq1);
    s2.write(x+eq2);
    s3.write(y+eq3);
    s4.write(z+eq4);

}

void execute()
{
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
    Serial.write("LED cycle\n");


    set(0,0,0,0);
    /*
    m1.write(0);
    for (pos = 0; pos <= 100; pos += 10) { 
        m1.write(pos);
        m2.write(pos);
        delay(200);
    }
    */



    /*
    //Throttle up in increments of 10 staying on each step for 3 seconds
    for (pos = 0; pos <= 100; pos += 10) { 
        m1.write(pos);              
        m2.write(pos);
        delay(200);
    }


    Serial.println("130");
    delay(5500);                
    set(5,-5,0,0);
    Serial.println("5");                       
    delay(5500);
    set(10,-10,0,0);
    Serial.println("10");                       
    delay(5500);
    set(15,-15,0,0);
    Serial.println("15");                       
    delay(5500);
    set(20,-20,0,0);
    Serial.println("20");                       
    delay(5500);
    set(25,-25,0,0);
    Serial.println("25");                       
    delay(5500);
    set(30,-30,0,0);
    Serial.println("30");                       
    delay(5500);
    set(0,0,0,0);

    
    //Throttle down
    for (pos = 100; pos >=0; pos -= 20) { 
        m1.write(pos);              
        m2.write(pos);
        delay(150);                       
    }
    */    
    
    
    
}


void setup()
{
    // put your setup code here, to run once:
    delay(2000);
    pinMode(13, OUTPUT);
    Serial.begin(9600);
    m1.attach(29);
    m2.attach(30);
    s1.attach(5);
    s2.attach(20);
    s3.attach(4);
    s4.attach(21);
}

void loop()
{
    execute();
}