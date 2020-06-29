import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import tables
from tables import app_tables
import anvil.server

@anvil.server.callable()
def get_all_items():
  return app_tables.items.search()

@anvil.server.callable
def get_item_name_list():
  non_unique_names = [r['name'] for r in app_tables.items.search()]
  unique_names = list(set(non_unique_names))
  return unique_names

@anvil.server.callable
def get_item_details(item_name, user):
  '''
  Called when an item is selected from the search. This code prioritizes readability over number of lines.
  Returns a dict that looks like:
  {
    "style": "cool",
    "all_colors": [item_row, item_row],
    "matches": [ {'villager': villager_row, 'items': [item_row, item_row], 'purchased_on': 'date'}, ...]
  }
  '''
  # non-lazily, find all item rows that have this name
  items = list( app_tables.items.search(name=item_name) )
  # item style is parsed out for the browser, and all items of the same name share the same style
  item_style = items[0]['style']
  # build a list of associated villager rows, or an empty list (None is not helpful here)
  villagers = user['villagers'] or []
  # build a list of villagers and which items they like, ignoring villagers that don't match
  matches = []
  for villager in villagers:
    # CHECK FOR MATCHES
    matching_items = []
    for item in items:
      if item_matches_villager(item, villager):
        matching_items.append(item)
    if len(matching_items) == 0:
      continue
    # LOOK FOR PREVIOUS GIFTS
    existing_gifts = app_tables.gifts.search(tables.order_by('updated_on'),
                                             villager=villager,
                                             item=q.any_of(*items))
    if len(existing_gifts) > 0:
      # this villager has already received this gift
      purchase_date = '{dt.month}/{dt.day}'.format(dt=existing_gifts[0]['updated_on'])
    else:
      purchase_date = ''
    # SAVE THE DATA
    matches.append({'villager': dict(villager), 'items':matching_items, 'purchased_on':purchase_date})
  return {'style':item_style, 'all_colors':items, 'matches':matches}
          
def item_matches_villager(item, villager):
  '''
  Checks whether a villager and item share at least one style and at least one color.
  FYI, & is the equivalent of s.intersection(t).
  '''
  i_styles = [item['style']]
  i_colors = [item['color1'], item['color2']]
  v_styles = [villager['style1'], villager['style2']]
  v_colors = [villager['color1'], villager['color2']]
  color_match = bool(set(v_colors) & set(i_colors))
  style_match = bool(set(v_styles) & set(i_styles))
  return color_match and style_match

        
  
 
  
   
    
    
    
    
    