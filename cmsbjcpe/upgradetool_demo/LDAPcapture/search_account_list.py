#!/usr/bin/python
#suppose the all DNs have been extracted
import ldap
import sys, ldif

def onelevel_dn_search(baseDN,ldap_conn):
  #ldap_result_id = ldap_conn.search(baseDN, ldap.SCOPE_ONELEVEL, "accountNumber=*1")
  ldap_result_id = ldap_conn.search(baseDN, ldap.SCOPE_ONELEVEL)
  result_set = []
  #ldif_writer=ldif.LDIFWriter(sys.stdout)

  #open ten files to write
  files=[]
  for i in range(10):
    files.append(open("account_child_"+str(i),"w"))

  index=0
  while 1:
    result_type, result_data = ldap_conn.result(ldap_result_id, 0)
    if (result_data == []):
      break
    else:
      if result_type == ldap.RES_SEARCH_ENTRY:
        #result_set.append(result_data)
        for entry in result_data:
          files[index].write(entry[0]+"\n")  
          index += 1
          if index >= 10:
            index=0
          #ldif_writer.unparse(entry[0],entry[1])

  #close all files
  for i in range(10):
    files[i].close()

if __name__ == '__main__':
  #main entry
  l = ldap.open("lijia",port=5005)
  l.protocol_version = ldap.VERSION3
  
  username = "cn=root"
  password = "secret"

  l.simple_bind(username,password)

  baseDN = "o=accounts"

  onelevel_dn_search(baseDN,l)
  l.unbind()

