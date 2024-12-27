set term gif animate delay 20 size 800, 800
set output "point.gif"
unset key

set xlabel "X"
set ylabel "Y"
set title "Planar Three-Body Problem"

r = 1
set xrange[-r:r]
set yrange[-r:r]

set style line 1 lc rgb "red" lt 2 lw 1 pt 6 ps 1.5
set style line 2 lc rgb "blue" lt 2 lw 1 pt 6 ps 1.5
set style line 3 lc rgb "green" lt 2 lw 1 pt 6 ps 1.5

do for [n=1:400] {
    plot "three_body_euler.dat" using 2:3 every ::::n:n with lp ls 1, \
         "three_body_euler.dat" using 4:5 every ::::n:n with lp ls 2, \
         "three_body_euler.dat" using 6:7 every ::::n:n with lp ls 3
}

