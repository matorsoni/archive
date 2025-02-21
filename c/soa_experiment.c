#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    float X, Y, Z;
} vec3f;

double cpu_time_seconds(clock_t start, clock_t end) {
    return ((double) (end - start)) / CLOCKS_PER_SEC;
}

double cpu_time_milliseconds(clock_t start, clock_t end) {
    return ((double) (end - start)) / (CLOCKS_PER_SEC / 1000);
}

struct entity
{
    vec3f position;
    vec3f velocity;
    int hp;
    char padding[16]; // Experiment performance impact by varying padding
};

struct entities
{
    vec3f* positions;
    vec3f* velocities;
    int* hps;
};

void update_position(vec3f* pos, const vec3f* vel) {
    pos->X = pos->X + vel->X;
    pos->Y = pos->Y + vel->Y;
    pos->Z = pos->Z + vel->Z;
}

void update_hp(int* hp) {
    *hp += 1;
}

int main(void)
{
    const int N = 100000000;
    clock_t tic, toc;

    tic = clock();
    struct entity* AoS = calloc(N, sizeof(struct entity));
    if (!AoS) {
        printf("AoS alloc failed\n");
        return EXIT_FAILURE;
    }
    toc = clock();
    printf("AoS : Allocation took %.6f milliseconds\n", cpu_time_milliseconds(tic, toc));

    tic = clock();
    struct entities SoA = {
        .positions = calloc(N, sizeof(vec3f)),
        .velocities = calloc(N, sizeof(vec3f)),
        .hps = calloc(N, sizeof(int)),
    };
    if (!SoA.positions || !SoA.velocities || !SoA.hps) {
        printf("SoA alloc failed\n");
        return EXIT_FAILURE;
    }
    toc = clock();
    printf("SoA : Allocation took %.6f milliseconds\n\n", cpu_time_milliseconds(tic, toc));

    tic = clock();
    for (int i = 0; i < N; ++i) {
        struct entity* ent = &AoS[i];
        update_position(&ent->position, &ent->velocity);
    }
    toc = clock();
    printf("AoS : Position update took %.6f milliseconds\n", cpu_time_milliseconds(tic, toc));

    tic = clock();
    for (int i = 0; i < N; ++i) {
        struct entity* ent = &AoS[i];
        update_hp(&ent->hp);
    }
    toc = clock();
    printf("AoS : HP Update took: %.6f milliseconds\n", cpu_time_milliseconds(tic, toc));

    tic = clock();
    for (int i = 0; i < N; ++i) {
        vec3f* pos = &SoA.positions[i];
        vec3f* vel = &SoA.velocities[i];
        update_position(pos, vel);
    }
    toc = clock();
    printf("SoA : Position update took %.6f milliseconds\n", cpu_time_milliseconds(tic, toc));

    tic = clock();
    for (int i = 0; i < N; ++i) {
        int* h = &SoA.hps[i];
        update_hp(h);
    }
    toc = clock();
    printf("SoA : HP Update took %.6f milliseconds\n", cpu_time_milliseconds(tic, toc));
}
