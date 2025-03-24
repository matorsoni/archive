#ifndef TINYMATH_H
#define TINYMATH_H

#include <math.h>

/* * * * * * * * *
 *     vec3f     *
 * * * * * * * * */
union vec3f{
    struct { float x, y, z; };
    float elt[3];
};
typedef union vec3f vec3f;


/* * * * * * * * *
 *     vec4f     *
 * * * * * * * * */
union vec4f{
    struct { float x, y, z, w; };
    float elt[4];
};
typedef union vec4f vec4f;

static inline vec3f xyz(vec4f u) {
    return (vec3f) {u.x, u.y, u.z};
}

static inline vec4f vadd4f(vec4f u, vec4f v) {
    return (vec4f) {u.x + v.x, u.y + v.y, u.z + v.z, u.w + v.w};
}

static inline vec4f vsub4f(vec4f u, vec4f v) {
    return (vec4f) {u.x - v.x, u.y - v.y, u.z - v.z, u.w - v.w};
}

static inline vec4f vmul4f(vec4f u, vec4f v) {
    return (vec4f) {u.x * v.x, u.y * v.y, u.z * v.z, u.w * v.w};
}

static inline vec4f vdiv4f(vec4f u, vec4f v) {
    return (vec4f) {u.x / v.x, u.y / v.y, u.z / v.z, u.w / v.w};
}

static inline vec4f vsmul4f(vec4f u, float s) {
    return (vec4f) {u.x * s, u.y * s, u.z * s, u.w * s};
}

static inline vec4f vsdiv4f(vec4f u, float s) {
    return (vec4f) {u.x / s, u.y / s, u.z / s, u.w / s};
}

static inline float redu4f(vec4f u) {
    return u.x + u.y + u.z + u.w;
}

static inline float dot4f(vec4f u, vec4f v) {
    return redu4f(vmul4f(u, v));
}

static inline float len4f(vec4f u) {
    return sqrtf(redu4f(vmul4f(u, u)));
}

static inline vec4f unit4f(vec4f u) {
    return vsdiv4f(u, len4f(u));
}

static inline float dist4f(vec4f u, vec4f v) {
    return len4f(vsub4f(u, v));
}

/* * * * * * * * *
 *     mat4f     *
 * * * * * * * * */
union mat4f{
    vec4f col[4];
    float elt[16];
};
typedef union mat4f mat4f;

static inline mat4f madd4f(mat4f A, mat4f B) {
    return (mat4f) {
        vadd4f(A.col[0], B.col[0]),
        vadd4f(A.col[1], B.col[1]),
        vadd4f(A.col[2], B.col[2]),
        vadd4f(A.col[3], B.col[3])
    };
}

static inline mat4f msub4f(mat4f A, mat4f B) {
    return (mat4f) {
        vsub4f(A.col[0], B.col[0]),
        vsub4f(A.col[1], B.col[1]),
        vsub4f(A.col[2], B.col[2]),
        vsub4f(A.col[3], B.col[3])
    };
}

static inline mat4f mhad4f(mat4f A, mat4f B) {
    return (mat4f) {
        vmul4f(A.col[0], B.col[0]),
        vmul4f(A.col[1], B.col[1]),
        vmul4f(A.col[2], B.col[2]),
        vmul4f(A.col[3], B.col[3])
    };
}

static inline vec4f mvmul4f(mat4f A, vec4f u) {
    vec4f r =     vsmul4f(A.col[0], u.elt[0]);
    r = vadd4f(r, vsmul4f(A.col[1], u.elt[1]));
    r = vadd4f(r, vsmul4f(A.col[2], u.elt[2]));
    r = vadd4f(r, vsmul4f(A.col[3], u.elt[3]));
    return r;
}

static inline mat4f matmul4f(mat4f A, mat4f B) {
    return (mat4f) {
        mvmul4f(A, B.col[0]),
        mvmul4f(A, B.col[1]),
        mvmul4f(A, B.col[2]),
        mvmul4f(A, B.col[3]),
    };
}

static inline mat4f msmul4f(mat4f A, float s) {
    return (mat4f) {
        vsmul4f(A.col[0], s),
        vsmul4f(A.col[1], s),
        vsmul4f(A.col[2], s),
        vsmul4f(A.col[3], s)
    };
}

static inline mat4f msdiv4f(mat4f A, float s) {
    return (mat4f) {
        vsdiv4f(A.col[0], s),
        vsdiv4f(A.col[1], s),
        vsdiv4f(A.col[2], s),
        vsdiv4f(A.col[3], s)
    };
}

static inline mat4f transp4f(mat4f A) {
    vec4f row0 = {A.elt[0], A.elt[4], A.elt[8],  A.elt[12]};
    vec4f row1 = {A.elt[1], A.elt[5], A.elt[9],  A.elt[13]};
    vec4f row2 = {A.elt[2], A.elt[6], A.elt[10], A.elt[14]};
    vec4f row3 = {A.elt[3], A.elt[7], A.elt[11], A.elt[15]};
    return (mat4f) {row0, row1, row2, row3};
}

static inline mat4f id4f(void) {
    mat4f R = {0};
    R.elt[0] = R.elt[5] = R.elt[10] = R.elt[15] = 1.0f;
    return R;
}


#endif // TINYMATH_H
