#ifndef DEBUG_LS_HPP_
#define DEBUG_LS_HPP_
#pragma once

#include "constants.hpp"

// #define debug_print(x) DebugSERIAL.print(x);
// #define debug_println(x) DebugSERIAL.println(x)
// #define debug_printF(x) DebugSERIAL.print(F(x))
// #define debug_printlnF(x) DebugSERIAL.println(F(x))
#define debug_header() DebugSERIAL.print(F("[ DEBUG ] $ "));
#define debug_terminator() DebugSERIAL.print(F("\n"));

//not in use yet
// template<typename T, typename L, size_t N>
// void debug_print(String label, T field_ref){
    
//     if(std::is_same<T, lin::Vector<L, N>>::value)
//         debug_lin_vec(label, field_ref);
//     else{
//         assert(false);
//         // other debug statements dont exist yet!
//     }
// }

template <typename T>
void debug_ele(T a){
    #ifdef DEBUG
    if(std::is_same<T, float>::value || std::is_same<T, double>::value )
        DebugSERIAL.printf("%f", a);
    else if(std::is_same<T, bool>::value){
        if(a) DebugSERIAL.print("true");
        else DebugSERIAL.print("false");
    }
    else
        DebugSERIAL.print(a);  
    #endif  
}

/**
 * @brief Debug print a data value
 * 
 * @tparam T can be a bool, int of any kind, float, double
 * @param label The label of the value
 * @param a The actual value, such as data_fp->get()
 */
template<typename T>
void debug_solo(String label, T a){
    #ifdef DEBUG
    debug_header()
    DebugSERIAL.print(label);

    DebugSERIAL.print(": ");
    debug_ele(a);
    debug_terminator()
    #endif
}

/**
 * @brief Debug print a lin vector
 * 
 * @tparam T lin::Vector of any kind
 * @tparam N Any positive number
 * @param label Label for the lin vec
 * @param lin_vec vector_fp->get() for example
 */
template<typename T, size_t N>
void debug_lin_vec(String label, lin::Vector<T, N> lin_vec){
    #ifdef DEBUG
    debug_header()
    DebugSERIAL.print(label);
    DebugSERIAL.print(": (");
    for(unsigned int i = 0; i < N-1; i++){
        debug_ele(lin_vec(i));
    }
    DebugSERIAL.print(", ");
    debug_ele(lin_vec(N-1));
    DebugSERIAL.print(")");
    debug_terminator()
    #endif
}


#endif