import urllib2, cookielib, json, re, logging
from urllib import urlencode
SITE="http://fluttr.heroku.com"

# Create a logger (Lots more logging could be added to this codebase if necessary)
log = logging.getLogger("fluttr-cli")
log.setLevel(logging.WARN)
ch = logging.StreamHandler()
ch.setLevel(logging.WARN)
ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
log.addHandler(ch)

class Fluttr(object):
  """An object oriented interface to the fluttrly application. This class
  encapsulates a to-do list on fluttr.heroku.com, and gives simple programatic
  access to list, add, and remove items. """
  def __init__(self, name):
    self.name = name
    self._items = None
    self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

  def __iter__(self):
    return iter(self.items)

  def __getitem__(self, i):
    return self.items[i]

  def _get_items(self):
    if not self._items: self.refresh()
    return self._items
  def _set_items(self, items):
    self.items = items
  items = property(_get_items, _set_items, None, "Items in the to-do list")

  def _get_auth_token(self):
    url = "%s/%s" %(SITE, self.name)
    data = self._opener.open(url).read()
    auth_token = re.search(r'name="authenticity_token".*value="(.+)"', data).group(1)
    log.debug("Got auth token: %s" % auth_token)
    return auth_token
  auth_token = property(_get_auth_token,
                        lambda x: x,
                        "Magically creates a valid authenticity_token")

  def __str__(self):
    if len(self.items) < 1:
      return "Nothing to do!"
    else:
      return "\n".join(("%d) %s" % (i+1, task) for i, task in enumerate(self)))

  def refresh(self):
    """Updates the list of items.  This function is called implicitly if the
    list doesn't exist, but can be called manually to ensure a fresh list."""
    url = "%s/%s.json" % (SITE, self.name)
    log.debug("fetching list from url '%s'" % url)
    raw_data = json.loads(self._opener.open(url).read())
    self._items = [ Task(x['task']) for x in raw_data ]

  def add(self, content):
    """Add an item to the list. Invalidates cached list."""
    url = "%s/tasks" % SITE
    params = urlencode({ "task[name]": self.name, "task[content]": content, "authenticity_token": self.auth_token })
    res = self._opener.open(url, params).read()
    log.debug("Item added")
    self._items = None # Invalidate cache

  def remove(self, indices):
    for index in indices:
      self.items[index].destroy()
    self._items = None # Invalidate cache

class Task(object):
  def __init__(self, data_hash):
    self.id = data_hash["id"]
    self.name = data_hash["name"]
    self.content = data_hash["content"]
    self._completed = data_hash["completed"]
    self.created_at = data_hash["created_at"]
    self.updated_at = data_hash["updated_at"]
    self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

  def _get_auth_token(self):
    url = "%s/%s" %(SITE, self.name)
    data = self._opener.open(url).read()
    auth_token = re.search(r'name="authenticity_token".*value="(.+)"', data).group(1)
    log.debug("Got auth token: %s" % auth_token)
    return auth_token
  auth_token = property(_get_auth_token, lambda x: x, "Magically creates a valid authenticity_token")

  def toggle(self):
    self.completed = not self.completed

  def destroy(self):
    """Remove an item from the list. Invalidates cached list."""
    url = "%s/tasks/%d" % (SITE, self.id)
    params = urlencode({ "_method": "delete", "_": "",
                         "authenticity_token": self.auth_token })
    res = self._opener.open(url, params).read()
    log.debug("Item removed")
    self._items = None # Invalidate cached items

  def __repr__(self):
    return '<Fluttr Task: "%s">' % self.content

  def _get_completed(self):
    return self._completed
  def _set_completed(self, value):
    if not self._completed == value:
      url = "%s/tasks/%d" % (SITE, self.id)
      params = urlencode({ "_method": "put", "_": "",
                           "completed": str(value).lower(),
                           "authenticity_token": self.auth_token })
      res = self._opener.open(url, params).read()
      log.debug("Item updated")
    self._completed = value
  completed = property(_get_completed, _set_completed, "Whether this item is completed (i.e. crossed off)")

  def _get_completion_x(self):
    """This is just for the status in __str__. You're probably looking for 'completed'."""
    if self.completed: return "X"
    else:              return " "
  completion_x = property(_get_completion_x)

  def __str__(self):
    return '[%s] %s' % (self.completion_x, self.content)
