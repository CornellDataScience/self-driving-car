#include "../StateFieldRegistryMock.hpp"

#include <Wire.h>
#include <Adafruit_Sensor.h>
    
#include "../../src/FCCode/BMPMonitor.hpp"

#include <unity.h>

class TestFixture {
    public:
        StateFieldRegistryMock registry;

        InternalStateField<bool>* functional_fp;

        // pointers to output statefields for easy access
        InternalStateField<float>* temp_fp;
        InternalStateField<float>* pressure_fp;
        InternalStateField<float>* altitude_fp;

        //pointer to control task
        std::unique_ptr<BMPMonitor> bmp_monitor;

        Adafruit_BMP280 bmp;
        
        // Create a TestFixture instance of AttitudeEstimator with pointers to statefields
        TestFixture() : registry(){
            bmp_monitor = std::make_unique<BMPMonitor>(registry, 0);  

            // initialize pointers to statefields
            functional_fp = registry.find_internal_field_t<bool>("bmp.functional");
            temp_fp = registry.find_internal_field_t<float>("bmp.temp");
            pressure_fp = registry.find_internal_field_t<float>("bmp.pressure");
            altitude_fp = registry.find_internal_field_t<float>("bmp.altitude");
        }
};

//checks that all ref vector and actual vector are pretty much the same
void elements_same(const std::array<float, 3> ref, const std::array<float, 3> actual){
    TEST_ASSERT_FLOAT_WITHIN(0.001, ref[0], actual[0]);
    TEST_ASSERT_FLOAT_WITHIN(0.001, ref[1], actual[1]);
    TEST_ASSERT_FLOAT_WITHIN(0.001, ref[2], actual[2]);
}

void test_task_initialization()
{
    TestFixture tf;
}

void test_execute(){
    TestFixture tf;

    tf.bmp_monitor->execute();

    float read_temp = tf.temp_fp->get();
    float read_pressure = tf.pressure_fp->get();
    float read_altitude = tf.altitude_fp->get();

    Serial.printf("Functional: ");
    Serial.printf(tf.functional_fp->get() ? "true\n" : "false\n");

    Serial.printf("Temp (C): %f\n", read_temp);
    //assert within 10 degrees of 21 C for indoor testing lmao
    TEST_ASSERT_FLOAT_WITHIN(10, 21, read_temp);

    Serial.printf("Pressure (Pa): %f\n", read_pressure);
    //assert within 2000 Pa of 101000 Pa?
    TEST_ASSERT_FLOAT_WITHIN(2000, 101000, read_pressure);

    Serial.printf("Altitude (m): %f\n", read_altitude);
    TEST_ASSERT_FLOAT_WITHIN(700, 500, read_altitude);
}

int test_control_task()
{
        UNITY_BEGIN();
        RUN_TEST(test_task_initialization);
        RUN_TEST(test_execute);
        return UNITY_END();
}

//for lodestar we won't run tests in desktop? idk
#ifdef DESKTOP
int main()
{
        return test_control_task();
}
#else
#include <Arduino.h>
void setup()
{
        delay(2000);
        Serial.begin(9600);
        test_control_task();
}

void loop() {}
#endif