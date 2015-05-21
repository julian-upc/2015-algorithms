SHELL = /bin/sh

.SUFFIXES:
.SUFFIXES: .cc .o

BOOSTDIR = /home/julian/software/boost_1_57_0
INCLUDEDIR = -I. -I$(BOOSTDIR)
LIBDIR = -L$(BOOSTDIR)/lib
LIBS = -lboost_unit_test_framework
CFLAGS = -Wall -Wextra -Wpedantic -std=c++1y -O3 -g
CC = g++

test_dancing_links: test_dancing_links.o
	$(CC) $(LIBDIR) $(CFLAGS) $< $(LIBS) -o $@

test_dancing_links.o: test_dancing_links.cc test_pentominos.cc test_incidence_matrix.cc pentominos.h boost_cout_wrappers.h incidence_matrix.h dancing_links.h test_algorithm_x.cc
	$(CC) $(INCLUDEDIR) $(CFLAGS) -c $< -o $@

