#include <stdio.h>

int global_data = 123;
int global_bss;
const int global_ro = 456;

int main() {
    int local_data = 789;
    char str[] = "Salve, simpatia!";
    
    printf("%p -> global_data  = %d\n", &global_data, global_data);
    printf("%p -> global_bss   = %d\n", &global_bss,  global_bss);
    printf("%p -> global_ro    = %d\n", &global_ro, global_ro);
    printf("%p -> local_data   = %d\n", &local_data, local_data);
    printf("%p -> str          = %s\n", str, str);
    printf("%p -> main\n", &main);

    
    
    return 0;
}
