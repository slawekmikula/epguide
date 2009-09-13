

from sgmllib import SGMLParser
import time
import re

class WPParser(SGMLParser):
  def __init__ (s):
    SGMLParser.__init__ (s)
    s.state = []
    s.i = ""
    s.s_start ("HTML")

    s.channel = ""
    s.chanid = ""
    s.date = ""
    s.success = False

  def close (s):
    SGMLParser.close (s)
    s.channel = s.channel.decode("iso-8859-2", "replace").strip()
    s.chanid = re.sub("[^a-z0-9]", "", s.channel.lower())+".wp"
    s.s_end ("HTML")

  def get_attr (s, list, name):
    for attr in list:
      if attr[0] == name:
        return attr[1]
    return None

  def start_table(s, attrs):
    if s.state[-1] == "HTML" and s.get_attr (attrs, "class") == "drukowalne":
      s.s_start ("TABLE")
      s.s_start ("NAME")

  def end_table (s):
    if "TABLE" in s.state:
      s.s_end ("TABLE")

  def start_b (s, attrs):
    if s.get_attr (attrs, "class") == "ng":
      if s.state[-1] == "NAME":
        s.s_start ("name")
      elif s.state[-1] == "DATE":
        s.s_start ("date")
    elif s.state[-1] == "P_TIME":
      s.s_start ("p_time")
    elif s.state[-1] == "P_TITLE":
      s.s_start ("p_title")

  def end_b (s):
    if "name" in s.state:
      s.s_end ("name")
      s.s_switch ("DATE")
    elif "date" in s.state:
      s.s_end ("date")
      s.s_switch ("PROGRAMS")
      s.programs = []
    elif "p_time" in s.state:
      s.s_end ("p_time")
      s.s_switch ("P_TITLE")
    elif "p_title" in s.state:
      s.s_end ("p_title")
      s.s_switch ("P_DESC")

  def start_span (s, attrs):
    if s.get_attr (attrs, "class") == "SGinfo":
      if s.state[-1] == "P_DESC":
        s.s_start ("p_desc")

  def end_span (s):
    if "p_desc" in s.state:
      s.s_end ("p_desc")

  def start_tr (s, attrs):
    if s.state[-1] == "PROGRAMS":
      s.program = {'time' : "", 'title' : "", 'desc' : ""}
      s.s_start ("PROGRAM")
      s.s_start ("P_TIME")

  def end_tr (s):
    if "PROGRAM" in s.state:
      s.program['sub-title'] = ""
      s.program['cat'] = []
      s.programs.append (s.program)
      s.s_end ("PROGRAM")
      
  def handle_data (s, data):
    data = data.strip()
    if s.state[-1] == "name":
      s.channel = data
    elif s.state[-1] == "date":
      s.date = time.strptime (data[11:21], "%d.%m.%Y")
    elif s.state[-1] == "p_time":
      s.program['time'] = data
    elif s.state[-1] == "p_title":
      s.program['title'] = data
    elif s.state[-1] == "p_desc":
      s.success = True
      s.program['desc'] += data + "\n"

  def s_start (s, state):
    s.state.append (state)

  def s_end (s, state):
    i = 2
    while s.state.pop() != state:
      i += 2

  def s_switch (s, state):
    s.state[-1] = state
