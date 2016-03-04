# A small shell script to demonstrate how to run
# magnetic.py in parallel using xargs. This is a
# general approach, and should be useful for other
# problems as well.

# magnetic.py takes one number as a command line argument.
# This number gives the starting position of the particle.

# Here, I've chosen to make a list of the starting positions
# I want to simulate. A more general approach might be to
# keep these in a file, or generate them automatically.
# echo just prints the list of positions. The pipe, |, passes
# the list of numbers on to xargs. xargs is used like this:
# xargs -n1 -P4 command
# This tells xargs to take the list of arguments that gets "piped" in,
# and pass one (-n1) to each copy of the program that gets started by
# command, and then to start four (-P4) copies in parallel.
echo '0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.1 1.2' | xargs -n1 -P4 python magnetic.py

# A more elegant way to get the list of starting positions would be
# to generate it by a program. For example, try to un-comment the line
# below. If you want to try more than a few parameters, automatic
# generation like this is very convenient.

# python -c "for i in range(1, 13): print(0.1*i)" | xargs -n1 -P4 python magnetic.py
