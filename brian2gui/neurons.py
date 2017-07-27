from collections import OrderedDict
import uuid

import ipywidgets as ipw
from ipywidgets.widgets import register
from IPython.display import display
from traitlets import Unicode

#from brian2gui.notebook import Brian2GUI
from brian2gui.models import NEURON_MODELS, LIF
from brian2gui.synapses import SynapseEntry
from brian2gui.utilities import Entry


@register('brian2gui.NeuronGroupInterface')
class NeuronGroupInterface(ipw.Box):
    """Class definition for Brian 2 NeuronGroup graphical interface"""

    _model_name = Unicode('VBoxModel').tag(sync=True)
    _view_name = Unicode('VBoxView').tag(sync=True)

    _NEURON_TYPES = ('NeuronGroup', 'PoissonGroup', 'PoissonInput',
                     'SpikeGeneratorGroup')
    #_SHORT_NEURON_TYPES = ('NG', 'PG', 'PI', 'SGG')

    _methods = ('linear', 'euler', 'heun')

    # Make this an OrderedDict with the values as widths
    _NEURON_HEADER = ('Label', '$N$', 'Equations', 'Threshold', 'Reset',
                      'Refractoriness', 'Integrator')

    _labels = [ipw.Label(value=field) for field in _NEURON_HEADER]

    ENTRY_COUNTER = 0  # class variable shared by all instances
    ENTRIES = []
    ENTRY_BOX = ipw.VBox(children=[])  # NeuronGroupEntry()
    INPUT_ENTRIES = []  # All input objects
    NEURON_ENTRIES = []  # Just for NeuronGroups as these are the only targets

    def __init__(self, gui=None):

        ipw.Box.__init__(self, _dom_classes=['widget-interact'])
        super().__init__()  # super(NeuronGroupInterface, self).__init__()

        self.gui = gui  # Top level container
        self._controls = OrderedDict([('type', ipw.Dropdown(description='Type', options=self._NEURON_TYPES)),
                                      ('template', ipw.Dropdown(description='Template', options=list(NEURON_MODELS.keys()))),
                                      ('new', ipw.Button(description='Add'))])

        #self._neuron_group_entries = [NeuronGroupEntry()]
        # Put all this in a VBox?
        #self._tabs[0].children
        #self._Neurons_tab.children = [ipw.HBox(children=list(self._controls.values())),
        #                              ipw.HBox(children=self._labels),
        #                              ipw.VBox(children=[NeuronGroupEntry()])]

        #self.ENTRIES.append(NeuronGroupEntry())

        #self.ENTRY_BOX = ipw.VBox(children=self.ENTRIES)  # self.children[-1]
        #self.ENTRY_BOX.children = self.ENTRIES

        self.children = [ipw.HBox(children=list(self._controls.values())),
                         #ipw.HBox(children=self._labels),
                         self.ENTRY_BOX]#self.ENTRIES)]  # _neuron_group_entries)]

        #self._controls['template'].observe(self.on_group_select, names='value')
        self._controls['new'].on_click(self.on_new_clicked)

        self.on_new_clicked(None)  # Create a neuron group of the default type (blank)

        # Make accordian for each type of group

        # Set formatting for entry controls
        self._controls['type'].layout = ipw.Layout(width='250px')
        self._controls['template'].layout = ipw.Layout(width='250px')
        self._controls['new'].layout = ipw.Layout(width='50px')
        self._controls['new'].button_style = 'success'
        #self.children[0].children[0].width = '250px'

        # Set formatting for column headers
        # Formatting - may need to set padding to align labels properly

        #self._labels[0].layout = ipw.Layout(width='125px')
        #self._labels[1].layout = ipw.Layout(width='50px')
        #self._labels[2].layout = ipw.Layout(width='350px')
        #self._labels[3].layout = ipw.Layout(width='100px')
        #self._labels[4].layout = ipw.Layout(width='75px')
        #self._labels[5].layout = ipw.Layout(width='75px')
        #self._labels[6].layout = ipw.Layout(width='100px')
        #self._labels[7].layout = ipw.Layout(width='25px')
        #self._labels[8].layout = ipw.Layout(width='25px')

# NeuronGroup(N, model, method=('linear', 'euler', 'heun'), threshold=None,
#             reset=None, refractory=False, events=None, namespace=None,
#             dtype=None, dt=None, clock=None, order=0, name='neurongroup*',
#             codeobj_class=None)

    def on_group_select(self, change):
        if change['new'] is 'NeuronGroup':  # self._controls['type']
            self._controls['template'].disabled = False
        else:
            self._controls['template'].disabled = True

    def on_new_clicked(self, b):
        #self.children[-1].children.append(NeuronGroupEntry())
        #NeuronGroupEntry(self, self._controls['type'].value)

        self.ENTRIES.append(NeuronGroupEntry(self, self._controls['type'].value))
        self.ENTRY_BOX.children = self.ENTRIES  # [nge for nge in self.ENTRIES]
        self.ENTRY_COUNTER += 1
        #print('Now there are {} neuron groups!'.format(self.ENTRY_COUNTER))
        #self.ENTRY_BOX.children = [NGE for NGE in self.ENTRIES]


@register('brian2gui.NeuronGroupEntry')
class NeuronGroupEntry(Entry):  # ipw.Box):  # NeuronGroupInterface
    """Class definition for Brian 2 NeuronGroup graphical entries"""
    # Should this be a single row or the whole set?

    _model_name = Unicode('HBoxModel').tag(sync=True)
    _view_name = Unicode('HBoxView').tag(sync=True)

    _ids = []  # class variable shared by all instances

    # NeuronGroup(N, model, method=('linear', 'euler', 'heun'), threshold=None,
    # reset=None, refractory=False, events=None, namespace=None, dtype=None,
    # dt=None, clock=None, order=0, name='neurongroup*', codeobj_class=None)
    _NeuronGroup_fields = ('N', 'model', 'method', 'threshold', 'reset',
                           'refractory', 'name')  # 'events', 'namespace', 'dtype', 'dt', 'clock', 'order', 'codeobj_class'
    # BinomialFunction(n, p, approximate=True, name='_binomial*')
    _BinomialFunction_fields = ('n', 'p', 'approximate', 'name')
    # http://brian2.readthedocs.io/en/stable/reference/brian2.input.poissongroup.PoissonGroup.html
    _PoissonGroup_fields = ('N', 'rates', 'dt', 'clock', 'when', 'order', 'name')
    # PoissonInput(target, target_var, N, rate, weight, when='synapses', order=0)
    _PoissonInput_fields = ('target', 'target_var', 'N', 'rate', 'weight', 'when', 'order')
    # SpikeGeneratorGroup(N, indices, times, dt=None, clock=None, period=1e100*second, when='thresholds', order=0, sorted=False, name='spikegeneratorgroup*', codeobj_class=None)
    _SpikeGeneratorGroup_fields = ('N', 'indices', 'times', 'dt', 'clock', 'period', 'when', 'order', 'sorted', 'name', 'codeobj_class')
    # TimedArray(values, dt, name=None)
    _TimedArray_fields = ('values', 'dt', 'name')

    _FIELDS = _NeuronGroup_fields  #('name', 'N', 'model', 'threshold', 'reset',
              # 'refractory', 'method')

    #def _change_label(self, change):
    #    self._label.value = change['new']
        #for sg in synapse_groups:
            # This method preserves the order shown (vs. options = neuron_map.keys())
        #    sg['Source'].options = [ng['Label'].value for ng in ENTRIES]
        #    sg['Target'].options = [ng['Label'].value for ng in ENTRIES]

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, name):
        self._name.value = name

    @property
    def N(self):
        return self._N.value  # or self._default_N

    @N.setter
    def N(self, N):
        if type(N) is int:
            self._N.value = N
        else:
            print("N must be a positive integer!")

    @property
    def model(self):
        return self._model.value

    @model.setter
    def model(self, model):
        self._model.value = model

    @property
    def threshold(self):
        return self._threshold.value

    @threshold.setter
    def threshold(self, threshold):
        self._threshold.value = threshold

    @property
    def reset(self):
        return self._reset.value

    @reset.setter
    def reset(self, reset):
        self._reset.value = reset

    @property
    def refractory(self):
        return self._refractory.value

    @refractory.setter
    def refractory(self, refractory):
        self._refractory.value = refractory

    @property
    def method(self):
        return self._method.value

    @method.setter
    def method(self, method):
        self._method.value = method

    #def __init__(self, children = (), **kwargs):
    #    kwargs['children'] = children
    #    super(Box, self).__init__(**kwargs)
    #    self.on_displayed(Box._fire_children_displayed)

    def __init__(self, interface=None, group_type=None, *args, **kwargs):  # N=10, model=LIF, method=None,
                 #threshold='v > 10*mV', reset='v = 0*mV', refractory='5*ms'):

        #ipw.Box.__init__(self, _dom_classes=['widget-interact'])
        super().__init__()
        self.interface = interface
        self.group_type = group_type
        # Create widgets


        self._name = ipw.Text(value="{}{}".format(self.group_type,
                                                  self.interface.ENTRY_COUNTER),
                               tooltip='Label')

        self._name.observe(self._change_name, names='value')

        self._uuid = uuid.uuid4()
        # Move these to superclass
        self._ids.append(self._uuid)

        # Create a dict of model attributes to print out and check

        if self.group_type is 'NeuronGroup':

            self._FIELDS = self._NeuronGroup_fields
            # events=None, namespace=None, dtype=None,
            # dt=None, clock=None, order=0, name='neurongroup*', codeobj_class=None]
            self._N = ipw.BoundedIntText(placeholder='N', min=1, max=1e12, tooltip='Number of neurons')  # value=N
            self._model = ipw.Textarea(placeholder='model', tooltip='Model equations')
            self._method = ipw.Dropdown(options=self.interface._methods, tooltip='Integrator')  # INTEGRATORS
            self._threshold = ipw.Text(placeholder='threshold', tooltip='Threshold')
            self._reset = ipw.Text(placeholder='reset', tooltip='Reset condtion')
            self._refractory = ipw.Text(placeholder='refractory', tooltip='Refractory period')

        elif self.group_type is 'BinomialFunction':
            self._FIELDS = self._BinomialFunction_fields
            # BinomialFunction(n, p, approximate=True, name='_binomial*')
            self._n = ipw.BoundedIntText(placeholder='n', min=1, max=1e12, tooltip='Number of samples')
            self._p = ipw.BoundedFloatText(placeholder='p', min=0, max=1, tooltip='Probability')  # value=N

        elif self.group_type is 'PoissonGroup':
            self._FIELDS = self._PoissonGroup_fields
            # ('N', 'rates', 'dt', 'clock', 'when', 'order', 'name')
            self._N = ipw.BoundedIntText(placeholder='N', min=1, max=1e12, tooltip='Number of neurons')

        elif self.group_type is 'PoissonInput':
            self._FIELDS = self._PoissonInput_fields
            # PoissonInput(target, target_var, N, rate, weight, when='synapses', order=0)

        elif self.group_type is 'SpikeGeneratorGroup':
            self._FIELDS = self._SpikeGeneratorGroup_fields
            # SpikeGeneratorGroup(N, indices, times, dt=None, clock=None, period=1e100*second, when='thresholds', order=0, sorted=False, name='spikegeneratorgroup*', codeobj_class=None)
            self._N = ipw.BoundedIntText(placeholder='N', min=1, max=1e12, tooltip='Number of neurons')  # value=N

        elif self.group_type is 'TimedArray':
            self._FIELDS = self._TimedArray_fields
            # TimedArray(values, dt, name=None)

        else:
            print('Unknown Group Type ({})!'.format(self.group_type))

        #self.interface.ENTRIES.append(self)
        #self.interface.ENTRY_BOX = self.interface.ENTRIES
        #self.interface.ENTRY_COUNTER += 1

        # This crashes the kernel :(
        #self.ENTRY_BOX.children = [NGE for NGE in self.ENTRIES]




        # 'primary' 'success' 'info' 'warning' 'danger'
        self._copy = ipw.Button(button_style='info',
                                tooltip='Copy', icon='copy') # description='Copy',
        self._copy.on_click(self.on_click_copy)
        self._delete = ipw.Button(button_style='danger',
                                  tooltip='Delete', icon='fa-trash') # description='Delete',
        self._delete.on_click(self.on_click_delete)

        self.children = [self._name, self._N, self._model, self._threshold,
                         self._reset, self._refractory, self._method,
                         self._copy, self._delete]
        #self.on_displayed(ipw.Box._fire_children_displayed)
        #self._model_id = None

        if self.group_type is 'NeuronGroup':  # interface._controls['type']
            model = self.interface._controls['template'].value
            self.set_values(NEURON_MODELS[model])
            #for key, value in NEURON_MODELS['template'].items():
            #    field = '_{}'.format(key)
            #    self.__dict__[field].value = value


        children = [self.__dict__['_{}'.format(field)] for field in self._FIELDS]
        children.extend([self._copy, self._delete])
        self.children = children

        # Formatting - may need to set padding to align labels properly
        self._name.layout = ipw.Layout(width='110px', height='32px')
        self._N.layout = ipw.Layout(width='60px', height='32px')
        # Check if setting height stops it resizing properly c.f. old prototype
        self._model.layout = ipw.Layout(min_width='325px') #, height='96px')
        self._threshold.layout = ipw.Layout(width='80px', height='32px')
        self._reset.layout = ipw.Layout(width='80px', height='32px')
        self._refractory.layout = ipw.Layout(width='80px', height='32px')
        self._method.layout = ipw.Layout(width='70px', height='32px')
        self._copy.layout = ipw.Layout(width='25px', height='28px')
        self._delete.layout = ipw.Layout(width='25px', height='28px')

        #display(self)

    #def get_entry_index(self):
    #    return self.interface.ENTRIES.index(self)

    #def on_click_neuron_delete(self, b):
    #    del self.interface.ENTRIES[self.get_entry_index()]
    #    self.interface.ENTRY_BOX.children = self.interface.ENTRIES

        #self.ENTRIES[NGE for NGE in self.ENTRIES if NGE != self.get_entry_index()]
        #self.ENTRY_BOX.children = [NGE for NGE in self.ENTRIES]
