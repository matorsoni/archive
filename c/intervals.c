#include <stdio.h>
#include <stdbool.h>

struct interval {
    int x, y;
};
typedef struct interval interval;

#define invalid (interval){.x = 0, .y = -1}

bool valid(interval a) {
    return a.x <= a.y;
}

bool inside(int x, interval a) {
    return x >= a.x && x <= a.y;
}

bool overlap(interval a, interval b) {
    return inside(a.x, b) ||
           inside(a.y, b) ||
           inside(b.x, a) ||
           inside(b.y, a);
}

interval merge(interval a, interval b) {
    //assert(overlap(a,b));
    int pos[4] = {a.x, a.y, b.x, b.y};
    int xmax = pos[0], xmin = pos[0];
    for (int i = 0; i < 4; i++) {
        if (xmax < pos[i]) xmax = pos[i];
        if (xmin > pos[i]) xmin = pos[i];
    }
    return (interval) {.x = xmin, .y = xmax};
}

void insert(interval* intervs, int n, interval a) {
    int first_invalid = -1;
    for (int i=0; i<n; i++) {
        interval intv = intervs[i];
        first_invalid = (!valid(intv) && first_invalid < 0) ? i : first_invalid;
        if (valid(intv) && overlap(intv, a)) {
            intervs[i] = invalid;
            insert(intervs, n, merge(a, intv));
            return;
        }
    }
    if (first_invalid < 0) puts("OK SOMETHING WENT WRONG...");
    intervs[first_invalid] = a;
}


void print_intervals(interval* intervs, int n) {
    char s[] = "....................................";
    for (int i=0; i<n; i++) {
        interval in = intervs[i];
        printf("%d %d\n", in.x, in.y);

        if (valid(in)) {
            for (int x=in.x; x<=in.y; x++) {
                s[x] = '#';
            }
        }
    }
    printf("%s\n\n", s);
}

int main(void) {
    interval intervals[] = {
        {.x = 1, .y = 3},
        {.x = 5, .y = 6},
        {.x = 8, .y = 12},
        {.x = 19, .y = 25},
        invalid,
        invalid
    };
    int n = sizeof(intervals) / sizeof(*intervals);
    print_intervals(intervals, n);

    interval a = {.x = 27, .y = 30};
    insert(intervals, n, a);
    print_intervals(intervals, n);

    insert(intervals, n, (interval){.x = 11, .y = 20});
    print_intervals(intervals, n);

    return 0;
}
