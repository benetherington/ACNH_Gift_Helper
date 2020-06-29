from ._anvil_designer import GiftSelectorTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

# Thanks to all the folks behind tinyurl.com/acnh-sheet for the data that drives this app.

# TODO: if a user assigns a gift to a villager, then removes the villager,
# the gift will still get counted in the cart count, but won't appear. Need to
# either delete gifts assigned to a villager, limit the count, or display all
# gifts in the cart, not just those associated with selected villagers.
# TODO: build a nicer history display in ShoppingCart with dates and narrow row heights.

class GiftSelector(GiftSelectorTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # initiate UI
    self.and_more_label.text = ''
    # set event handlers
    self.results_repeating_panel.set_event_handler('x-search-results-select-clicked', self.view_colors)
    
  '''
  UI
  '''
  def search_text_box_change(self, **event_args):
    # show/hide clear button
    self.refresh_data_bindings()
    # update UI to make sure we're in search mode
    self.search_panel.visible = True
    self.assign_panel.visible = False
    # search for the string
    search_string = self.search_text_box.text
    if search_string == '':
      self.results_repeating_panel.items = []
      return
    search_results = [i for i in Globals.item_names if search_string.lower() in i.lower()]
    # set UI elements
    show_number = int(self.results_show_dropdown.selected_value)
    self.results_repeating_panel.items = search_results[:show_number]
    if len(search_results) > show_number:
      self.and_more_label.text = f'And {len(search_results)-show_number} more...'
    else:
      self.and_more_label.text = ''
  def assign_panel_close_button_click(self, **event_args):
    # update UI to change back to search mode
    self.search_panel.visible = True
    self.assign_panel.visible = False

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
  def about_button_click(self, **event_args):
    open_form('About')
    
  '''
  EVENT HANDLERS
  '''
  def view_colors(self, **event_args):
    '''
    Called by SearchResultsTemplate when a user selects an item name.
    Displays all variations in VillagerLikeDisplay or AllColorsDisplay.
    '''
    # quick UI update to display item name
    item_name = event_args['item_name']
    self.selected_item_label.text = item_name
    # update UI to change to item assignment mode
    self.search_panel.visible = False
    self.assign_panel.visible = True
    # get data from the server, and do a little parsing
    server_details = anvil.server.call('get_item_details',
                                       item_name=item_name,
                                       user=Globals.current_user)
    # populate VillagerLikeDisplay or AllColorsDisplay with server data
    if len(server_details['matches']) > 0:
      self.villager_like_display.item = server_details['matches']
      self.villager_like_display.visible = True
      self.all_colors_display.visible = False
    else:
      # if nothing matched, display a placeholder
      self.all_colors_display.item = server_details['all_colors']
      self.villager_like_display.visible = False
      self.all_colors_display.visible = True
      self.user_needs_warning() # let guests know limitations
    # update the selected item label
    item_style = server_details['style']
    self.selected_item_label.text = f"{item_name} ({item_style})"

  '''
  UTILITIES
  '''
  def user_needs_warning(self, **event_args):
    '''
    Does nothing if a user is logged in. If we're in guest mode, and they haven't
    seen this warning, warn them about restrictions and give them some options.
    
    Note that AllColorsDisplay further warns users that don't have villagers selected.
    '''
    if Globals.current_user_is_not_guest() or Globals.current_user['warned']:
      # skip all users and warned guests
      return
    else:
      # handle non-warned guest
      a = anvil.alert(("You're running in guest mode with limited features. "
                      "Create an account to access the shopping cart, "
                      "gift history, and warnings for items you've already "
                       "given as gifts."),
                 title='Guest mode',
                 buttons=[
                   ('Continue in guest mode', 'continue'),
                   ('Log in or create an account', 'login')
                 ])
    # take action based on guest response
    if a == 'continue':
      Globals.current_user['warned'] = True
    elif a == 'login':
      Globals.current_user['warned'] = True
      self.titlebar_user_display.login_link_click()
  
  '''
  BINDING ACCESSORS
  '''
  def current_user(self, **event_args):
    return Globals.current_user
  def current_user_is_not_guest(self, **event_args):
    return Globals.current_user_is_not_guest()
  def cart_item_count(self, **event_args):
    return Globals.cart_quantity




  
  
  
  
  
  
  
  
  
  
  


