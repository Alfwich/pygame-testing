#include <string>
//test.cpp
#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT int sum(int a, int b) {
    return a + b;
}
