import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import app



def permit_dict(user_row):
  # used to generate a cachable dict that only contains permitted parameters
  permitted = ['enabled', 'email', 'villagers', 'warned']
  # not permitted: 'remembered_logins', 'last_login', 'username', 'password_hash', 'signed_up'
  return dict(filter(
    lambda key_value: key_value[0] in permitted,
    dict(user_row).items()
  ))

@anvil.server.callable
def auto_login():
  print('WARNING WARNING WARNING')
  print('UserController signed in a user')
  print('WARNING WARNING WARNING')
  if anvil.app.branch == 'published':
    raise PermissionError("If you're seeing this, please let ben.j.etherington@gmail.com know he's a moron." )
  default_user = app_tables.users.get(email='zoundspadang@gmail.com')
  anvil.users.force_login(default_user)
  return permit_dict(default_user)

@anvil.server.callable
def assign_villager(villager, remove_from_profile):
  '''
  Called by the settings page, letting us know the user wants to add or remove a villager
  from their profile. villager can be a row or a string, remove_from_profile is a bool.
  Returns user data so the client cache can get updated
  '''
  if isinstance(villager, str):
    villager_row = app_tables.villagers.get(name=villager)
  else:
    villager_row = villager
  user = anvil.users.get_user()
  if remove_from_profile:
    # remove villager association by rebuilding the association list
    user['villagers'] = [v for v in user['villagers'] if v != villager_row]
  else:
    # add villager association using a set for uniqueness
    user['villagers'] = list(set( user['villagers']+[villager_row] ))
  return permit_dict(user)

@anvil.server.callable
def init_user_cache():
  '''
  Called on successful login to cache some data about the user, and on logout to set guest dict
  '''
  current_user = anvil.users.get_user()
  current_user['villagers'] = sorted(current_user['villagers'], key=lambda v: v['name'])
  if current_user:
    cart_quantity = anvil.server.call('count_gifts')
  else:
    current_user = {'email': 'Guest',
                    'villagers': [],
                    'warned': False}
    cart_quantity = None
  return permit_dict(current_user), cart_quantity












