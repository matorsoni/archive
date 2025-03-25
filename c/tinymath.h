#ifndef TINYMATH_H
#define TINYMATH_H

#include <math.h>

/* * * * * * * * * * * * * * * * * * * * *
 *                 vec2f                 *
 * * * * * * * * * * * * * * * * * * * * */
union vec2f {
    struct { float x, y; };
    float elt[2];
};
typedef union vec2f vec2f;

static inline vec2f vadd2f(vec2f u, vec2f v) {
    return (vec2f) {u.x + v.x, u.y + v.y};
}

static inline vec2f vsub2f(vec2f u, vec2f v) {
    return (vec2f) {u.x - v.x, u.y - v.y};
}

static inline vec2f vmul2f(vec2f u, vec2f v) {
    return (vec2f) {u.x * v.x, u.y * v.y};
}

static inline vec2f vdiv2f(vec2f u, vec2f v) {
    return (vec2f) {u.x / v.x, u.y / v.y};
}

static inline vec2f vsmul2f(vec2f u, float s) {
    return (vec2f) {u.x * s, u.y * s};
}

static inline vec2f vsdiv2f(vec2f u, float s) {
    return (vec2f) {u.x / s, u.y / s};
}

static inline float redu2f(vec2f u) {
    return u.x + u.y;
}

static inline float dot2f(vec2f u, vec2f v) {
    return redu2f(vmul2f(u, v));
}

static inline float len2f(vec2f u) {
    return sqrtf(redu2f(vmul2f(u, u)));
}

static inline vec2f unit2f(vec2f u) {
    return vsdiv2f(u, len2f(u));
}

static inline float dist2f(vec2f u, vec2f v) {
    return len2f(vsub2f(u, v));
}

/* * * * * * * * * * * * * * * * * * * * *
 *                 mat2f                 *
 * * * * * * * * * * * * * * * * * * * * */
union mat2f {
    vec2f col[2];
    float elt[4];
};
typedef union mat2f mat2f;

static inline mat2f madd2f(mat2f A, mat2f B) {
    return (mat2f) {
        vadd2f(A.col[0], B.col[0]),
        vadd2f(A.col[1], B.col[1])
    };
}

static inline mat2f msub2f(mat2f A, mat2f B) {
    return (mat2f) {
        vsub2f(A.col[0], B.col[0]),
        vsub2f(A.col[1], B.col[1])
    };
}

static inline mat2f mhad2f(mat2f A, mat2f B) {
    return (mat2f) {
        vmul2f(A.col[0], B.col[0]),
        vmul2f(A.col[1], B.col[1])
    };
}

static inline vec2f mvmul2f(mat2f A, vec2f u) {
    vec2f r =     vsmul2f(A.col[0], u.elt[0]);
    r = vadd2f(r, vsmul2f(A.col[1], u.elt[1]));
    return r;
}

static inline mat2f matmul2f(mat2f A, mat2f B) {
    return (mat2f) {
        mvmul2f(A, B.col[0]),
        mvmul2f(A, B.col[1])
    };
}

static inline mat2f msmul2f(mat2f A, float s) {
    return (mat2f) {
        vsmul2f(A.col[0], s),
        vsmul2f(A.col[1], s)
    };
}

static inline mat2f msdiv2f(mat2f A, float s) {
    return (mat2f) {
        vsdiv2f(A.col[0], s),
        vsdiv2f(A.col[1], s)
    };
}

static inline mat2f transp2f(mat2f A) {
    vec2f row0 = {A.elt[0], A.elt[2]};
    vec2f row1 = {A.elt[1], A.elt[3]};
    return (mat2f) {row0, row1};
}

static inline mat2f id2f(void) {
    mat2f R = {0};
    R.elt[0] = R.elt[3] = 1.0f;
    return R;
}


/* * * * * * * * * * * * * * * * * * * * *
 *                 vec3f                 *
 * * * * * * * * * * * * * * * * * * * * */
union vec3f {
    struct { float x, y, z; };
    float elt[3];
};
typedef union vec3f vec3f;

static inline vec2f xy(vec3f u) {
    return (vec2f) {u.x, u.y};
}

static inline vec3f vadd3f(vec3f u, vec3f v) {
    return (vec3f) {u.x + v.x, u.y + v.y, u.z + v.z};
}

static inline vec3f vsub3f(vec3f u, vec3f v) {
    return (vec3f) {u.x - v.x, u.y - v.y, u.z - v.z};
}

static inline vec3f vmul3f(vec3f u, vec3f v) {
    return (vec3f) {u.x * v.x, u.y * v.y, u.z * v.z};
}

static inline vec3f vdiv3f(vec3f u, vec3f v) {
    return (vec3f) {u.x / v.x, u.y / v.y, u.z / v.z};
}

static inline vec3f vsmul3f(vec3f u, float s) {
    return (vec3f) {u.x * s, u.y * s, u.z * s};
}

static inline vec3f vsdiv3f(vec3f u, float s) {
    return (vec3f) {u.x / s, u.y / s, u.z / s};
}

static inline float redu3f(vec3f u) {
    return u.x + u.y + u.z;
}

static inline float dot3f(vec3f u, vec3f v) {
    return redu3f(vmul3f(u, v));
}

static inline float len3f(vec3f u) {
    return sqrtf(redu3f(vmul3f(u, u)));
}

static inline vec3f unit3f(vec3f u) {
    return vsdiv3f(u, len3f(u));
}

static inline float dist3f(vec3f u, vec3f v) {
    return len3f(vsub3f(u, v));
}

/* * * * * * * * * * * * * * * * * * * * *
 *                 mat3f                 *
 * * * * * * * * * * * * * * * * * * * * */
union mat3f {
    vec3f col[3];
    float elt[9];
};
typedef union mat3f mat3f;

static inline mat3f madd3f(mat3f A, mat3f B) {
    return (mat3f) {
        vadd3f(A.col[0], B.col[0]),
        vadd3f(A.col[1], B.col[1]),
        vadd3f(A.col[2], B.col[2])
    };
}

static inline mat3f msub3f(mat3f A, mat3f B) {
    return (mat3f) {
        vsub3f(A.col[0], B.col[0]),
        vsub3f(A.col[1], B.col[1]),
        vsub3f(A.col[2], B.col[2])
    };
}

static inline mat3f mhad3f(mat3f A, mat3f B) {
    return (mat3f) {
        vmul3f(A.col[0], B.col[0]),
        vmul3f(A.col[1], B.col[1]),
        vmul3f(A.col[2], B.col[2])
    };
}

static inline vec3f mvmul3f(mat3f A, vec3f u) {
    vec3f r =     vsmul3f(A.col[0], u.elt[0]);
    r = vadd3f(r, vsmul3f(A.col[1], u.elt[1]));
    r = vadd3f(r, vsmul3f(A.col[2], u.elt[2]));
    return r;
}

static inline mat3f matmul3f(mat3f A, mat3f B) {
    return (mat3f) {
        mvmul3f(A, B.col[0]),
        mvmul3f(A, B.col[1]),
        mvmul3f(A, B.col[2])
    };
}

static inline mat3f msmul3f(mat3f A, float s) {
    return (mat3f) {
        vsmul3f(A.col[0], s),
        vsmul3f(A.col[1], s),
        vsmul3f(A.col[2], s)
    };
}

static inline mat3f msdiv3f(mat3f A, float s) {
    return (mat3f) {
        vsdiv3f(A.col[0], s),
        vsdiv3f(A.col[1], s),
        vsdiv3f(A.col[2], s)
    };
}

static inline mat3f transp3f(mat3f A) {
    vec3f row0 = {A.elt[0], A.elt[3], A.elt[6]};
    vec3f row1 = {A.elt[1], A.elt[4], A.elt[7]};
    vec3f row2 = {A.elt[2], A.elt[5], A.elt[8]};
    return (mat3f) {row0, row1, row2};
}

static inline mat3f id3f(void) {
    mat3f R = {0};
    R.elt[0] = R.elt[4] = R.elt[8] = 1.0f;
    return R;
}



/* * * * * * * * * * * * * * * * * * * * *
 *                 vec4f                 *
 * * * * * * * * * * * * * * * * * * * * */
union vec4f {
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


/* * * * * * * * * * * * * * * * * * * * *
 *                 mat4f                 *
 * * * * * * * * * * * * * * * * * * * * */
union mat4f {
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
