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

def sub_tree_search(baseDN,ldap_conn,ldap_conn_target):
  ldap_result_id = ldap_conn.search(baseDN, ldap.SCOPE_SUBTREE)
  result_set = []
  listdn = []
  dictdn = {}
  while 1:
    result_type, result_data = ldap_conn.result(ldap_result_id, 0)
    if (result_data == []):
      listdn = sorted(listdn,key=lambda s: s.lower())
      for d in listdn:
        print(d[::-1])
        print dict2list(dictdn[d])
        ldap_conn_target.add_s(d[::-1],dict2list(dictdn[d]))
      break
    else:
      if result_type == ldap.RES_SEARCH_ENTRY:
        for entry in result_data:
          listdn.append(entry[0][::-1])
          dictdn[entry[0][::-1]] = entry[1]


if __name__ == '__main__':
  #main entry

  in_file = open(sys.argv[1],"r")

  l = ldap.open("lijia.com",port=5005)
  l.protocol_version = ldap.VERSION3
  
  username = "cn=root"
  password = "secret"

  l.simple_bind(username,password)
  l2 = ldap.open("lijia.com",port=5005)
  l2.protocol_version = ldap.VERSION3

  username = "cn=root"
  password = "secret"

  #l2.simple_bind(username,password)
  l2.simple_bind()

  for baseDN in in_file:
    #hanlde each line
    sub_tree_search(baseDN,l,l2)
  l.unbind()
  l2.unbind()

  #before close out file, output the date to out file
  in_file.close()

