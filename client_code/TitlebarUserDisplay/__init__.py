from ._anvil_designer import TitlebarUserDisplayTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class TitlebarUserDisplay(TitlebarUserDisplayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    '''
    self.item is a user row or a dict that looks like one.
    '''
    
  '''
  BINDING ACCESSORS
  '''
  def user_email(self, **event_args):
    return Globals.current_user['email']
  def current_user_is_guest(self, **event_args):
    return Globals.current_user_is_guest()
  
  '''
  UI
  '''
  def login_link_click(self, **event_args):
    successful_login = anvil.users.login_with_form()
    if successful_login:
      Globals.update_user_cache()
      self.item = successful_login
    self.refresh_data_bindings()
    get_open_form().refresh_data_bindings()
  def logout_link_click(self, **event_args):
    anvil.users.logout()
    Globals.update_user_cache()
    self.refresh_data_bindings()
    get_open_form().refresh_data_bindings()




  
