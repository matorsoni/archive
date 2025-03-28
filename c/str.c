#include <stdio.h>

#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

struct str_t {
    char*  dat;
    size_t len;
};
typedef struct str_t str_t;

struct strbuf_t {
    char*  dat;
    size_t len;
    size_t cap;
};
typedef struct strbuf_t strbuf_t;

// charray must be a stack allocated string
#define static_str(charray) \
    (str_t){.dat = charray, .len = sizeof(charray) - 1}

void str_replace(str_t s, char key, char new) {
    for (size_t i = 0; i < s.len; i++) {
        if (s.dat[i] == key) s.dat[i] = new;
    }
}

str_t sbf_as_str(strbuf_t sb) {
    return (str_t) {.dat = sb.dat, .len = sb.len};
}

void sbf_reserve(strbuf_t* sb, size_t new_cap);

strbuf_t sbf_new(const char* str, size_t length) {
    size_t cap = length + 1;
    size_t len = (str == NULL) ? 0 : length;
    char* s = malloc(cap);
    if (len > 0) memcpy(s, str, len);
    s[len] = '\0';
    return (strbuf_t) {.dat = s, .cap = cap, .len = len};
}

bool sbf_valid(const strbuf_t sb) {
    bool valid_state[] = {
        sb.dat == NULL && (sb.len == sb.cap == 0),
        sb.dat != NULL && sb.dat[sb.len] == '\0' && sb.cap > sb.len
    };
    return valid_state[0] || valid_state[1];
}


int main(void) {
    char cu[] = "hello";
    str_t s = static_str(cu);
    printf("String size: %zu\n", s.len);
    for (int i = 0; i < s.len; i++) printf("%c\n", s.dat[i]);

    strbuf_t sb = sbf_new(s.dat, s.len);
    printf("%s\n", sb.dat);

    str_replace(sbf_as_str(sb), 'l', 'X');
    printf("%s\n", sb.dat);

    return 0;
}
