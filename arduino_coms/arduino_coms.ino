#include "ADS1X15.h"
 
ADS1115 ADS(0x48);

#define V_S 3.3
float LOCAL_AIR_PRESSURE = 101.2; // sea level pressure in kPa
int counter = 0;
bool first_scan = true;
int16_t raw_1, raw_2;
float p_1, p_2;
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
  ADS.setGain(1);
  
}

void loop() {
  
  raw_1 =  ADS.readADC_Differential_0_1(); //ADS.readADC(0); 
  p_1 = vdig_to_p(raw_1);
  
  raw_2 =  ADS.readADC_Differential_2_3(); //ADS.readADC(0); 
  p_2 = vdig_to_p(raw_2);
  
  if (Serial.read() == 'g'){
    Serial.print("P1:");
    Serial.print(p_1);
    Serial.print(",");

    Serial.print("P2:");
    Serial.println(p_2);
  }

}
