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

        # TODO: Consolidate the ITEMS/CONTROLS
        self._FIELDS = ['timestep', 'duration']
        self._ITEMS = OrderedDict([('timestep', ipw.Text(description='Timestep, $dt$', value='0.1*ms')),
                                   ('duration', ipw.Text(description='Duration', value='100*ms'))])
        for field in self._FIELDS:
            setattr(self, '_{}'.format(field), self._ITEMS[field])
        #'fa-flask'
        controls = [('Build', ipw.Button(description='Build', tooltip='Build',
                                         button_style='success', icon='fa-gears')),
                    ('Run', ipw.Button(description='Run', tooltip='Run',
                                       button_style='success', icon='fa-play')),
                    ('Progress', ipw.FloatProgress(description='Progress',
                                                   min=0, max=1,
                                                   icon='fa-hourglass')),
                    ('Save', ipw.Button(description='Save', tooltip='Save',
                                        button_style='info', icon='fa-save')),

                    ('Load', ipw.Button(description='Load', tooltip='Load',
                                        button_style='info', icon='fa-sign-in')),
                    ('Filename', ipw.Text(description='Filename'))]
        self._CONTROLS = OrderedDict(controls)

        self.children = (ipw.HBox(children=[self._CONTROLS['Filename'],
                                            self._CONTROLS['Save'],
                                            self._CONTROLS['Load']]),
                         ipw.HBox(children=[self._CONTROLS['Build'],
                                            self._timestep,
                                            self._duration,
                                            self._CONTROLS['Run'],
                                            self._CONTROLS['Progress']]))

                         #(ipw.HBox(children=list(self._CONTROLS.values())),
                         #ipw.HBox(children=self._LABELS),
                         #self.ENTRY_BOX)


        #self._CONTROLS['new'].on_click(self.on_new_clicked)
