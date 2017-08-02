TODO
====

* Create Brian object for each GUI object
* Build the GUI fields from the Brian objects automatically
* Link the Brian object values to the corresponding GUI object values for automatic updates
* Add a 'More' button to automatically generate all the optional fields in addition to statically listed and nicely formatted main ones
* Invalidate each object once parameters are changed then check all at runtime and only regenerate where necessary

* sphnxext to pull out docstrings
* BrianObjectException to highlight offending field
* Use base.py:121 'BrianObject()._dependencies' to invalidate interdependencies
