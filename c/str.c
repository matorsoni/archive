#include <stdio.h>

#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

struct str_t {
    char*  str;
    size_t len;
};
typedef struct str_t str_t;

// charray must be a stack allocated string
#define static_str(charray) \
    (str_t){.str = charray, .len = sizeof(charray) - 1}

void str_replace(str_t s, char key, char new) {
    for (size_t i = 0; i < s.len; i++) {
        if (s.str[i] == key) s.str[i] = new;
    }
}

struct strbuf_t {
    char*  str;
    size_t len;
    size_t cap;
};
typedef struct strbuf_t strbuf_t;

str_t as_str(strbuf_t sb) {
    return (str_t) {.str = sb.str, .len = sb.len};
}

void strbuf_reserve(strbuf_t* sb, size_t new_cap);

strbuf_t strbuf_new(const char* str, size_t length) {
    size_t cap = length + 1;
    size_t len = (str == NULL) ? 0 : length;
    char* s = malloc(cap);
    if (len > 0) memcpy(s, str, len);
    s[len] = '\0';
    return (strbuf_t) {.str = s, .cap = cap, .len = len};
}

bool valid_strbuf(const strbuf_t sb) {
    bool valid_state_1 = sb.str == NULL && (sb.len == sb.cap == 0);
    bool valid_state_2 = sb.str != NULL && sb.str[sb.len] == '\0' && sb.cap > sb.len;
    return valid_state_1 || valid_state_2;
}


int main(void) {
    char cu[] = "hello";
    str_t s = static_str(cu);
    printf("String size: %zu\n", s.len);
    for (int i=0; i < s.len; i++) printf("%c\n", s.str[i]);

    strbuf_t sb = strbuf_new(s.str, s.len);
    printf("%s\n", sb.str);

    str_replace(as_str(sb), 'l', 'X');
    printf("%s\n", sb.str);

    return 0;
}
