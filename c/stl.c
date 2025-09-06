#include <stdio.h>
#include <stdint.h>

struct stl_header {
    char header[80];
    uint32_t tri_count;
};
typedef struct stl_header stl_header;

struct stl_tri {
    float normal[3];
    float vertex_a[3];
    float vertex_b[3];
    float vertex_c[3];
    uint16_t attribute;
};
typedef struct stl_tri stl_tri;

void write_stl(FILE* stream, const stl_tri* model, uint32_t tri_count);

int main(void) {

    stl_tri model[] = {
        {
            .normal   = {0.0f, 1.0f, 0.0f},
            .vertex_a = {0.5f, 0.5f, 0.5f},
            .vertex_b = {0.5f, 0.5f, -0.5f},
            .vertex_c = {-0.5f, 0.5f, -0.5f},
        },
        {
            .normal   = {0.0f, 1.0f, 0.0f},
            .vertex_a = {-0.5f, 0.5f, -0.5f},
            .vertex_b = {-0.5f, 0.5f, 0.5f},
            .vertex_c = {0.5f, 0.5f, 0.5f},
        },
        {
            .normal   = {0.0f, -1.0f, 0.0f},
            .vertex_a = {0.5f, -0.5f, 0.5f},
            .vertex_b = {-0.5f, -0.5f, -0.5f},
            .vertex_c = {0.5f, -0.5f, -0.5f},
        },
        {
            .normal   = {0.0f, -1.0f, 0.0f},
            .vertex_a = {-0.5f, -0.5f, -0.5f},
            .vertex_b = {0.5f, -0.5f, 0.5f},
            .vertex_c = {-0.5f, -0.5f, 0.5f},
        },
    };

    FILE* file = fopen("test.stl", "wb");
    write_stl(file, model, sizeof(model) / sizeof(*model));
    fclose(file);
    return 0;
}


void write_stl(FILE* stream, const stl_tri* model, uint32_t tri_count) {
    static const char header[80] = "STL";
    fwrite(header, sizeof(char), 80, stream);
    fwrite(&tri_count, sizeof(uint32_t), 1, stream);
    for (uint32_t i = 0; i < tri_count; ++i) {
        fwrite(&model[i], sizeof(float), 12, stream);
        fwrite(&model[i].attribute, sizeof(uint16_t), 1, stream);
    }
}
