# Trajectory of particle in Magnetic field

The python code here simulates a particle moving in a magnetic field, which is specified by the function `B(t, x)`, where `x` is a vector with three components. The program takes one command line argument, which is the starting position in the *y* direction. The complete starting position is `[0, y, 0]`, and the starting velocity is `[1, 0, 0]`. The idea is to use several copies of the program in parallel to see what happens with different starting conditions.

Run the program for example like this:

```
echo "0.1 0.2 0.3 0.4" | xargs -n1 -P4 python magnetic.py
```

and then plot the results (which are stored in one text file per input value) with

```
python plotter.py *.txt
```

What happens here is that `xargs` recieves the four numbers, the passes one (due to `-n1`) to `python magnetic.py`, and then starts four (due to `-P4`) copies in parallel. If you send in more than four numbers, `xargs` will automatically start new processes, to keep four copies running until they are all done.

For increased style and elegance, use an automated way to generate the text input. For example, this command will use python to generate numbers from 0.1 to 1.2, with a spacing of 0.1, and run simulations for all of those, using four parallel copies.

```
python -c "for i in range(1, 13): print(0.1*i)" | xargs -n1 -P4 python magnetic.py
```
