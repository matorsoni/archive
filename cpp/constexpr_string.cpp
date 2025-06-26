#include <iostream>
#include <cstdio>
#include <array>
#include <cstddef> // for std::size_t

template<std::size_t N>
using charray = std::array<char, N>;

template<std::size_t N>
constexpr auto make_charray(const char (&str)[N]) {
    charray<N> result{};
    for (std::size_t i = 0; i < N; ++i) {
        result[i] = str[i];
    }
    return result;
}

template<std::size_t N1, std::size_t N2>
constexpr auto concat(const charray<N1>& s1, const charray<N2>& s2) {
    charray<N1 + N2 - 1> result{};
    for (std::size_t i = 0; i < N1 - 1; ++i) {
        result[i] = s1[i];
    }
    for(std::size_t i = 0; i < N2; ++i) {
        result[N1 - 1 + i] = s2[i];
    }
    return result;
}

constexpr auto who = make_charray(R"(0123456789)");
static_assert(sizeof(who) == 11);

constexpr auto s1 = make_charray(R"(Hello, )");
constexpr auto s2 = make_charray(R"(constexpr strings!)");

int main() {
    std::cout << concat(s1,s2).data() << "\n";
    printf("%s\n", who.data());
}
