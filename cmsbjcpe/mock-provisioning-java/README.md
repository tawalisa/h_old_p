# go to project root

'cd cmsbjcpe/mock-provisioning-java'

# (optional)change yourself certificate 
you need overwrite file cert/ca.cert.pem 

# Build image

`sh build.sh`

# Run docker

'sh run.sh'

# (optional)if you want to change UIR host and port

you can eidt code/Test.java

`vi Test.java`

change 46 line

`LDAPConnection connection = new LDAPConnection("lijiatest", 1389);`

compile code

`javac Test.java`

# Run test

'sh run.sh'

