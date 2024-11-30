set terminal pngcairo size 800,600
set output "solution.png"
set xlabel "x"
set ylabel "u(x,t)"
set xrange [0:1]
set yrange [0:3]
set title "Numerical vs Analytical Solution at t=0.214s"
set grid
set style line 1 lc rgb "blue" lw 2 # Analytical solution style (blue line)
set style line 2 lc rgb "red" pt 6 ps 1.5 # Numerical solution style (red circles)

plot "output.dat" using 1:2 with lines linestyle 1 title "Analytical Solution", \
     "output.dat" using 1:3 with points linestyle 2 title "Numerical Solution"
