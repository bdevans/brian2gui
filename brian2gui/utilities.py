import abc
import uuid
from collections import OrderedDict
from traitlets import Unicode
import ipywidgets as ipw
from ipywidgets.widgets import register

__all__ = ['Interface', 'Entry']


# @abc.ABCMeta
@register('brian2gui.Interface')
class Interface(ipw.Box):

    _model_name = Unicode('VBoxModel').tag(sync=True)
    _view_name = Unicode('VBoxView').tag(sync=True)

    _TYPES = None
    _CONTROLS = None

    ENTRY_BOX = ipw.VBox(children=())
    ENTRIES = []
    ENTRY_COUNTER = 0

    def __init__(self, gui=None, *args, **kwargs):  # name='',

        # ipw.Box.__init__(self, _dom_classes=['widget-interact'])
        super().__init__(*args, **kwargs)
        self.gui = gui  # Top level container

    def on_new_clicked(self, b, *args, **kwargs):
        self.ENTRIES.append(type(self)(self, *args, **kwargs))
        self.ENTRY_BOX.children = self.ENTRIES  # [nge for nge in self.ENTRIES]
        self.ENTRY_COUNTER += 1


# @abc.ABCMeta
@register('brian2gui.Entry')
class Entry(ipw.Box):

    __metaclass__ = abc.ABCMeta

    _model_name = Unicode('HBoxModel').tag(sync=True)
    _view_name = Unicode('HBoxView').tag(sync=True)

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, name):
        self._name.value = name

    def __init__(self, interface=None, *args, **kwargs):  # group_type=None,
        super().__init__()
        self.interface = interface
        if 'group_type' in kwargs:
            # self.group_type = group_type
            self.group_type = kwargs['group_type']
        self._uuid = uuid.uuid4()

    def _change_name(self, change):
        self._name.value = change['new']

    def get_index(self):
        return self.interface.ENTRIES.index(self)

    def get_values(self):
        """Get all values and put them in an OrderedDict"""
        # return OrderedDict([(label, w.value) for (label, w)
        #                     in zip(self._FIELDS, self.children)])
        # TODO: Revert to more elegant function above
        pairs = []
        for key in self._FIELDS:
            attribute = '_{}'.format(key)
            if hasattr(self, attribute):
                pairs.append((key, self.__dict__[attribute].value))
        return OrderedDict(pairs)

    def set_values(self, values_dict):
        """Set all values except the label from a dictionary"""
        for key, value in values_dict.items():
            # This can be simplified with property decorators:
            # e.g. self.__dict__[key] = value
            attribute = '_{}'.format(key)
            if hasattr(self, attribute) and key is not 'name':
                self.__dict__[attribute].value = value

    def on_click_copy(self, b):
        clone = type(self)(self.interface, self.group_type)  # self.deepcopy()
        clone.set_values(self.get_values())
        # Insert after original
        self.interface.ENTRIES.insert(self.get_index()+1, clone)
        self.interface.ENTRY_BOX.children = self.interface.ENTRIES
        self.interface.ENTRY_COUNTER += 1

    def on_click_delete(self, b):
        del self.interface.ENTRIES[self.get_index()]
        self.interface.ENTRY_BOX.children = self.interface.ENTRIES


@register('brian2gui.Simulated')
class Simulated(object):
    '''Class for simulated objects.
    See: http://brian2.readthedocs.io/en/stable/user/running.html'''

    __metaclass__ = abc.ABCMeta

    _dt = None
    _schedule = ['start', 'groups', 'thresholds', 'synapses', 'resets', 'end']
    _when = None
    _order = None  # Default: 0
