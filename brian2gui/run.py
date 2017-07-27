from collections import OrderedDict
from traitlets import Unicode
import ipywidgets as ipw
from ipywidgets.widgets import register

from brian2gui.utilities import Interface


@register('brian2gui.Interface')
class RunInterface(Interface):  # brian2gui.

    #_model_name = Unicode('VBoxModel').tag(sync=True)
    #_view_name = Unicode('VBoxView').tag(sync=True)

    #_TYPES = ()
    #_CONTROLS = () #OrderedDict([('type', ipw.Dropdown(description='Type', options=_TYPES)),
                #             ('new', ipw.Button(description='Add'))])

    #ENTRY_BOX = ipw.VBox(children=())
    #ENTRIES = []
    #ENTRY_COUNTER = 0

    def __init__(self, gui=None, *args, **kwargs):  # name='',

        super().__init__(*args, **kwargs)
        self.gui = gui  # Top level container

        self._FIELDS = ['timestep', 'duration']
        self._ITEMS = OrderedDict([('timestep', ipw.Text(description='Timestep, $dt$', value='0.1*ms')),
                                   ('duration', ipw.Text(description='Duration', value='100*ms'))])
        for field in self._FIELDS:
            setattr(self, '_{}'.format(field), self._ITEMS[field])

        self._progress = ipw.FloatProgress(description='Progress', min=0, max=1)
        self.children = (self._timestep,
                         self._duration,
                         ipw.Button(description='Run', button_style='danger',
                                    tooltip='Run', icon='fa-flask'),
                         self._progress,
                         ipw.Button(description='Save', button_style='info',
                                    tooltip='Save', icon='fa-flask'),
                         ipw.Button(description='Load', button_style='info',
                                    tooltip='Load', icon='fa-flask'),
                         ipw.Text(description='Filename'))
                         #(ipw.HBox(children=list(self._CONTROLS.values())),
                         #ipw.HBox(children=self._LABELS),
                         #self.ENTRY_BOX)


        #self._CONTROLS['new'].on_click(self.on_new_clicked)
