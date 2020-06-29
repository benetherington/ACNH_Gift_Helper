from ._anvil_designer import AllColorsDisplayTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .VariationCardTemplate import VariationCardTemplate
from ... import Globals

class AllColorsDisplay(AllColorsDisplayTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    '''
    self.items looks like: [item_row, item_row]
    '''
    
  '''
  BINDING 'ACCESSORS'
  '''    
  def warning_text(self, **event_args):
    if Globals.current_user['villagers']:
      return "No villagers love this item's style and color. Here are all the color options."
    else:
      return "You haven't selected any villagers on the settings page. Here are all the color options."

  '''
  UI
  '''
  def form_refreshing_data_bindings(self, **event_args):
    self.flow_panel.clear()
    for item in self.item:
      item_card = VariationCardTemplate(item=item)
      self.flow_panel.add_component(item_card)

