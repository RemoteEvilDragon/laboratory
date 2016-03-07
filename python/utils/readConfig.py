#!/usr/bin/env python

fi = open(sys.argv[1], "r")
fo = open("output.config","w+")

for line in fi.readlines():
	if line[:1] != "#":
		fo.write(line+"\n")

# Close opend file
fi.close()

fo.close()

# 2016/03/05 02:43:32| WARNING: (A) '192.168.1.0/24' is a subnetwork of (B) '192.168.0.0/16'
# 2016/03/05 02:43:32| WARNING: because of this '192.168.1.0/24' is ignored to keep splay tree searching predictable
# 2016/03/05 02:43:32| WARNING: You should probably remove '192.168.1.0/24' from the ACL named 'localnet'