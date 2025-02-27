#ifndef TINYMATH_H
#define TINYMATH_H

typedef union {
    struct { float x, y, z, w; };
    float el[4];
} vec4f;

typedef union {
    vec4f col[4];
    float el[16];
} mat4f;

static inline vec4f addvec4f(vec4f u, vec4f v);
static inline vec4f subvec4f(vec4f u, vec4f v);
static inline vec4f mulvec4f(vec4f u, vec4f v);
static inline vec4f divvec4f(vec4f u, vec4f v);
static inline vec4f smulvec4f(vec4f u, float s);
static inline vec4f sdivvec4f(vec4f u, float s);
static inline float dot4f(vec4f u, vec4f v);
static inline float len4f(vec4f u);
static inline float dist4f(vec4f u, vec4f v);
static inline vec4f norm4f(vec4f u);

static inline mat4f addmat4f(mat4f A, mat4f B);
static inline mat4f submat4f(mat4f A, mat4f B);
static inline mat4f mulmat4f(mat4f A, mat4f B);
static inline vec4f matvec4f(mat4f A, vec4f u);
static inline mat4f smulmat4f(mat4f A, float s);
static inline mat4f sdivmat4f(mat4f A, float s);
static inline mat4f trans4f(mat4f A);


#endif // TINYMATH_H
