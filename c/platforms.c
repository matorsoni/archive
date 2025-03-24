#include <stdio.h>

int main()
{
    #if defined(__STDC__)
	    puts("__STDC__ macro defined (C89).");
    #endif

    #ifdef __STDC_VERSION__
        printf("__STDC_VERSION__ macro defined: %ld\n", __STDC_VERSION__);
        #if (__STDC_VERSION__ >= 199901L)
            puts("C99 compatible.");
        #endif
    #endif

    #ifdef __cplusplus
        printf("__cplusplus macro defined: %ld\n", __cplusplus);
    #else
        puts("__cplusplus macro not defined.");
    #endif

    #ifdef __clang__
        printf("Clang compiler identified: version %d.%d.%d\n", __clang_major__, __clang_minor__, __clang_patchlevel__);
    #endif

    #ifdef __GNUC__
        printf("GCC compiler identified: version %d.%d.%d\n", __GNUC__, __GNUC_MINOR__, __GNUC_PATCHLEVEL__);
    #endif

    return 0;
}
