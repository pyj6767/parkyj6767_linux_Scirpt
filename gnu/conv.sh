#!/bin/bash
gnuplot -persist -e "set terminal pdfcairo enhanced dashed size 5in,5in ;set output 'ENCUT_test.pdf';
set bmargin 4.0;
set tmargin 1.4;
set key right top;
set border -1 lw 2;
set style line 1 lt 1 lw 5 lc rgb 'red';
set xrange [:];
set yrange [-0.5:];
set xtics 250,50,850 font 'arial,12';
set ytics font 'arial,12';
set ylabel offset -1 font 'arial,12' \"Energy (eV)\";
set xlabel offset 0 font 'arial,12' \"ENCUT (eV)\";
set style fill transparent solid 0.2;
set tics nomirror;
plot 'encut_test_result' u 1:4 w l lc rgb 'black' lw 5 lt 1 title 'dE', 'encut_test_result' u 1:2 w l lc rgb 'web-blue' lw 5 lt 1 title 'EDIFFG';" # Total ENCUT_TEST

evince ENCUT_test.pdf
