//fig 12-5
//  *************************************************************
//  *                                                           *
//  *   P A S C A L   R U N T I M E   L I B R A R Y             *
//  *                                                           *
//  *   Note that all formal parameters are reversed to         *
//  *   accomodate the Pascal calling convention of the         *
//  *   compiled code.                                          *
//  *                                                           *
//  *   All floating point parameters are passed in as longs    *
//  *   to bypass unwanted type conversions.  Floating point    *
//  *   function values are also returned as longs.             *
//  *                                                           *
//  *   Copyright (c) 1996 by Ronald Mak                        *
//  *   For instructional purposes only.  No warranties.        *
//  *                                                           *
//  *************************************************************

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#define MAX_SOURCE_LINE_LENGTH  256

typedef enum {
    FALSE, TRUE
} BOOLEAN;

union {
    float real;
    long  dword;
} value;

//--------------------------------------------------------------
//  main                The main routine, which calls           
//                      _PascalMain, the "main" of the compiled
//                      program.                                
//--------------------------------------------------------------

