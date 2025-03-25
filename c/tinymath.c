#include <stdio.h>

#include "tinymath.h"


void print_vec4f(const vec4f v) {
    printf("[%.6f %.6f %.6f %.6f]\n", v.x, v.y, v.z, v.w);
}

void print_mat4f(const mat4f A) {
    printf(
        "[[%.6f %.6f %.6f %.6f]\n" \
        "[ %.6f %.6f %.6f %.6f]\n" \
        "[ %.6f %.6f %.6f %.6f]\n" \
        "[ %.6f %.6f %.6f %.6f]]\n",
        A.elt[0], A.elt[4], A.elt[8],  A.elt[12],
        A.elt[1], A.elt[5], A.elt[9],  A.elt[13],
        A.elt[2], A.elt[6], A.elt[10], A.elt[14],
        A.elt[3], A.elt[7], A.elt[11], A.elt[15]
    );
}

int main() {
    print_vec4f((vec4f){.x = 1.0f, .y = 2.0f, .z = 3.0f, .w = 4.0f});
    print_vec4f((vec4f){.elt = {1.0f, 2.0f, 3.0f, 4.0f}});
    print_vec4f((vec4f){{1.0f, 2.0f, 3.0f, 4.0f}});

    printf("\n");
    print_mat4f(id4f());
    vec4f a = mvmul4f(id4f(), (vec4f){{1.0f, 2.0f, 3.0f, 4.0f}});
    print_vec4f(a);

    printf("\n");
    mat4f A = (mat4f){.col = {a, a, a, a}};
    print_mat4f(A);

    printf("\n");
    A = matmul4f(A, id4f());
    print_mat4f(A);

    return 0;
}
