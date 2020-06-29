from ._anvil_designer import YourVillagersDisplayTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Globals

class YourVillagersDisplay(YourVillagersDisplayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    '''
    self.item is a list of villager rows.
    '''
    # event handlers
    self.set_event_handler('x-enable-remove-button', self.enable_remove_button)
    self.set_event_handler('x-disable-remove-button', self.disable_remove_button)
    self.set_event_handler('x-all-villagers-changed', self.all_villagers_changed)
    
    
  '''
  EVENT PASS-THROUGHS
  '''
  def enable_remove_button(self, **event_args):
    self.your_villagers_repeating_panel \
      .raise_event_on_children('x-enable-remove-button', **event_args)
  def disable_remove_button(self, **event_args):
    self.your_villagers_repeating_panel \
      .raise_event_on_children('x-disable-remove-button', **event_args)
  def all_villagers_changed(self, **event_args):
    # originated by AllVillagersTemplate, args include removed=bool and
    # villager={'name':'', 'icon_image':''}
    self.your_villagers_repeating_panel \
      .raise_event_on_children('x-all-villagers-changed', **event_args)
    
  '''
  BINDING ACCESSORS
  '''
  def current_user_is_guest(self, **event_args):
    return Globals.current_user_is_guest()

  