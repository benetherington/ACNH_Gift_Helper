from ._anvil_designer import VillagerLikeDisplayTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .VillagerCardTemplate import VillagerCardTemplate
from ... import Globals

class VillagerLikeDisplay(VillagerLikeDisplayTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    '''
    self.item looks like:
    [{'villager': villager_dict, 'items': [item_row, item_row], 'purchased_on': 'date'}, ...]
    '''
  
  
  '''
  BINDING ACCESSORS
  '''
  def cart_item_count(self, **event_args):
    return Globals.cart_quantity
      
  '''
  UI
  '''
  def add_to_cart_button_click(self, **event_args):
    selected_items = []
    villagers = self.column_panel.get_components()
    # find which variations the user selected
    for villager in villagers:
      for variation in villager.color_variations:
        if variation.radio_selected:
          # add selected variables to a list to send to the server
          villager = villager.item['villager']
          item = variation.item
          selected_items.append({'villager': villager, 'item': item})
          # increment the cart counter
          Globals.cart_quantity += 1
    anvil.server.call('assign_gifts',selected_items)
    self.refresh_data_bindings()
    get_open_form().refresh_data_bindings()

  def go_to_cart_button_click(self, **event_args):
    open_form('ShoppingCart')

  '''
  BINDING ACCESSORS
  '''
  def current_user_is_not_guest(self, **event_args):
    return Globals.current_user_is_not_guest()
  
  '''
  BINDING
  '''
  def form_refreshing_data_bindings(self, **event_args):
    for component in self.column_panel.get_components():
      component.remove_from_parent()
    for item in self.item:
      villager_card = VillagerCardTemplate(item=item)
      self.column_panel.add_component(villager_card)


