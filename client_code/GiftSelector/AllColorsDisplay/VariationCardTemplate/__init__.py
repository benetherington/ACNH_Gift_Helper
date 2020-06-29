from ._anvil_designer import VariationCardTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class VariationCardTemplate(VariationCardTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    '''
    self.item is an item row
    '''
    
#     self.villager_like_repeating_panel.items = self.item[1]
#     self.villager_like_repeating_panel.set_event_handler('x-gift-selected', self.select_gift)
    
#   def select_gift(self, **kwargs):
#     anvil.server.call_s('assign_gift', item=self.item[0], villager=kwargs['villager'])