#!/usr/bin/env python3

"""
  sct-production-hosts

  Checks which sct hosts (dvssct[0-14]) are currently used in production, meaning
  scientific cumputing is running.

  Copyright: 2015 Johannes Lauinger
"""

import subprocess


hosts = [ "dvssct00", "dvssct01", "dvssct03", "dvssct05","dvssct06",
   "dvssct07", "dvssct08", "dvssct09", "dvssct10", "dvssct11", "dvssct12", "dvssct13", "dvssct14" ]

needles = [ "qemu-system", "VBoxHeadless", "VBoxSvc", "rserver", "java" ]


safehosts = []

for host in hosts:
  print ("%s:" % host)
  safe = True

  haystack = subprocess.check_output("ssh %s ps aux" % host, shell=True).splitlines()

  for haybail in haystack:
    haybail = str(haybail)

    for needle in needles:
      if not needle in haybail: continue

      user = haybail[2:].split(" ")[0]

      safe = False
      print ("  found %s, run by %s" % (needle, user))

  if safe:
    safehosts.append(host)
    print ("  safe: no production processes found.")


print ("\nExecutive summary: safe hosts are: ", end="")
for host in safehosts:
  print ("%s " % host, end="")
print ()

