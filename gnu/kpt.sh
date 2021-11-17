#!/bin/bash
gnuplot -persist -e "set terminal pdfcairo enhanced dashed size 7in,7in ;set output 'kpt_test.pdf';
set bmargin 4.0;
set tmargin 1.4;
set key right top;
set border -1 lw 2;
set style line 1 lt 1 lw 5 lc rgb 'red';
set yrange [-0.01:];
set xtics font 'arial, 15';
set ytics font 'arial,15';
set ylabel offset -1 font 'arial,15' \"Energy (eV)\";
set xlabel offset 0 font 'arial,15' \"KPT\";
set style fill transparent solid 0.4;
set tics nomirror;
plot 'kpt_test_result' u 1:4:xtic(1) w l lc rgb 'black' lw 5 lt 1 title 'dE', 'kpt_test_result' u 1:2 w l lc rgb 'web-blue' lw 5 lt 1 title 'EDIFFG';" # Total kpt_TEST


evince kpt_test.pdf

