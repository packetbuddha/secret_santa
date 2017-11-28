#!/usr/bin/env python

# Author: Carl Tewksbury
# Last Update: 2017-11-26

import random
import yaml
from collections import OrderedDict
from datetime import date

class SecretSanta(object):

    def __init__(self, santa_config='santas.yml', debug=False, write=False, email=False):
        self.santas_config = santa_config
        self.couples = self.load_config()
        self.debug = debug
        self.write = write
        self.email = email
        d = date.today()
        self.year = d.year

    def badmatch(self, elves, santa, pick):
        """Santa can't pick themselves or anyone in their immediate family
        (param couples)

        Args:
           couples (list): list of tuples, each containing persons who should
           not be matched together
        ]
        Returns:
            True if is bad match, False otherwise
        """

        for couple in self.couples:
            if ((santa in couple) and (pick in couple)):
                return True    
        return

    def deadend(self, couples, hat, santa, pick):
        """ Detect dead ends - a badmatch() is the only available pick """ 
    
        if (len(hat) <= 2) and (self.badmatch(couples, santa, pick)):
            print "only", len(hat), "left:", hat
            return True
        else:
            return
    
    def pickfromthehat(self, couples, secretsantas, hat, santa):
        """ randomly select from the hat and check if its a good pick """

        pick = random.choice(hat)
        print "santa picked", pick
        if self.deadend(couples, hat, santa, pick):
            return ("deadend")    
        elif self.badmatch(couples, santa, pick):
            return ("badmatch")
        else:
            hat.remove(pick)
            print "looks good, man! I removed", pick, "from the hat!"
            return pick
    
    def playsecretsanta(self, couples, secretsantas, hat):
        """Wrapper for picking function to deal with the results; such as
           dead ends resulting in the need to start the game over again
        """

        for santa, pick in secretsantas.iteritems():
            santaschoice = False
            while santaschoice == False:
                print "santa is", santa
                mypick = self.pickfromthehat(couples, secretsantas, hat, santa)
                if mypick == "deadend":
                    print "crap, deadend!"
                    return True
                elif mypick == "badmatch":
                    print "crap, bad match!"
                    continue
                elif mypick:
                    print "adding match...", santa, "->", mypick
                    secretsantas[santa] = mypick
                    santaschoice = True
        return False
    
    def makefiles(self, secretsantas):    
        for santa, pick in secretsantas.iteritems():
            message = '{0} is secret santa for: {1} '.format(santa, pick)
            santaf = '/tmp/{0}_SecretSanta-{1}.txt'.format(santa, self.year)

            with open(santaf, 'w+') as f:
              f.write(message)
   
    def load_config(self):
        with open(self.santas_config, 'r') as f:
            return yaml.load(f)

    def run(self):
        keepplaying = True
        while keepplaying:
            
            if self.debug:
              print self.couples 

            hat = []        
            secretsantas = OrderedDict()
    
            # Create list of santas and the hat using couples data
            for couple in self.couples:
                for santa in couple:
                    if santa != "Mischief":
                        secretsantas[santa] = None
                        hat.append(santa)
    
            keepplaying = self.playsecretsanta(self.couples, secretsantas, hat)

            if self.debug:
                print secretsantas

            # Each time we play again, we reinitialize our elves data 
            if keepplaying:
                self.couples = self.load_config()
            
        if self.write:
            self.makefiles(secretsantas)
        if self.email:
            from email import email
            e = email()

        return secretsantas
