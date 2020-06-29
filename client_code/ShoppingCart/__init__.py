from ._anvil_designer import ShoppingCartTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class ShoppingCart(ShoppingCartTemplate):
  def __init__(self, **properties):
    # don't permit guestmode
    if Globals.current_user_is_guest():
      open_form('GiftSelector')
    # init data
    self.status_filter_drop_down.items = [ ("Shopping list", 'neither'),
                                           ("Delivery list", 'not_delivered'),
                                           ("History", 'all')]
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
    
  
  '''
  UI
  '''
  def filters_drop_down_change(self, **event_args):
    self.refresh_data_bindings()
  def delete_toggle_link_click(self, **event_args):
    self.villager_gift_repeating_panel.raise_event_on_children('x-toggle-delete')
  
  # SIDEBAR
  def selector_button_click(self, **event_args):
    open_form('GiftSelector')
  def settings_button_click(self, **event_args):
    open_form('Settings')
  def about_button_click(self, **event_args):
    open_form('About')

    
  '''
  BINDING ACCESSORS
  '''
  def cart_item_count(self, **event_args):
    return Globals.cart_quantity

  '''
  DATA BINDINGS
  '''
  def form_refreshing_data_bindings(self, **event_args):
    server_data = anvil.server.call('get_gifts',
                                    status=self.status_filter_drop_down.selected_value)
    self.villager_gift_repeating_panel.items = server_data








