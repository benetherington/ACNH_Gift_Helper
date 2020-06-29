from ._anvil_designer import AllVillagersTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Globals

class AllVillagersTemplate(AllVillagersTemplateTemplate):
  '''
  This is an object that displays a villager's image and name, and a button
  to allow the user to add or remove them from their profile. For some reason,
  I decided I wanted as little logic in here as posisble, so literally the only
  comparison that is made is to determine if an incoming event applies to it
  or not. It was fun to work with this restriction, but I'm not sure it's
  super helpful, as it requires some amount of code duplication in other places.
  '''
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    '''
    self.item is a dict that looks like:
    { "selected": True, "villager": {'name':'', 'icon_image':''} }
    '''
    # set event handlers
    self.set_event_handler('x-your-villagers-removed', self.your_villagers_removed)
    self.set_event_handler('x-ur-a-winner-baby', self.select_remove_button_click)
  
  '''
  UI
  '''
  def select_remove_button_click(self, **event_args):
    # do the thing
    Globals.assign_villager(self.item['villager']['name'], self.item['selected'])
    # make it look good
    get_open_form().raise_event('x-all-villagers-changed',
                                villager=self.item['villager'],
                                removed=self.item['selected'])
    self.item['selected'] = not self.item['selected']
    self.refresh_data_bindings()
    
  '''
  EVENT HANDLERS
  '''
  def your_villagers_removed(self, **event_args):
    if event_args['villager']['name'] == self.item['villager']['name']:
      self.item['selected'] = False
    self.refresh_data_bindings()
    
    
    
    
    