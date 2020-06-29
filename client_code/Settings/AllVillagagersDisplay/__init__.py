from ._anvil_designer import AllVillagagersDisplayTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AllVillagagersDisplay(AllVillagagersDisplayTemplate):
  def __init__(self, **properties):
    self.expanded = False
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    '''
    self.item looks like:
    {
      range: 'AB',
      'segment': [
        { "selected": True, "villager": {'name':'', 'icon_image':''} }, ...
      ]
    }
    '''
    # EVENT HANDLERS
    self.set_event_handler('x-expand-all', self.expand_all)
    self.set_event_handler('x-collapse-all', self.collapse_all)
    # EVENT PASS-THROUGH
    self.set_event_handler('x-enable-select-button', lambda **event_args:
             self.repeating_panel.raise_event_on_children('x-enable-select-button', **event_args))
    self.set_event_handler('x-disable-select-button', lambda **event_args:
             self.repeating_panel.raise_event_on_children('x-disable-select-button', **event_args))
    self.set_event_handler('x-your-villagers-removed', lambda **event_args:
             self.repeating_panel.raise_event_on_children('x-your-villagers-removed', **event_args))
    self.set_event_handler('x-ur-a-winner-baby', lambda **event_args:
             self.repeating_panel.raise_event_on_children('x-ur-a-winner-baby', **event_args))

  '''
  UI
  '''
  def accordion_link_click(self, **event_args):
    self.expanded = not self.expanded
    if self.expanded:
      self.repeating_panel.items = self.item['segment']
    else:
      self.repeating_panel.items = []
    self.refresh_data_bindings()
  
  '''
  DATA BINDING
  '''
  def accordion_label(self, **event_args):
    # formats range string into comma/ampersand separated string
    range_str = self.item['range']
    range_formatted = ('{}, '*(len(range_str)-2) + '{} & '*(len(range_str)>1) + '{}').format(*range_str)
    # return something like: "A, B & C (5)"
    return f"{range_formatted} ({len(self.item['segment'])})"
    
  '''
  EVENT HANDLERS
  '''
  def expand_all(self, **event_args):
    self.expanded = False # accordion_link_click toggles this, so set what we DON'T want.
    self.accordion_link_click()
  def collapse_all(self, **event_args):
    self.expanded = True # accordion_link_click toggles this, so set what we DON'T want.
    self.accordion_link_click()
    
    
    
    
    
    
    
    
