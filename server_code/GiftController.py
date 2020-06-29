import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .ItemController import item_matches_villager
from datetime import datetime

"""
GETTERS
"""
@anvil.server.callable
def count_gifts():
  # used to populate "continue to shopping cart (#)" buttons
  return len( app_tables.gifts.search(user=anvil.users.get_user(), delivered=False) )
@anvil.server.callable
def get_gifts(status):
    '''
    Called by shopping cart form. Status and villagers are strings that filter the returned value.
    Status can be: 'neither', 'not_delivered', and 'all'.
    Returns something like:
    [
      {
        "name":"villager_name",
        "icon_image":"URL",
        "preferences":"style, style, color, color",
        "gifts": [ {'selected': gift_dict, 'all_others': [item_row, item_row]}, ...]
      }
    ]
    '''
    # set queries based on filter dropdown
    if status == 'neither':
      search_filters = q.any_of(purchased=False, delivered=False)
    elif status == 'not_delivered':
      search_filters = q.all_of(purchased=True, delivered=False)
    elif status == 'all':
      search_filters = q.any_of(purchased=q.any_of(True, False)) # ugh anvil is there no empty query object?
    else:
      raise ValueError('Search filters were invalid!')
    # search the database, digest the info
    return_data = []
    villager_list = anvil.users.get_user()['villagers']
    for villager in villager_list:
      # Find all gifts that belong to the villager and fit the filter dropdown
      v_gifts = app_tables.gifts.search(search_filters, villager=villager, user=anvil.users.get_user())
      # short-circuit if no gifts remain
      if not len(v_gifts) > 0:
        return_data.append({
          'name': villager['name'],
          'icon_image': villager['icon_image'],
          'preferences': f"{villager['style1']}, {villager['style2']}, {villager['color1']}, {villager['color2']}",
          'gifts': []
        })
        continue
        
      # find this gift's item, find all other items with the same name, filter by match with the villager
      v_gifts_enriched = []
      for gift in v_gifts:
        item = gift['item']
        other_items = [ i for i in app_tables.items.search(name=item['name']) if i != item]
        other_matching_items = [i for i in other_items if item_matches_villager(i, villager)]
        v_gifts_enriched.append({'selected':gift, 'all_others': other_matching_items})
        
      # add this villager, this gift, and alternate variations to the return data
      return_data.append({
        'name': villager['name'],
        'icon_image': villager['icon_image'],
        'preferences': f"{villager['style1']}, {villager['style2']}, {villager['color1']}, {villager['color2']}",
        'gifts': v_gifts_enriched
      })
   
    # once we've finished going through all the villagers, sort and send the data back.
    return_data = sorted(return_data, key=lambda i: len(i['gifts'])==0)
    return return_data

  
  
"""
SETTERS
"""
  
@anvil.server.callable
def assign_gifts(villager_items):
  '''
  Called by VillagerLikeDisplay when the user adds gifts to the cart.
  villager_items is a list that looks like:
  [ {'villager': villager_dict, 'item': item_row}, ...]
  '''
  user = anvil.users.get_user()
  for villager_item in villager_items:
    villager = app_tables.villagers.get(name=villager_item['villager']['name'])
    app_tables.gifts.add_row(user=user,
                             villager=villager,
                             item=villager_item['item'],
                             delivered=False,
                             purchased=False,
                             updated_on=datetime.now())   
@anvil.server.callable
def update_gift_status(gift, purchased, delivered):
  gift.update(purchased=purchased, delivered=delivered, updated_on=datetime.now())
@anvil.server.callable
def update_gift_item(gift, new_item):
  gift.update(item=new_item, updated_on=datetime.now())
@anvil.server.callable
def delete_gift(gift):
  gift.delete()
















