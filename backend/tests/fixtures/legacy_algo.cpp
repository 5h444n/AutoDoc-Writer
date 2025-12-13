#include <iostream>
using namespace std;

// Old school C++ pointer arithmetic
void weird_swap(int *xp, int *yp) {
    if (xp == yp) return;
    *xp = *xp + *yp;
    *yp = *xp - *yp;
    *xp = *xp - *yp;
}

int main() {
    int x = 10, y = 20;
    weird_swap(&x, &y);
    return 0;
}