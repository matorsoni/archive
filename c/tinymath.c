#include <stdio.h>

typedef union {
    struct { float x, y, z, w; };
    float data[4];
} vec4f;

typedef union {
    vec4f cols[4];
    float data[16];
} mat4f;

#define EX4F (vec4f){.data = {1.0f, 0.0f, 0.0f, 0.0f}}
#define EY4F (vec4f){.data = {0.0f, 1.0f, 0.0f, 0.0f}}
#define EZ4F (vec4f){.data = {0.0f, 0.0f, 1.0f, 0.0f}}
#define EW4F (vec4f){.data = {0.0f, 0.0f, 0.0f, 1.0f}}

#define ID4F (mat4f){.cols = {EX4F, EY4F, EZ4F, EW4F}}
#define M4F_ROW(A, i) (vec4f){.data = {(A)->data[0][(i)], (A)->data[1][(i)], (A)->data[2][(i)], (A)->data[3][(i)]}}

void print_vec4f(const vec4f* a) {
    printf("%.6f %.6f %.6f %.6f\n", a->x, a->y, a->z, a->w);
}

void print_mat4f(const mat4f* A) {
    printf(
        "[%.6f %.6f %.6f %.6f]\n" \
        "[%.6f %.6f %.6f %.6f]\n" \
        "[%.6f %.6f %.6f %.6f]\n" \
        "[%.6f %.6f %.6f %.6f]\n",
        A->data[0], A->data[4], A->data[8],  A->data[12],
        A->data[1], A->data[5], A->data[9],  A->data[13],
        A->data[2], A->data[6], A->data[10], A->data[14],
        A->data[3], A->data[7], A->data[11], A->data[15]
    );
}

float reduce_vec4f(const vec4f* a) {
    return a->x + a->y + a->z + a->w;
}

vec4f vecmul_vec4f(const vec4f* a, const vec4f* b) {
    return (vec4f) {
        .data = {a->x * b->x, a->y * b->y, a->z * b->z, a->w * b->w}
    };
}

float dot_vec4f(const vec4f* a, const vec4f* b) {
    vec4f mul = vecmul_vec4f(a,b);
    return reduce_vec4f(&mul);
}

vec4f matmul_vec4f(const mat4f* A, const vec4f* b) {
    return (vec4f) {
        .x = dot_vec4f(&M4F_ROW(A, 0), b),
        .y = dot_vec4f(&M4F_ROW(A, 1), b),
        .z = dot_vec4f(&M4F_ROW(A, 2), b),
        .w = dot_vec4f(&M4F_ROW(A, 3), b),
    };
}

mat4f matmul_mat4f(const mat4f* A, const mat4f* B) {
    return (mat4f) {
        .cols = {
            {
                dot_vec4f(&M4F_ROW(A, 0), &B->cols[0]),
                dot_vec4f(&M4F_ROW(A, 1), &B->cols[0]),
                dot_vec4f(&M4F_ROW(A, 2), &B->cols[0]),
                dot_vec4f(&M4F_ROW(A, 3), &B->cols[0]),
            },
            {
                dot_vec4f(&M4F_ROW(A, 0), &B->cols[1]),
                dot_vec4f(&M4F_ROW(A, 1), &B->cols[1]),
                dot_vec4f(&M4F_ROW(A, 2), &B->cols[1]),
                dot_vec4f(&M4F_ROW(A, 3), &B->cols[1]),
            },
            {
                dot_vec4f(&M4F_ROW(A, 0), &B->cols[2]),
                dot_vec4f(&M4F_ROW(A, 1), &B->cols[2]),
                dot_vec4f(&M4F_ROW(A, 2), &B->cols[2]),
                dot_vec4f(&M4F_ROW(A, 3), &B->cols[2]),
            },
            {
                dot_vec4f(&M4F_ROW(A, 0), &B->cols[3]),
                dot_vec4f(&M4F_ROW(A, 1), &B->cols[3]),
                dot_vec4f(&M4F_ROW(A, 2), &B->cols[3]),
                dot_vec4f(&M4F_ROW(A, 3), &B->cols[3]),
            }
        }
    };
}

int main() {
    print_vec4f(&(vec4f){.x = 1.0f, .y = 2.0f, .z = 3.0f, .w = 4.0f});
    print_vec4f(&(vec4f){.data = {1.0f, 2.0f, 3.0f, 4.0f}});
    print_vec4f(&(vec4f){{1.0f, 2.0f, 3.0f, 4.0f}});

    printf("\n");
    print_mat4f(&ID4F);
    vec4f a = matmul_vec4f(&ID4F, &(vec4f){{1.0f, 2.0f, 3.0f, 4.0f}});
    print_vec4f(&a);

    printf("\n");
    print_mat4f(&(mat4f){.cols = {a, a, a, a}});

    printf("\n");
    mat4f A = matmul_mat4f(&(mat4f){.cols = {a, a, a, a}}, &ID4F);
    print_mat4f(&A);

/*    mat4 A;
    vec4 v;
    vec4 b = mvmul4f(A, v);
    mat4 B = mmul4f(A,A);
    vec c = vmul4f()
    vec4 u = dot4f(v, b);
    vec4 t = red4f(v);
    vec4 v = vadd4f()
    madd4f
*/


    return 0;
}
