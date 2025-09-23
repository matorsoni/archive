// Experiment from https://mike.trausch.us/blog/minimal-cxx/

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <concepts>

template<typename T>
class Thing {
public:
    Thing();
    ~Thing();

    T get() const { return generic_data; }
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
    printf("new allocating %zu bytes\n", size);
    return calloc(1, size);
}

void* operator new[](size_t size) {
    printf("new[] allocating %zu bytes\n", size);
    return calloc(1, size);
}

void operator delete(void* ptr, size_t size) {
    printf("delete freeing %zu bytes\n", size);
    free(ptr);
}

void operator delete[](void* ptr) {
    printf("delete[] freeing bytes\n");
    free(ptr);
}

struct str_t {
    char* str;
    size_t len;
    size_t cap;
};


template<typename T>
concept has_plus_assign = requires(T a, T b) { { a+=b } -> std::same_as<T&>; };

template<has_plus_assign T, size_t M, size_t N>
struct matrix {
    T elt[M*N];

    T& operator[] (size_t index) { return elt[index]; }
    const T& operator[] (size_t index) const { return elt[index]; }

    void operator+= (const matrix<T, M, N>& m) {
        for (size_t i = 0; i < M*N; ++i) elt[i] += m[i];
    }
};

int main(int argc, char** argv) {
    auto t1 = new Thing<uint64_t>;
    delete t1;

    auto t2 = new Thing<char*>;
    delete t2;

    auto t3 = new Thing<str_t>;
    delete t3;

    {
        Thing<bool> t4;
    }

    auto* ptr = new int[4];
    delete[] ptr;

    matrix<float, 2, 2> m1{.elt = {0.f, 1.0f, 2.0f, 3.0f}};
    matrix<float, 2, 2> m2 = {};
    m2 += m1;
    m2 += m2;

    // compilation fails for T == int*
    //matrix<int*, 2, 2> m3 = {};
    //matrix<int*, 2, 2> m4 = {};
    //m3 += m4;

    return 0;
}
