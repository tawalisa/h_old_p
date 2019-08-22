#!/usr/bin/python
#suppose the all DNs have been extracted
import ldap
import sys, ldif, datetime


def dict2list(d):
  dictlist = []
  for key, value in d.iteritems():
    if key == "shawtelephonenumber":
      value = map(lambda foo: "+"+foo, value) 
    temp = (key,value)
    dictlist.append(temp)
  return dictlist

def sub_tree_search(baseDN,ldap_conn):
  #ldap_result_id = ldap_conn.search(baseDN, ldap.SCOPE_SUBTREE)
  ldap_result_id = ldap_conn.search(baseDN, ldap.SCOPE_BASE)
  result_set = []
  listdn = []
  dictdn = {}
  while 1:
    try:
      result_type, result_data = ldap_conn.result(ldap_result_id, 0)
      if (result_data == []):
        #listdn = sorted(listdn)
        #for d in listdn:
        #  print(d[::-1])
        #  print dict2list(dictdn[d])
        break
      else:
        if result_type == ldap.RES_SEARCH_ENTRY:
          for entry in result_data:
            listdn.append(entry[0][::-1])
            dictdn[entry[0][::-1]] = entry[1]
    except ldap.NO_SUCH_OBJECT:
      break
  return (listdn,dictdn)
def compareAttr(k,attr_source, attr_target):
  retu = []
  for v in attr_source:
    if v not in attr_target:
      retu.append((ldap.MOD_ADD, k, v))
  for v in attr_target:
    if v not in attr_source:
      retu.append((ldap.MOD_DELETE, k, v))
  return retu

def compareEntry(source_entry,target_entry):
  retu = []
  for k in source_entry.keys():
    if k in target_entry.keys():
      retu.extend(compareAttr(k,source_entry[k],target_entry[k]))
    else :
      for v in source_entry[k]:
        retu.append((ldap.MOD_ADD, k, v))
      pass
  for k in target_entry.keys():
    if k not in source_entry.keys():
      for v in target_entry[k]:
        retu.append((ldap.MOD_DELETE, k, v))
  return retu
def compareAndUpdateEntry(ldap_conn_target,dn,source_entry,target_entry):
  modify_entry = compareEntry(source_entry,target_entry)
  print("modify_entry",modify_entry)
  print("dn",dn)
  if len(modify_entry) > 0:
    ldap_conn_target.modify_s(dn,modify_entry)
  pass
def addEntry(ldap_conn_target,dn,source_entry):
  print("addEntry",dn,dict2list(source_entry))
  ldap_conn_target.add_s(dn,dict2list(source_entry))
  pass
def deleteEntry(ldap_conn_target,dn):
  print("deleteEntry",dn)
  ldap_conn_target.delete_s(dn)
  pass
def lowerDict(dic):
  retu = {}
  for k,v in dic.iteritems():
    retu[k.lower()] = v
  return retu
def sub_tree_compare(baseDN,ldap_conn,ldap_conn_target):
  (source_list_dn, sourece_entry_dict) = sub_tree_search(baseDN,ldap_conn) 
  (target_list_dn, target_entry_dict) = sub_tree_search(baseDN,ldap_conn_target)
  source_list_dn = map(lambda foo: foo.lower(),source_list_dn)
  target_list_dn = map(lambda foo: foo.lower(),target_list_dn)
  sourece_entry_dict = lowerDict(sourece_entry_dict)
  target_entry_dict = lowerDict(target_entry_dict) 
  #print (source_list_dn, sourece_entry_dict)
  #print (target_list_dn, target_entry_dict)
  print(target_list_dn) 
  print len(target_list_dn)
  for dn in sorted(source_list_dn):
    if dn in target_list_dn:
      compareAndUpdateEntry(ldap_conn_target,dn[::-1],lowerDict(sourece_entry_dict[dn]),lowerDict(target_entry_dict[dn]))
    else :
      addEntry(ldap_conn_target,dn[::-1],sourece_entry_dict[dn])
  for dn in sorted(target_entry_dict,reverse=True):
    if dn not in source_list_dn:
      deleteEntry(ldap_conn_target,dn[::-1])

if __name__ == '__main__':
  #main entry

  in_file = open(sys.argv[1],"r")
#source LDAP connection
  l = ldap.open("lijia.com",port=5005)
  l.protocol_version = ldap.VERSION3
  
  username = "cn=root"
  password = "secret"
#target LDAP connection
  l.simple_bind(username,password)
  l2 = ldap.open("lijia.com",port=5005)
  l2.protocol_version = ldap.VERSION3

  username = "cn=root"
  password = "secret"

  #l2.simple_bind(username,password)
  l2.simple_bind()

  for line in in_file:
    #hanlde each linei
    baseDN = line.split(":")[0]
    print baseDN
    sub_tree_compare(baseDN,l,l2)
  l.unbind()
  l2.unbind()

  #before close out file, output the date to out file
  in_file.close()

