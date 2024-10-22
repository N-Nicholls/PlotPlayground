# PlotPlayground
This started as a project in pygame to model phasor signals. Currently it operates as a cool little wallpaper program that will generate 
phasors stacked on top of each other that will draw themselves before adding more phasors and then restarting and repeating the cycle. 
The code is currently pretty barebones and im sure very inefficient but it has the "bones" of a dynamic pannable and scaleable graph, though
the grid lines don't render correctly and the phasors don't scale properly. Also the lines stay in place on the screen they don't move properly when 
you scale or pan the graph.

The basic controls are 
1: Spawns a new Phasor. Resets all the drawn lines and starts drawing a signal of the topmost phasor
2: Deletes the top phasor. If there is a phasor left it will begin drawing its signal.
3: Resets the line being drawn. Useful if you pan the screen and want to reset the signal. Also of note is that
currently the phasors are hardcoded to stop drawing their line after they generate around 680 points, which for the given 
maximum signal period is around 680 points. This ensures the program doesn't draw unecessary points. I tried making a system to figure out the current
period and then to only draw the necessary points for a whole period, but it turned out to be slightly buggy.
4: Draws the signal of all current phasors. Currently this looks kinda messy but it can be pretty cool. This will also disable if any other key is pressed.
5: Wallpaper Mode. Will cycle between 1 and 8 phasors, when it reached 9 phasors it resets back to 1. It will draw around 2 revolutions of the signal before adding a new phasor.
Minus the first phasor which will always draw a simple circle, so it only renders that one once.

I hope to expand this program in the future to include desmos like functionality with a proper dynamic graph and the ability to plot all kinds of cool data.
