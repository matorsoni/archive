set terminal pngcairo size 800,600
set output "solution.png"
set xlabel "x"
set ylabel "u(x,t)"
set xrange [0:1]
set yrange [0:1]
set title "Numerical comparison: Lax-Friedrichs vs Regular Upwind at t=0.2s"
set grid

# Styles: Blue line and red circles
set style line 1 lc rgb "blue" lw 2
set style line 2 lc rgb "red" pt 6 ps 1.5

plot "output.dat" using 1:2 with lines linestyle 1 title "Lax-Friedrichs", \
     "output.dat" using 1:3 with points linestyle 2 title "Regular Upwind"
