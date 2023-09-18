#include <fenv.h>
#include <cmath>

//Comment compiler ?
//g++ -shared -o float_rounder.so float_rounder.cpp

extern "C" {

    //Arrondit vers l'infini négatif.
    int get_FE_DOWNWARD() {
        return FE_DOWNWARD;
    }

    //Arrondit vers zéro.
    int get_FE_TOWARDZERO() {
        return FE_TOWARDZERO;
    }

    //Arrondit vers l'infini positif.
    int get_FE_UPWARD() {
        return FE_UPWARD;
    }
    
    //Arrondit vers le nombre le plus proche. En cas d'égalité, arrondit vers le nombre pair le plus proche.
    int get_FE_TONEAREST() {
        return FE_TONEAREST;
    }

    double add(double x, double y, int rounding) {
        fesetround(rounding);
        return x + y;
    }

    double sub(double x, double y, int rounding) {
        fesetround(rounding);
        return x - y;
    }

    double mul(double x, double y, int rounding) {
        fesetround(rounding);
        return x * y;
    }

    double _div(double x, double y, int rounding) {
        fesetround(rounding);
        return x / y;
    }

    double _sqrt(double x, int rounding) {
        fesetround(rounding);
        return sqrt(x);
    }

}

