#pragma once

#include "../../common/tfhe_kats.h"
#include "my_basic_algorithm_tfhe.h"

using namespace MY_BASIC_ALGORITHM;

// build an array of KnownAnswerTests for MY_BASIC_ALGORITHM
TFHEKnownAnswerTest<MY_BASIC_ALGORITHM_TFHE> KNOWN_ANSWER_TESTS[] = {
    
    // "dec_test()"
    // {
    //     {0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55,
    //      0x55, 0x55, 0x55, 0x55},
    //     {0x00, 0x00, 0x00, 0x00, 0x00, 0x00},
    //     {0x89, 0xA3, 0xB7, 0x00, 0xD9, 0x44},
    //     128,
    //     TFHEKnownAnswerTest<MY_BASIC_ALGORITHM_TFHE>::Testcase::DEC,
    // },


    // // "test()"
    // {
    //     // key
    //     {0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55,
    //      0x55, 0x55, 0x55, 0x55},
        
    //     // plaintext (unused because this test case randomly generates one)
    //     {0x00},

    //     // ciphertext (unused too)
    //     {0x00},

    //     // security level
    //     128,

    //     // test case type
    //     TFHEKnownAnswerTest<MY_BASIC_ALGORITHM_TFHE>::Testcase::USE_CASE,

    //     // N
    //     5,

    //     // bitsize
    //     16,
    // }

    // "test()"
    {
        // key
        {0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55,
         0x55, 0x55, 0x55, 0x55},
        
        // plaintext (unused because this test case randomly generates one)
        {0x00},

        // ciphertext (unused too)
        {0x00},

        // security level
        128,

        // test case type
        TFHEKnownAnswerTest<MY_BASIC_ALGORITHM_TFHE>::Testcase::USE_CASE,

        // N
        2,

        // bitsize
        8,
    },
};
