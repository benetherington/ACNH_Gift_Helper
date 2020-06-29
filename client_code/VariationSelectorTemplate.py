from ._anvil_designer import VariationSelectorTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.image

class VariationSelectorTemplate(VariationSelectorTemplateTemplate):
  '''
  A radio button-style object that can store an item, allow the user to select it,
  alert its neighbors when its been selected, disable itself if a neighbor is selcted,
  and tell its parent that it's been selected.
  '''
  def __init__(self, **properties):
    self.init_components(**properties)
    '''
    self.item is an item row
    '''
    self.set_event_handler('x-radio-enable', self.radio_enable)
    self.set_event_handler('x-radio-disable', self.radio_disable)
    self.radio_selected = False
    self.image.width = self.image.height = self.flow_panel_1.width = self.img_size
  
  '''
  UTILITIES
  '''
  def radio_enable(self, **event_args):
    self.card.role = 'card'
    self.card.background = ''
    self.image.role = ''
    self.radio_selected = True
  def radio_disable(self, **event_args):
    self.card.role = 'default'
    self.card.background = 'theme:Gray 300'
    self.image.role = 'image-dim'
    self.radio_selected = False
  
  '''
  UI
  '''
  def image_mouse_down(self, x, y, button, **event_args):
    if self.radio_selected:
      self.radio_disable()
    else:
      self.parent.raise_event_on_children('x-radio-disable')
      self.raise_event('x-selected')
      self.radio_enable()
