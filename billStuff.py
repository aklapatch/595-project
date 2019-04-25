import xmltodict,json

# returns inputdict['resolution'] or inputdict['bill'] depending on which one exists
def get_alias_dict(input_dict):
  if 'resolution' in input_dict:
    return input_dict['resolution']
  
  elif 'bill' in input_dict:
    return input_dict['bill']

  elif 'amendment-doc' in input_dict:
    return input_dict['amendment-doc']

  return {}
#end def --------------------------------------

# returns members if the member exists in the dictionary
def get_str_if_there(input_dict,keyarr):
  try:
    if keyarr in input_dict:
      if isinstance(input_dict[keyarr],str):
        return  '\n' + input_dict[keyarr] + '\n'

    return ""
  except:
   return ""
#----------------------------------------------------------

# returns true if all the keys in string array are in the dict
# like such inputdict[stringarray[0]][stringarray[1]]....
# if stringarray is a string, 
def keyin(inputdict, stringarray):
  # iterate through the keys and see if they match
  tmp = inputdict

  if isinstance(stringarray,str):
    if stringarray in inputdict:
      return True
    else:
      return False

  try:
    for key in stringarray:
      if key in tmp:
        tmp = tmp[key]
      else:
        return False
  except TypeError:
    return False

  return True
#------------------------------------------------- 

# grabs every header and text and #text element 
# from section, subsections and other key names
# it is assuming that inputdict = hconres['resolution']['resolution-body']
def get_bill_text_and_headers(input_dict):
  # search current layer for text,#text, and header keys
  # concat to str

  outstr = ""
  tmp = input_dict

  if isinstance(tmp,str):
    return tmp

  # do something else if it is a list
  if isinstance(input_dict,list):
    for item in input_dict:
      outstr += get_bill_text_and_headers(item)

  outstr += get_str_if_there(tmp,'header')

  # text is sometimes a dict
  if 'text' in tmp:
    outstr += get_bill_text_and_headers(tmp['text'])
  else:
    outstr += get_str_if_there(tmp,'text')
  
  outstr += get_str_if_there(tmp,'#text')

# words to investigate are paragraph,section,subection, and text
# division, quoted-block

  try:
    for key in tmp.keys(): 
      if 'section' == key:
        outstr += get_bill_text_and_headers(tmp['section'])

      if 'paragraph' == key:
        outstr += get_bill_text_and_headers(tmp['paragraph'])

      if 'subsection' == key:
        outstr += get_bill_text_and_headers(tmp['subsection'])

      if 'division' == key:
        outstr += get_bill_text_and_headers(tmp['division'])

      if 'quoted-block' == key:
        outstr += get_bill_text_and_headers(tmp['quoted-block'])

      if 'quote' == key:
        outstr += get_bill_text_and_headers(tmp['quote'])
        # more recursion
        outstr += get_bill_text_and_headers(tmp[key])
  except:
    return outstr
  
  return outstr

def select_leg_date(alias):
  if keyin(alias,['attestation','attestation-group','attestation-date','@date']):
    return alias['attestation']['attestation-group']['attestation-date']['@date']
  
  elif keyin(alias,['endorsement','action-date','@date']):
    return alias['endorsement']['action-date']['@date']
  elif keyin(alias,['endorsement','action-date']):
    return alias['endorsement']['action-date']

  elif keyin(alias,['form','action']):
    if isinstance(alias['form']['action'],list):
      return alias['form']['action'][-1]['action-date']

    elif keyin(alias,['form','action','action-date','@date']):
      return alias['form']['action']['action-date']['@date']
    else:
      return alias['form']['action']['action-date']

  else:
    return alias['metadata']['dublinCore']['dc:date']
#-----------------------------------------------------------------

def get_text_body(alias):
  if 'legis-body' in alias:
    return get_bill_text_and_headers(alias['legis-body'])
  elif 'resolution-body' in alias:
    return get_bill_text_and_headers(alias['resolution-body'])
  else:
    return  get_bill_text_and_headers(alias['engrossed-amendment-body'])

def get_before_colon(string_in):
  dex = string_in.find(':')
  if dex > -1:
    return string_in[0:dex]
  else:
    return string_in

def select_leg_title(alias):
  if keyin(alias, ['metadata','dublinCore','dc:title']):
    return get_before_colon(alias['metadata']['dublinCore']['dc:title'])

  elif isinstance(alias['form']['official-title'],str): 
    return get_before_colon(alias['form']['official-title'])
  else:
    return get_before_colon(alias['form']['official-title']['#text'])

def reduce_s_dict(hconres):
  outputdict = {}

  alias = get_alias_dict(hconres)

  outputdict['title'] = select_leg_title(alias)

  outputdict['date'] = select_leg_date(alias)

  if keyin(alias,['engrossed-amendment-body','section','@section-type']):
    outputdict['status'] = alias['engrossed-amendment-body']['section']['@section-type']

  elif '@bill-stage' in alias:
    outputdict['status'] = alias['@bill-stage']
  
  else:
    outputdict['status'] = alias['@resolution-stage']
  
  if keyin(alias,['form','action','action-desc','sponsor','#text']):
    outputdict['sponsors'] = alias['form']['action']['action-desc']['sponsor']['#text']

  elif keyin(alias,['attestation','attestation-group','attestor','#text']):
    outputdict['sponsors'] = alias['attestation']['attestation-group']['attestor']['#text']

  outputdict['text'] = get_text_body(alias)

  return outputdict
#--------------------------------------------------

def dumptojson(inputdict,fname):
  with open(fname,'w') as fp:
    json.dump(inputdict,fp)

# testing starts here -----------------------------------------------------------------------------