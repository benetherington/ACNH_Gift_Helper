from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # set class variables and events
    self.edit = False
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # init data
    if Globals.current_user_is_guest():
      self.your_villagers = Globals.current_user['villagers']
    else:
      self.your_villagers = anvil.server.call('get_user_villagers')
    # init UI (further updates happen in first form_refreshing_data_bindings)
    self.your_villagers_display.item = Globals.current_user['villagers']
    # set event handlers
    self.set_event_handler('x-your-villagers-removed', self.your_villagers_removed)
    self.set_event_handler('x-all-villagers-changed', self.all_villagers_changed)
    
    # TODO: warn guests that their selections won't get pushed into a new account
    
  '''
  EVENT HANDLERS
  '''
  def your_villagers_removed(self, **event_args):
    # pass through from YourVillagersTemplate
    self.all_villagers_repeating_panel \
      .raise_event_on_children('x-your-villagers-removed', **event_args)
  def all_villagers_changed(self, **event_args):
    # pass through from AllVillagersTemplate (with some extra logic)
    if event_args['removed']:
      # if a villager was un-selected, we can just delete their panel
      self.your_villagers_display\
        .raise_event('x-all-villagers-changed', **event_args)
    else:
      # if a new villager was selected, we need to go get their details.
      self.update_your_villagers()
      # if this event was raised, we're in edit mode.
      self.your_villagers_display.raise_event('x-enable-remove-button', **event_args)
  
  '''
  UTILITIES
  '''
  def villagers_enriched(self, display_list=None, **event_args):
    '''
    A function that builds data to populate AllVillagersDisplay. AVDisplay shows a segment of
    the large number of total villagers with an accordion titlebar, so that we don't have to
    render every single AllVillagersTemplate at the same time, which is slowwwww. This function
    takes a list of villager cache dicts (containing name and icon_image), and splits them up
    by the first letter of their name. It returns a list of segment "lists" with villager dicts.
    All this looks like:
    [ # handed to all_villagers_repeating_panel
      { # handed to AllVillagersDisplay
        range: 'A B',
        'segment': [ # handed to AllVillagersTemplate
          { "selected": True, "villager": {'name':'', 'icon_image':''} }, ...
        ]
      }, ...
    ]
    '''
    if display_list == None:
      display_list = Globals.all_villagers_dict_list
    # This distribution of letter segments results in no more than 40 villagers in each
    # segment. Most have around 25-30, but there are a lot of Cs and Bs. There's probably
    # a better distribution, but this works and is fast enough.
    enriched_list = [
      {'range': 'A', 'segment': []},
      {'range': 'B', 'segment': []},
      {'range': 'C', 'segment': []},
      {'range': 'DE', 'segment': []},
      {'range': 'FG', 'segment': []},
      {'range': 'HIJ', 'segment': []},
      {'range': 'KL', 'segment': []},
      {'range': 'HIJ', 'segment': []},
      {'range': 'KL', 'segment': []},
      {'range': 'M', 'segment': []},
      {'range': 'NOP', 'segment': []},
      {'range': 'QR', 'segment': []},
      {'range': 'S', 'segment': []},
      {'range': 'TUV', 'segment': []},
      {'range': 'WXYZ', 'segment': []}
    ]
    for v in display_list:
      # check if this villager is selected, build the dict for AllVillagersTemplate
      villager_dict = { 'selected': (v['name'] in Globals.current_user_villager_names()),
                       'villager': v}
      # put this dict into the right segment
      villager_initial = v['name'][0]
      for i,  segment in enumerate(enriched_list):
        if villager_initial in segment['range']:
          segment_index = i
          break
      enriched_list[segment_index]['segment'].append(villager_dict)
    # remove empty segments
    for segment in enriched_list:
      if len(segment['segment'])==0:
        enriched_list.remove(segment)
    return enriched_list
  
  def update_select_buttons(self, **event_args):
    if self.edit:
      self.your_villagers_display.raise_event('x-enable-remove-button')
      self.all_villagers_repeating_panel.raise_event_on_children('x-enable-select-button')
    else:
      self.your_villagers_display.raise_event('x-disable-remove-button')
      self.all_villagers_repeating_panel.raise_event_on_children('x-disable-select-button')
  def update_your_villagers(self, **event_args):
    self.your_villagers_display.item = Globals.current_user['villagers']
    #TODO: use data binding?

  '''
  UI
  '''
  def edit_button_click(self, **event_args):
    # toggle edit mode
    self.edit = not self.edit
    if self.edit:
      self.edit_button.role = 'primary-color'
    else:
      self.edit_button.role = 'raised'
    self.update_select_buttons()
  def search_text_box_change(self, **event_args):
    # This is super slow when loading all names, or even a partial list that matches
    # one or two letters. An alternative would be displaying a partial list, perhaps
    # with a row of first letters down one side to allow pulling up a subset of names.
    # A quick analysis shows ['AB', 'CD', 'EFGH', 'IJKLM', 'NOPQ', 'RS', 'TUVWXYZ']
    # has a relatively even distribution of villagers in each group. :shrug:
    # search for the string
    search_string = self.search_text_box.text
    if search_string == '':
      # an empty box should return all villagers
      self.all_villagers_repeating_panel.items = self.villagers_enriched()
      self.update_select_buttons()
      return
    # TODO implement https://en.wikipedia.org/wiki/Trie#A_Python_version?
    search_results = [i for i in Globals.all_villagers_dict_list
                      if search_string.lower() in i['name'].lower()]
    # set UI elements
    enriched = self.villagers_enriched(search_results)
    self.all_villagers_repeating_panel.items = enriched
    # if the entire list is short enough to display quickly, expand the accordions
    if len(search_results) < 10:
      self.expand_button_click()
    self.update_select_buttons() 
  def search_text_box_pressed_enter(self, **event_args):
    # if just one villager matches the search, select or un-select it
    if len(self.all_villagers_repeating_panel.items) == 1:
      self.all_villagers_repeating_panel.raise_event_on_children('x-ur-a-winner-baby')
  def expand_button_click(self, **event_args):
    self.all_villagers_repeating_panel.raise_event_on_children('x-expand-all')
  def collapse_button_click(self, **event_args):
    self.all_villagers_repeating_panel.raise_event_on_children('x-collapse-all')

  
  # SIDEBAR
  def selector_button_click(self, **event_args):
    open_form('GiftSelector')
  def cart_button_click(self, **event_args):
    open_form('ShoppingCart')  
  def about_button_click(self, **event_args):
    open_form('About')
  
  
  '''
  BINDING ACCESSORS
  '''
  def cart_item_count(self, **event_args):
    return Globals.cart_quantity
  def current_user_is_not_guest(self, **event_args):
    return Globals.current_user_is_not_guest()

  '''
  DATA BINDING
  '''
  def form_refreshing_data_bindings(self, **event_args):
    # no data bindings are used in this form, however, data bindings are refreshed on
    # form load and user changes, so this is a handy way to init/refresh UI elements
    self.update_your_villagers()
    self.search_text_box_change()







  


