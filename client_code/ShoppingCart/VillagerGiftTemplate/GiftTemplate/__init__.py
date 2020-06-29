from ._anvil_designer import GiftTemplateTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....VariationSelectorTemplate import VariationSelectorTemplate
from .... import Globals

class GiftTemplate(GiftTemplateTemplate):
  def __init__(self, **properties):
    # init class variables
    self.delete_active = False
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    '''
    self.item looks like: {'selected': gift_row, 'all_others': [item_row, item_row]}
    '''
    # set event handlers
    self.set_event_handler('x-toggle-delete', self.toggle_delete)

  '''
  EVENT HANDLERS
  '''
  def variation_changed(self, **event_args):
    # called when VariationSelectorTemplate raises 'x-selected'
    new_variation = event_args['sender'].item
    anvil.server.call_s('update_gift_item', self.item['selected'], new_variation)
  def toggle_delete(self, **event_args):
    if self.delete_active:
      self.delete_button.foreground = 'theme:Gray 300'
    else:
      self.delete_button.foreground = 'theme:Secondary 700'
    self.delete_active = not self.delete_active
  
  '''
  UI
  '''
  def checkboxes_changed(self, **event_args):
    # update the server
    anvil.server.call_s('update_gift_status',
                        gift=self.item['selected'],
                        purchased=self.purchased_checkbox.checked,
                        delivered=self.delivered_checkbox.checked
                       )
    # update the UI
    self.delivered_checkbox.enabled = self.purchased_checkbox.checked
  def delete_button_click(self, **event_args):
      if self.delete_active:
        self.parent.parent.raise_event('x-item-deleted')
        self.remove_from_parent()
        anvil.server.call_s('delete_gift', self.item['selected'])
        Globals.cart_quantity -= 1

  '''
  DATA BINDINGS
  '''
  def form_refreshing_data_bindings(self, **event_args):
    # clear the flow panel
    self.variations_flow_panel.clear()
    # add the selected item to the panel
    this_item = self.item['selected']['item']
    variation_card = VariationSelectorTemplate(item=this_item, img_size=50)
    variation_card.set_event_handler('x-selected', self.variation_changed)
    self.variations_flow_panel.add_component(variation_card)
    # add the other items to the panel and disable them
    other_variations = self.item['all_others']
    for variation in other_variations:
      variation_card = VariationSelectorTemplate(item=variation, img_size=50)
      self.variations_flow_panel.add_component(variation_card)
      variation_card.set_event_handler('x-selected', self.variation_changed)
      variation_card.raise_event('x-radio-disable')



      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
