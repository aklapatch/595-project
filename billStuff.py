import requests, xmltodict
import json

#from mongoWrapper import *

def getXMLfrom(URL):
  response = requests.get(URL)
  return xmltodict.parse(response.content)
# ----------------------------------------------

# returns inputdict['resolution'] or inputdict['bill'] depending on which one exists
def getAliasDict(inputdict):
  if 'resolution' in inputdict:
    return inputdict['resolution']
  
  elif 'bill' in inputdict:
    return inputdict['bill']
  
  return {}
#end def --------------------------------------

# returns members if the member exists in the dictionary
def concatif(inputdict,keystr):
  strin = ""

  if isinstance(inputdict, list):
    for subdict in inputdict:
      if isinstance(subdict,dict):
        strin += getTextAndHeader(subdict)

      else:
        strin+= '\n' + subdict[keystr] + '\n'

  elif keystr in inputdict[keystr]:
    strin += '\n' + inputdict[keystr] + '\n'
  return strin
#----------------------------------------------------------

# input the dict['section'] and if there is a subsection, it will grab all the members
# that have a 'header' or '#text' member
def getbilltext(inputdict):

  # grab the header
  billtext = ""
  if 'header' in inputdict:
    billtext += '\n' + inputdict['header'] + '\n'

  # concat subsections
  for sec in inputdict['subsection']:
    
    billtext += '\n' + sec['header'] + '\n'
    billtext += sec['#text'] + '\n'

  return billtext
#---------------------------------------------------------------

# reduces a dictionary from the govinfo xml so that it fits our schema
def reduceDict(inputdict):
  # the top member is named 'resolution' or 'bill'
  outputdict = {}

  # if  the upper layer is resolution
  if inputdict['resolution']:
    # get the name
    alias = inputdict['resolution']
    outputdict['title'] = alias['metadata']['dublinCore']['dc:title']

    # if there are multiple sections in the bil
    if 'subsection' in alias['resolution-body']['section']:
      bill_sections = alias['resolution-body']['section']['subsection']

      # get and concat all bill text
      bill_text = ""
      for subsection in bill_sections:
        # add \n's for headers
        bill_text += '\n' + subsection['header'] + '\n'

        if (not isinstance(subsection['text'], str)):
          bill_text += subsection['text']['#text'] + '\n'

        else:
          bill_text += subsection['text'] + '\n'

        # end block
      outputdict['text'] = bill_text

      # end for
    #end if
    else: # no subsections to go through
      outputdict['text'] = alias['resolution-body']['section']['text']

    outputdict ['sponsors'] = inputdict['resolution']['form']['action']['action-desc']['sponsor']['#text']

    outputdict['description'] = inputdict['resolution']['form']['official-title']

    outputdict['status'] = inputdict['resolution']['@resolution-stage']

  # end if

  return outputdict
#------------------------------------------------------

# returns true if all the keys in string array are in the dict
# like such inputdict[stringarray[0]][stringarray[1]]....
def keyin(inputdict, stringarray):
  # iterate through the keys and see if they match
  tmp = inputdict

  try:
    for key in stringarray:
      if key in tmp:
        tmp = tmp[key]
      else:
        return False
  except TypeError as err:
    return False

  return True
#------------------------------------------------- 

# checks the section below for a header and #text and concat and return those
def getTextAndHeader(inputdict):
  outstr = ""
  if 'header' in inputdict:
    if isinstance(inputdict['header'],dict):
      outstr += inputdict['header']['#text']
    else:
      outstr += '\n' + inputdict['header'] + '\n'
    
  if 'text' in inputdict:
    if '#text' in inputdict['text']:
      outstr += inputdict['text']['#text'] + '\n'
    
  if '#text' in inputdict:
    outstr += inputdict['#text']
  
  return outstr


# currently skips amendments
def reducehconres(hconres):
  outputdict = {}
  alias = {}

  keystr = ""
  if 'resolution' in hconres:
    alias = hconres['resolution']
    keystr = 'resolution'

  elif 'amendment-doc' in hconres:
    keystr = 'amendment-doc'
    alias = hconres['amendment-doc']
    return

  if keyin(alias, ['title-amends','official-title-amendment']):
    outputdict['title'] = alias['title-amends']['official-title-amendment']

  else:
    outputdict['title'] = alias['form']['official-title']['#text']

  if 'dc:date' in alias['metadata']['dublinCore']:
    outputdict['date'] = alias['metadata']['dublinCore']['dc:date']

  elif 'action' in alias['form']:
    outputdict['date'] = alias['form']['action']['action-date']

  elif 'attestation-group' in alias:
    outputdict['date'] = alias['attestation']['attestation-group']['attestation-date']['@date']

  if keyin(alias,['engrossed-amendment-body','section','@section-type']):
    outputdict['status'] = alias['engrossed-amendment-body']['section']['@section-type']

  else:
    outputdict['status'] = alias['@resolution-stage']
  

  if keyin(alias,['form','action','action-desc','sponsor','#text']):
    outputdict['sponsors'] = alias['form']['action']['action-desc']['sponsor']['#text']

  elif keyin(alias,['attestation','attestation-group','attestor','#text']):
    outputdict['sponsor'] = alias['attestation']['attestation-group']['attestor']['#text']

  billtext = ""
  # get bill text
  if keyin(alias,['resolution-body','section','subsection']):
    
    # foreach through all of the subsections
    for sec in alias['resolution-body']['section']['subsection']:
      billtext += '\n' + sec['header'] + '\n'
      if (isinstance(sec['text'],str)):
        billtext += sec['text']
      else:
        billtext += sec['text']['#text'] + '\n'

  else:
    billtext = concatif(alias['resolution-body']['section'],'text')

  outputdict['text'] = billtext

  return outputdict
#-----------------------------------------------------------------

def dumptojson(inputdict,fname):
  with open(fname,'w') as fp:
    json.dump(inputdict,fp)

# testing starts here -----------------------------------------------------------------------------
'''
hjres = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/hjres/BILLS-116hjres10ih.xml")


s = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/s/BILLS-116s1000is.xml")


hconres = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/hconres/BILLS-116hconres10ih.xml")
print(reducehconres(hconres))


hr = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/hr/BILLS-116hr1000ih.xml")


hres = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/hres/BILLS-116hres100ih.xml")

sconres = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/sconres/BILLS-116sconres10is.xml")

sjres = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/sjres/BILLS-116sjres10is.xml")

sres = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/sres/BILLS-116sres100ats.xml")
'''