#include "ADS1X15.h"
 
ADS1115 ADS(0x48);

#define V_S 3.3
float LOCAL_AIR_PRESSURE = 101.2; // sea level pressure in kPa
int counter = 0;
bool first_scan = true;
int16_t raw_1;  
float p_1;
float offset = 0;


float vdig_to_p(int v_dig){
  float v_out = v_dig/65536.0;
  return ((v_out/V_S)+0.95)/0.009-offset;
  
}
void setup() {
  // put your setup code here, to run once:

  Serial.begin(460800);
  Serial.setTimeout(1);

  Wire.begin();
  ADS.begin();
}

void loop() {
  ADS.setGain(1);
  
//  if (first_scan) {
//    float sum = 0;
//    int loops = 100;
//    for(int i=0; i < loops; i++){
//      sum = sum + vdig_to_p(ADS.readADC_Differential_0_1());
//    }
//    offset = float(sum/loops) - LOCAL_AIR_PRESSURE;
//    Serial.println(offset);
//    first_scan = false;
//  }

  
  if (Serial.read() == 'g'){

    raw_1 =  ADS.readADC_Differential_0_1(); //ADS.readADC(0); 
    p_1 = vdig_to_p(raw_1);

    int16_t val_1 = ADS.readADC(1);  
//    int16_t val_2 = ADS.readADC(2);  
//    int16_t val_3 = ADS.readADC(3);
  
    float f = ADS.toVoltage(1);  // voltage factor

    
    Serial.print("P1:");
    Serial.println(p_1);
//    Serial.println(", ");
  
//    Serial.print("P2:");
//    Serial.println(val_1*f);
//    Serial.print(", ");
//  
//    Serial.print("P3:");
//    Serial.print(val_2);
//    Serial.print(", ");
//  
//    Serial.print("P4:");
//    Serial.print(val_3);
//    Serial.print(", ");
//  
//    Serial.print("P5:");
//    Serial.print(analogRead(A4));
//    Serial.print(", ");
//  
//    Serial.print("P6:");
//    Serial.println(analogRead(A5));
//    Serial.println("");
  }

}
