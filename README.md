Brian 2 Graphical User Interface Readme
=======================================

This is an add on for the Brian 2 Spiking Neural Network Simulator. It provides
an intuitive graphical user interface built on Jupyter notebook widgets.


Dependencies
------------

brian2
brian2tools


Quickstart
----------

1. Pull the git repository:
    `git clone https://github.com/bdevans/brian2gui.git`

2. Build the Docker container:
    `docker build -t brian2gui .`

3. Run the Docker container:
    `docker run -it -v $(pwd):/home/jovyan --rm -p 8888:8888 brian2gui`

4. Copy and paste the notebook server URL into your browser

5. Open the notebook `brian2gui.ipynb`



Ideas
-----

Automatically set the tooltips to the Brian2 documentation for that field.
