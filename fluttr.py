#!/usr/bin/env python
import sys
from fluttr import Fluttr

def add_task(f, args):
  """Add a task to a fluttr list"""
  content = " ".join(args)
  f.add(content)

def _fix(it):
  """Turns 1-based string indexes into 0-based integer indexes."""
  return int(it) - 1

def remove_tasks(f, args):
  """Remove tasks from a fluttr list. Takes a Fluttr object and a list of
     1-based string indices."""
  try:
    for i in map(_fix, args):
      f[i].destroy()
  except:
    print "At least one of the things you tried to remove didn't exist. Please"+\
          " specify the number of an item that is actually in your list.\n"
  finally:
    # Refresh list, now that we've removed some. 
    f.refresh()

def toggle_completion(f, args):
  """Toggle a task's completion status. Takes a Fluttr object and a list of
     1-based string indices."""
  try:
    for i in map(_fix, args):
      f[i].toggle()
  except:
    print "Some of the things you tried to toggle didn't exist. Please"+\
          " specify the number of an item that is actually in your list.\n"


def usage():
  """Print usage information for this command line interface"""
  print "Usage: fluttr <list>\n" + \
        "       fluttr <list> add <item>\n" + \
        "       fluttr <list> toggle <index> [<index2> <index3> ...]\n" + \
        "       fluttr <list> rm <index> [<index2> <index3> ...]"



if __name__ == "__main__":
  args = sys.argv[1:]
  commands = { "add": add_task,
               "del":  remove_tasks,
               "create": add_task,
               "remove":  remove_tasks,
               "rm":  remove_tasks,
               "toggle": toggle_completion }

  # Special case for default listing behavior
  if len(args) == 1:
    f = Fluttr(args[0])
    print f

  # A command, and potentially some arguments to it
  elif len(args) >= 2:
    f = Fluttr(args[0])
    command = args[1]
    if command in commands:
      commands[command](f, args[2:])
      print f
    else: # Command name we don't recognize; give them usage.
      usage()

  # Catchall "we didn't understand you", so we give them usage. 
  else:
    usage()
