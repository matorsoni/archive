set term gif animate delay 30 size 800, 800
set output "point.gif"
do for [n=1:400] {
    plot [-5:5][-5:5] "three_body_euler.dat" using 2:3 every ::::n:n with lp title sprintf("n=%i", n)
}

