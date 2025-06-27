#include <tuple>
#include <array>
#include <cstddef>
#include <iostream>
#include <Eigen/Dense>

using vec2f = Eigen::Vector2f;
using mat4f = Eigen::Matrix4f;

template <std::size_t N, typename... Types>
using array_struct = std::tuple<std::array<Types, N>...>;

template <std::size_t N, typename... Types>
struct StructArraySerializer {
    array_struct<N, Types...> data;
    size_t length;

    template<std::size_t k>
    auto& get() {
        static_assert(k < sizeof...(Types));
        return std::get<k>(data);
    }
};

int main(void)
{

    array_struct<4, int> b{};
    array_struct<4, int, double> c{};
    std::cout << std::get<0>(b)[0] << " " << std::get<0>(b)[1] << std::endl;
    std::cout << std::get<1>(c)[0] << std::endl;

    StructArraySerializer<10, int, double> s{};
    std::cout << std::get<1>(s.data)[0] << std::endl;
    std::cout << s.get<1>()[0] << std::endl;
    s.get<1>()[0] = 1.10;
    std::cout << s.get<1>()[0] << std::endl;
    std::cout << sizeof(s) << std::endl;

    // matrix power method test
    Eigen::Matrix<double, 3, 3> A{{1,2,0}, {2,1,0}, {0, 0, -1}};
    std::cout << A << std::endl;
    std::cout << "\n";
    Eigen::Vector<double, 3> v[12];
    //v[0] = {0.01,0,1};
    v[0] = {1,1,0};
    std::cout << v[0] << std::endl;
    std::cout << "\n";
    for (int i = 1; i < 12; ++i) {
        v[i] = A * v[i-1];
        v[i].normalize();
        std::cout << v[i] << std::endl;
        std::cout << "\n";
    }
}

