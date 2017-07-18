// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#ifdef __unix__                    /* __unix__ is usually defined by compilers targeting Unix systems */

    #define OS_Windows 0
    #include <unistd.h>
    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>

#elif defined(_WIN32) || defined(WIN32)     /* _Win32 is usually defined by compilers targeting 32 or   64 bit Windows systems */

    #define OS_Windows 1
    #include <windows.h>
    #include <stdio.h>
    #include <tchar.h>
    #define DIV 1048576
    #define WIDTH 7

#endif

// TODO: reference additional headers your program requires here
