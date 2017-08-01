from collections import OrderedDict
import uuid

import ipywidgets as ipw
from ipywidgets.widgets import register
from IPython.display import display
from traitlets import Unicode

# from brian2gui.notebook import Brian2GUI
from brian2gui.models import NEURON_MODELS  # , LIF
from brian2gui.synapses import SynapseEntry
from brian2gui.utilities import Interface, Entry, Simulated


@register('brian2gui.InputsInterface')
class InputsInterface(Interface):  # ipw.Box):
    """Class definition for Brian 2 Inputs graphical interface"""

    _model_name = Unicode('VBoxModel').tag(sync=True)
    _view_name = Unicode('VBoxView').tag(sync=True)

    _TYPES = ('BinomialFunction', 'PoissonGroup', 'PoissonInput',
              'SpikeGeneratorGroup', 'TimedArray')

    _methods = ('linear', 'euler', 'heun')

    ENTRY_COUNTER = 0  # class variable shared by all instances
    ENTRIES = []
    ENTRY_BOX = ipw.VBox(children=[])  # NeuronGroupEntry()

    def __init__(self, gui=None):

        ipw.Box.__init__(self, _dom_classes=['widget-interact'])
        super().__init__()  # super(NeuronGroupInterface, self).__init__()

        self.gui = gui  # Top level container

        self._CONTROLS = OrderedDict([('type', ipw.Dropdown(description='Type',
                                                            options=self._TYPES)),
                                      ('new', ipw.Button(description='Add'))])

        #self.ENTRY_BOX = ipw.VBox(children=self.ENTRIES)  # self.children[-1]
        #self.ENTRY_BOX.children = self.ENTRIES

        self._CONTROLS['new'].on_click(self.on_new_clicked)

        self.children = [ipw.HBox(children=list(self._CONTROLS.values())),
                         self.ENTRY_BOX]
        #self.children = [self.accordion]

        #self.accordion.selected_index = list(self._CONTROLS.keys()).index('Neurons')
        #self.on_new_clicked(None, group_type='PoissonGroup')

        # Set formatting for entry controls
        self._CONTROLS['type'].layout = ipw.Layout(width='250px')
        self._CONTROLS['new'].layout = ipw.Layout(width='50px')
        self._CONTROLS['new'].button_style = 'success'

    def on_new_clicked(self, b, *args, **kwargs):
        # TODO: Consolidate this with inherited function
        #self.children[-1].children.append(NeuronGroupEntry())
        #NeuronGroupEntry(self, self._controls['type'].value)

        #if self.accordion.selected_index is list(self._CONTROLS.keys()).index('Inputs'):
        #    self.INPUT_ENTRIES.append(NeuronGroupEntry(self, self._CONTROLS['Inputs']['type'].value))
        #    self.INPUT_ENTRY_BOX.children = self.INPUT_ENTRIES
        #else:
        #    self.NEURON_ENTRIES.append(NeuronGroupEntry(self, 'NeuronGroup'))
        #    self.NEURON_ENTRY_BOX.children = self.NEURON_ENTRIES

        #self.ENTRIES.append(type(self)(self, group_type=self._CONTROLS['type'].value))
        self.ENTRIES.append(InputsEntry(self, group_type=self._CONTROLS['type'].value))
        #self.ENTRIES = self.NEURON_ENTRIES
        #self.ENTRIES.append(NeuronGroupEntry(self, self._controls['type'].value))
        self.ENTRY_BOX.children = self.ENTRIES  # [nge for nge in self.ENTRIES]
        self.ENTRY_COUNTER += 1


@register('brian2gui.InputsEntry')
class InputsEntry(Entry, Simulated):
    """Class definition for Brian 2 Inputs graphical entries"""

    _model_name = Unicode('HBoxModel').tag(sync=True)
    _view_name = Unicode('HBoxView').tag(sync=True)

    _ids = []  # class variable shared by all instances

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

    def __init__(self, interface=None, group_type=None, *args, **kwargs):

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

        if self.group_type is 'BinomialFunction':
            self._FIELDS = self._BinomialFunction_fields
            # BinomialFunction(n, p, approximate=True, name='_binomial*')
            self._n = ipw.BoundedIntText(description='n', min=1, max=1e12, tooltip='Number of samples')
            self._p = ipw.BoundedFloatText(description='p', min=0, max=1, tooltip='Probability')  # value=N
            self._approximate = ipw.Checkbox(description='Approximate', value=True, tooltip='Whether to approximate the binomial with a normal distribution if np>5 ∧ n(1−p)>5')
            #children = [self._name, self._n, self._p, self._approximate]

            self._n.layout = ipw.Layout(width='150px', height='32px')
            self._p.layout = ipw.Layout(width='150px', height='32px')

        elif self.group_type is 'PoissonGroup':
            self._FIELDS = self._PoissonGroup_fields
            # ('N', 'rates', 'dt', 'clock', 'when', 'order', 'name')
            self._N = ipw.BoundedIntText(description='N', min=1, max=1e12, tooltip='Number of neurons')
            self._rates = ipw.Text(placeholder='rates', tooltip='Single rate, array of rates of length N, or a string expression evaluating to a rate. This string expression will be evaluated at every time step, it can therefore be time-dependent (e.g. refer to a TimedArray).')
            self._dt = ipw.Text(placeholder='dt', value='0.1*ms', tooltip='dt')
            self._clock = ipw.Text(placeholder='clock', tooltip='clock')
            self._when = ipw.Dropdown(description='when', options=self._schedule, tooltip='when')
            self._order = ipw.IntSlider(description='order', value=0, min=0, max=10, step=1)
            #children = [self._name, self._N, self._rates, self._dt]

            self._N.layout = ipw.Layout(width='150px', height='32px')
            self._rates.layout = ipw.Layout(width='60px', height='32px')
            self._dt.layout = ipw.Layout(width='60px', height='32px')
            self._clock.layout = ipw.Layout(width='60px', height='32px')
            self._when.layout = ipw.Layout(width='300px', height='32px')
            self._order.layout = ipw.Layout(width='400px', height='32px')

        elif self.group_type is 'PoissonInput':
            self._FIELDS = self._PoissonInput_fields
            # PoissonInput(target, target_var, N, rate, weight, when='synapses', order=0)
            self._target = ipw.Dropdown(options=self.interface.gui.get_neuron_group_names(), tooltip='The group that is targeted by this input.')
            self._target_var = ipw.Text(placeholder='target_var', tooltip='The variable of target that is targeted by this input.')
            self._N = ipw.BoundedIntText(description='N', min=1, max=1e12, tooltip='The number of inputs')
            self._rate = ipw.Text(placeholder='rate', tooltip='The rate of each of the inputs')
            self._weight = ipw.Text(placeholder='weight', tooltip='Either a string expression (that can be interpreted in the context of target) or a Quantity that will be added for every event to the target_var of target. The unit has to match the unit of target_var')
            self._when = ipw.Dropdown(description='when', options=self._schedule, tooltip='when')
            self._order = ipw.IntSlider(description='order', value=0, min=0, max=10, step=1)

            self._target.layout = ipw.Layout(width='110px', height='32px')
            self._target_var.layout = ipw.Layout(width='110px', height='32px')
            self._N.layout = ipw.Layout(width='150px', height='32px')
            self._rate.layout = ipw.Layout(width='60px', height='32px')
            self._weight.layout = ipw.Layout(width='60px', height='32px')
            self._when.layout = ipw.Layout(width='300px', height='32px')
            self._order.layout = ipw.Layout(width='400px', height='32px')

        elif self.group_type is 'SpikeGeneratorGroup':
            # TODO: Finish attributes: codeobj_class
            self._FIELDS = ('N', 'indices', 'times', 'dt', 'clock', 'period', 'when', 'order', 'sorted', 'name')  # self._SpikeGeneratorGroup_fields
            # SpikeGeneratorGroup(N, indices, times, dt=None, clock=None, period=1e100*second, when='thresholds', order=0, sorted=False, name='spikegeneratorgroup*', codeobj_class=None)
            self._N = ipw.BoundedIntText(description='N', min=1, max=1e12, tooltip='Number of neurons')  # value=N
            self._indices = ipw.Text(placeholder='indices', tooltip='The indices of the spiking cells')
            self._times = ipw.Text(placeholder='times', tooltip='The spike times for the cells given in indices. Has to have the same length as indices.')
            self._dt = ipw.Text(placeholder='dt', value='0.1*ms', tooltip='dt')
            self._clock = ipw.Text(placeholder='clock', tooltip='clock')
            self._period = ipw.Text(placeholder='period', tooltip='If this is specified, it will repeat spikes with this period.')
            self._when = ipw.Dropdown(description='when', options=self._schedule, tooltip='when')
            self._order = ipw.IntSlider(description='order', value=0, min=0, max=10, step=1)
            self._sorted = ipw.Checkbox(description='Sorted', value=False, tooltip='Whether the given indices and times are already sorted. ')

            self._N.layout = ipw.Layout(width='150px', height='32px')
            self._indices.layout = ipw.Layout(width='250px', height='32px')
            self._times.layout = ipw.Layout(width='250px', height='32px')
            self._dt.layout = ipw.Layout(width='60px', height='32px')
            self._clock.layout = ipw.Layout(width='60px', height='32px')
            self._period.layout = ipw.Layout(width='60px', height='32px')
            self._when.layout = ipw.Layout(width='300px', height='32px')
            self._order.layout = ipw.Layout(width='400px', height='32px')

        elif self.group_type is 'TimedArray':
            self._FIELDS = self._TimedArray_fields
            # TimedArray(values, dt, name=None)
            self._values = ipw.Text(placeholder='values', tooltip='values')
            self._dt = ipw.Text(placeholder='dt', value='0.1*ms', tooltip='dt')
            #children = [self._name, self._values, self._dt]

            self._values.layout = ipw.Layout(width='300px', height='32px')
            self._dt.layout = ipw.Layout(width='60px', height='32px')

        else:
            print('Unknown Group Type ({})!'.format(self.group_type))


        # 'primary' 'success' 'info' 'warning' 'danger'
        self._copy = ipw.Button(button_style='info',
                                tooltip='Copy', icon='copy') # description='Copy',
        self._copy.on_click(self.on_click_copy)
        self._delete = ipw.Button(button_style='danger',
                                  tooltip='Delete', icon='fa-trash') # description='Delete',
        self._delete.on_click(self.on_click_delete)

        # TODO: Use this to generate children
        children = [self.__dict__['_{}'.format(field)] for field in self._FIELDS]
        children.extend([self._copy, self._delete])
        self.children = children

        # Formatting - may need to set padding to align labels properly
        self._name.layout = ipw.Layout(width='110px', height='32px')

        self._copy.layout = ipw.Layout(width='25px', height='28px')
        self._delete.layout = ipw.Layout(width='25px', height='28px')


@register('brian2gui.NeuronGroupInterface')
class NeuronGroupInterface(Interface):  # ipw.Box):
    """Class definition for Brian 2 NeuronGroup graphical interface"""

    _model_name = Unicode('VBoxModel').tag(sync=True)
    _view_name = Unicode('VBoxView').tag(sync=True)

    #_NEURON_TYPES = ('NeuronGroup', 'PoissonGroup', 'PoissonInput',
    #                 'SpikeGeneratorGroup')

    #_TYPES = ('BinomialFunction', 'PoissonGroup', 'PoissonInput',
    #                'SpikeGeneratorGroup', 'TimedArray')
    _TYPES = ('NeuronGroup')
    # _SHORT_NEURON_TYPES = ('NG', 'PG', 'PI', 'SGG')

    _methods = ('linear', 'euler', 'heun')

    # Make this an OrderedDict with the values as widths
    _NEURON_HEADER = ('Label', '$N$', 'Equations', 'Threshold', 'Reset',
                      'Refractoriness', 'Integrator')

    _labels = [ipw.Label(value=field) for field in _NEURON_HEADER]

    ENTRY_COUNTER = 0  # class variable shared by all instances
    ENTRIES = []
    ENTRY_BOX = ipw.VBox(children=[])  # NeuronGroupEntry()

    #INPUT_ENTRIES = []  # All input objects
    #INPUT_ENTRY_BOX = ipw.VBox(children=[])
    #NEURON_ENTRIES = []  # Just for NeuronGroups as these are the only targets
    #NEURON_ENTRY_BOX = ipw.VBox(children=[])

    def __init__(self, gui=None):

        ipw.Box.__init__(self, _dom_classes=['widget-interact'])
        super().__init__()  # super(NeuronGroupInterface, self).__init__()

        self.gui = gui  # Top level container

        self._CONTROLS = OrderedDict([#('type', ipw.Dropdown(description='Type', options=self._NEURON_TYPES)),
                                      ('template', ipw.Dropdown(description='Template', options=list(NEURON_MODELS.keys()))),
                                      ('new', ipw.Button(description='Add'))])

        # Make accordion for each type of group
        #input_controls = OrderedDict([('type', ipw.Dropdown(description='Type', options=self._TYPES)),
        #                              ('new', ipw.Button(description='Add'))])
        #neuron_controls = OrderedDict([('template', ipw.Dropdown(description='Template', options=list(NEURON_MODELS.keys()))),
        #                               ('new', ipw.Button(description='Add'))])
        #self._CONTROLS = OrderedDict([('Inputs', input_controls),
        #                              ('Neurons', neuron_controls)])
        #self.accordion = ipw.Accordion(children=[ipw.VBox(children=[ipw.HBox(children=list(self._CONTROLS['Inputs'].values())), self.INPUT_ENTRY_BOX]),
        #                                         ipw.VBox(children=[ipw.HBox(children=list(self._CONTROLS['Neurons'].values())), self.NEURON_ENTRY_BOX])])
        #for ind, title in enumerate(self._CONTROLS.keys()):
        #    self.accordion.set_title(ind, title)

        #self.ENTRIES.append(NeuronGroupEntry())

        #self.ENTRY_BOX = ipw.VBox(children=self.ENTRIES)  # self.children[-1]
        #self.ENTRY_BOX.children = self.ENTRIES

        self.children = [ipw.HBox(children=list(self._CONTROLS.values())),
        #                 ipw.HBox(children=self._labels),
                         self.ENTRY_BOX]#self.ENTRIES)]  # _neuron_group_entries)]

        #self._CONTROLS['new'].on_click(self.on_new_clicked)

        #self._CONTROLS['Inputs']['new'].on_click(self.on_new_clicked)
        #self._CONTROLS['Neurons']['new'].on_click(self.on_new_clicked)
        self._CONTROLS['new'].on_click(self.on_new_clicked)

        #self.accordion.selected_index = list(self._CONTROLS.keys()).index('Neurons')
        self.on_new_clicked(None)  # Create a neuron group of the default type (blank)

        # Set formatting for entry controls
        self._CONTROLS['template'].layout = ipw.Layout(width='250px')
        self._CONTROLS['new'].layout = ipw.Layout(width='50px')
        self._CONTROLS['new'].button_style = 'success'

        #self.children[0].children[0].width = '250px'


# NeuronGroup(N, model, method=('linear', 'euler', 'heun'), threshold=None,
#             reset=None, refractory=False, events=None, namespace=None,
#             dtype=None, dt=None, clock=None, order=0, name='neurongroup*',
#             codeobj_class=None)

    #def on_group_select(self, change):
    #    if change['new'] is 'NeuronGroup':  # self._controls['type']
    #        self._CONTROLS['template'].disabled = False
    #    else:
    #        self._CONTROLS['template'].disabled = True

    def on_new_clicked(self, b):
        # TODO: Generalise this to create the right type of entry
        self.ENTRIES.append(NeuronGroupEntry(self))
        # self.ENTRIES.append(type(self)(self, self._CONTROLS['type'].value))
        # self.ENTRIES.append(type(self)(self, group_type=self._CONTROLS['type'].value))
        self.ENTRY_BOX.children = self.ENTRIES  # [nge for nge in self.ENTRIES]
        self.ENTRY_COUNTER += 1


@register('brian2gui.NeuronGroupEntry')
class NeuronGroupEntry(Entry):  # ipw.Box):  # NeuronGroupInterface
    """Class definition for Brian 2 NeuronGroup graphical entries"""
    # Should this be a single row or the whole set?

    _model_name = Unicode('VBoxModel').tag(sync=True)
    _view_name = Unicode('VBoxView').tag(sync=True)

    _ids = []  # class variable shared by all instances

    # NeuronGroup(N, model, method=('linear', 'euler', 'heun'), threshold=None,
    # reset=None, refractory=False, events=None, namespace=None, dtype=None,
    # dt=None, clock=None, order=0, name='neurongroup*', codeobj_class=None)
    _NeuronGroup_fields = ('N', 'model', 'method', 'threshold', 'reset',
                           'refractory', 'name')  # 'events', 'namespace', 'dtype', 'dt', 'clock', 'order', 'codeobj_class'

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

    def __init__(self, interface=None, group_type='NeuronGroup', *args, **kwargs):  # N=10, model=LIF, method=None,
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

        self._FIELDS = self._NeuronGroup_fields
        # events=None, namespace=None, dtype=None,
        # dt=None, clock=None, order=0, name='neurongroup*', codeobj_class=None]
        self._N = ipw.BoundedIntText(placeholder='N', min=1, max=1e12, tooltip='Number of neurons')  # value=N
        self._model = ipw.Textarea(placeholder='model', tooltip='Model equations')
        self._method = ipw.Dropdown(options=self.interface._methods, tooltip='Integrator')  # INTEGRATORS
        self._threshold = ipw.Text(placeholder='threshold', tooltip='Threshold')
        self._reset = ipw.Text(placeholder='reset', tooltip='Reset condtion')
        self._refractory = ipw.Text(placeholder='refractory', tooltip='Refractory period')
        # TODO: Finish attributes

        # Formatting
        self.layout = ipw.Layout(border='solid 1px', overflow_x='scroll', margin='1px')
        self._N.layout = ipw.Layout(width='60px', height='32px')
        # Check if setting height stops it resizing properly c.f. old prototype
        self._model.layout = ipw.Layout(min_width='600px') #, height='96px')
        self._threshold.layout = ipw.Layout(width='80px', height='32px')
        self._reset.layout = ipw.Layout(width='80px', height='32px')
        self._refractory.layout = ipw.Layout(width='80px', height='32px')
        self._method.layout = ipw.Layout(width='70px', height='32px')


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

        #self.children = [self._name, self._N, self._model, self._threshold,
        #                 self._reset, self._refractory, self._method,
        #                 self._copy, self._delete]

        #self.on_displayed(ipw.Box._fire_children_displayed)
        #self._model_id = None

        #if self.group_type is 'NeuronGroup':  # interface._controls['type']
        model = self.interface._CONTROLS['template'].value
        self.set_values(NEURON_MODELS[model])
        #for key, value in NEURON_MODELS['template'].items():
        #    field = '_{}'.format(key)
        #    self.__dict__[field].value = value

        #children = [self.__dict__['_{}'.format(field)] for field in self._FIELDS]
        #children.extend([self._name, self._copy, self._delete])
        children = [ipw.HBox(children=[self._N, self._method, self._threshold,
                                       self._reset, self._refractory,
                                       self._name, self._copy, self._delete]),
                    ipw.HBox(children=[self._model])]

        self.children = children

        # Formatting - may need to set padding to align labels properly
        self._name.layout = ipw.Layout(width='110px', height='32px')

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
