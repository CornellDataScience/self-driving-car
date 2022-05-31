#include <unity.h>
#include <Arduino.h>

void test_task_execute()
{
    TEST_ASSERT(true);
}

int test_control_task()
{
    UNITY_BEGIN();
    RUN_TEST(test_task_execute);
    return UNITY_END();
}

void execute(){
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
    Serial.write("LED cycle\n");
}

#ifdef DESKTOP
int main()
{
    return test_control_task();
}

#else

void setup()
{
    delay(2000);
    pinMode(13, OUTPUT);
    Serial.begin(9600);
    test_control_task();
}

void loop(){
    execute();
}
#endif