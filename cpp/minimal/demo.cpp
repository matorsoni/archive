// Experiment from https://mike.trausch.us/blog/minimal-cxx/

#include <cstdint>
#include <cstdio>
#include <cstdlib>

template<typename T>
class Thing {
public:
    Thing();
    ~Thing();
private:
    uint32_t data;
    T generic_data;
};


template<typename T>
Thing<T>::Thing() : data(0), generic_data(T()) {
    puts("Thing created");
}

template<typename T>
Thing<T>::~Thing() {
    puts("Thing destroyed");
}

void* operator new(size_t size) {
    printf("Allocating %zu bytes\n", size);
    return calloc(1, size);
}

void operator delete(void* ptr, size_t size) {
    printf("Freeing memory\n");
    free(ptr);
}

struct str_t
{
    char* str;
    size_t len;
    size_t cap;
};

int main(int argc, char** argv) {
    auto t1 = new Thing<uint64_t>;
    delete t1;

    auto t2 = new Thing<char*>;
    delete t2;

    auto t3 = new Thing<str_t>;
    delete t3;

    return 0;
}
