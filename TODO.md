TODO
====

* Widgets are no longer registered with a string argument to the decorator but depend on `_model_*` and `_view_*` http://ipywidgets.readthedocs.io/en/latest/migration_guides.html
* Create Brian object for each GUI object
* Build the GUI fields from the Brian objects automatically
* Link the Brian object values to the corresponding GUI object values for automatic updates
* Add a 'More' button to automatically generate all the optional fields in addition to statically listed and nicely formatted main ones
* Invalidate each object once parameters are changed then check all at runtime and only regenerate where necessary

* Add synapse models from brian2/examples/synapses/
* brain2tools plotting button
* Add a help button on each tab / object type
* Revise Monitors inputs to handle objects derived from Group and SpikeSource: Group -> StateMonitor; SpikeSource -> SpikeMonitor
* BrianObjectException to highlight offending field
* Use base.py:121 `BrianObject()._dependencies` to invalidate interdependencies
* Add setup.py
* Run sphinx on installation (see sphinxext) to pull out docstrings
    - http://www.sphinx-doc.org/en/stable/tutorial.html
    - sphinx-build -b html sourcedir builddir
