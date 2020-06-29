from ._anvil_designer import VillagerGiftTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class VillagerGiftTemplate(VillagerGiftTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    '''
    self.item looks like:
      {
        "name":"Mac",
        "icon_image":"URL",
        "preferences":"style, style, color, color",
        "gifts": [ {'selected': gift_row, 'all_others': [item_row, item_row]} ...]
      }
    '''
    # pass through event handler
    self.set_event_handler('x-toggle-delete',
                           lambda **event_args: self.gift_repeating_panel
                           .raise_event_on_children('x-toggle-delete'))
    self.set_event_handler('x-item-deleted', self.item_deleted)
  
  '''
  EVENT HANDLERS
  '''
  def item_deleted(self, **event_args):
    # called by GiftTemplate just before it removes itself
    if len(self.gift_repeating_panel.get_components()) == 1:
      # no gifts are left, change some UI elements
      # we don't need to worry about changing the labels back later b/c
      # the elements will be recreated before new items can be added
      self.image.height = 44
      self.villager_label.visible = False
      self.before_name_label.text = "No gifts left for "
      self.after_name_label.text = '.'
      self.nothing_to_display_flow_panel.visible = True
  
  '''
  DATA BINDING
  '''
  def form_refreshing_data_bindings(self, **event_args):
    if self.item['gifts']:
      self.gift_repeating_panel.items = self.item['gifts']
    else:
      # no gifts were assigned, change some UI elements
      self.image.height = 44
      self.villager_label.visible = False
      self.nothing_to_display_flow_panel.visible = True
      
      
      
      
