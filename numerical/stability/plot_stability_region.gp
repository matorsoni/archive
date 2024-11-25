set terminal pngcairo enhanced size 800,800
set output "eigenvalues_and_stability.png"

set xlabel "Real Part"
set ylabel "Imaginary Part"
set grid
set key left top
set size square

set xrange [-2:0]
set yrange [-1:1]

# Plot stability region and eigenvalues
plot "stability_region.dat" using 1:2 with lines title "" lw 2 lc rgb "blue", \
     "eigenvalues.dat" using 1:2 with points title "" pt 7 lc rgb "red"
