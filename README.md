There are three files that need to be run in order:
1. abm_run.py creates a toy wave-like spread, saves it to file and runs the ABM which infers parameters. Crucially, it only saves the parameters and seeds of the individual runs to save memory.
2. abm_processing.R reads in the posterior simulations of the previous file, generates plots and selects the 'accepted' runs which it writes to file.
3. abm_repro.py reads in the accepted runs from the previous file along with their seeds and reproduces them. This time, it saves the information for each agent and time step, generating matrices that can be plotted to view the spread of the simulated innovations.
