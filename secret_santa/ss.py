#!/usr/bin/env python

'''
To Do:
------

- move child matches into couples dictionary as new key; results to include 
  couples dict so email addy and match are avail

'''

import secret_santa

<<<<<<< HEAD
ss = secret_santa.SecretSanta(email=False, write=True, debug=True)
matches = ss.run()

print(matches)
=======
ss = secret_santa.SecretSanta(write=True, debug=True)
r = ss.run()
>>>>>>> f22222bc1ac95ec84bce8a88e275b7c25247a808


