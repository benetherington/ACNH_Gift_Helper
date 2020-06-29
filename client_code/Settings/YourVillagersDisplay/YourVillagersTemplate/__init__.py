from ._anvil_designer import YourVillagersTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import Globals

class YourVillagersTemplate(YourVillagersTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    '''
    self.item is a villager row.
    '''
    self.set_event_handler('x-enable-remove-button', self.enable_remove_button)
    self.set_event_handler('x-disable-remove-button', self.disable_remove_button)
    self.set_event_handler('x-all-villagers-changed', self.all_villagers_changed)

  '''
  EVENT HANDLERS
  '''
  def all_villagers_changed(self, **event_args):
    # originated by AllVillagersTemplate, args include removed=bool and
    # villager={'name':'', 'icon_image':''}. If it gets here, removed will always
    # be True thanks to logic in Settings form.
    if event_args['villager']['name'] == self.item['name']:
      self.remove_from_parent()
  
  '''
  UI
  '''
  def remove_button_click(self, **event_args):
    # do the thing
    Globals.assign_villager(self.item, True)
    # make it look good
    get_open_form().raise_event('x-your-villagers-removed', villager=self.item)
    self.remove_from_parent()
  def enable_remove_button(self, **event_args):
    self.remove_button.visible = True
  def disable_remove_button(self, **event_args):
    self.remove_button.visible = False

