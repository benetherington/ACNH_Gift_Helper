from ._anvil_designer import AboutTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class About(AboutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
  '''
  UI
  '''
  # SIDEBAR
  def cart_button_click(self, **event_args):
    if Globals.current_user_is_guest():
      anvil.alert("""Please log in to view your shopping cart and delivery 
        checklist. You'll also get access to your gift history, and we can warn 
        you if you've already given this item as a gift recently. """,
        title="This feature is not available to guests")
    else:
      open_form('ShoppingCart')
  def settings_button_click(self, **event_args):
    open_form('Settings')
  def selector_button_click(self, **event_args):
    open_form('GiftSelector')
    
  '''
  BINDING ACCESSORS
  '''
  def current_user_is_not_guest(self, **event_args):
    return Globals.current_user_is_not_guest()
  def cart_item_count(self, **event_args):
    return Globals.cart_quantity
  def version(self, **event_args):
    return Globals.VERSION




