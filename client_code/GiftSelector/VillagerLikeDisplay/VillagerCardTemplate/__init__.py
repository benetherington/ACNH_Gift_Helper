from ._anvil_designer import VillagerCardTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ....VariationSelectorTemplate import VariationSelectorTemplate

class VillagerCardTemplate(VillagerCardTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    '''
    self.item looks like:
    {'villager': villager_dict, 'items': [item_row, item_row], purchased_on: 'date'}
    '''
    self.color_variations = []
    for item in self.item['items']:
      item_card = VariationSelectorTemplate(item=item)
      self.color_variations.append(item_card)
      self.variations_flow_panel.add_component(item_card)
    self.variations_flow_panel.raise_event_on_children('x-radio-disable')

