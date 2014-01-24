#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

class Person:
    def __init__(self, i):
        self._id = i
        self._affianced = None
        return

    def set_preference(self, people, preference = None):
        if preference == None:
            # generate preference randomly from people
            random.shuffle(people)
            self._preference = people
        else:
            self._preference = preference
        return self._preference
    def get_preference(self,):
        return self._preference

    def is_free(self):
        return self._affianced == None
    def is_engaged(self,):
        return self.has_affianced()

    def has_affianced(self,):
        return self._affianced != None
    def get_affianced(self,):
        return self._affianced
    def set_affianced(self, affianced):
        self._affianced = affianced
        return True

    def set_free(self,):
        self._affianced = None
        return True
    def set_engaged(self, affianced):
        return self.set_affianced(affianced)

    def get_id(self,):
        return self._id
    def __repr__(self,):
        return str(self.get_id())

class Man(Person):
    def __init__(self, i):
        Person.__init__(self, i)
        self._proposed = []
        return

    def still_in_action(self, women):
        return self.is_free() and len(self._proposed) < len(women)

    def get_woman_to_propose_to(self,):
        women_candidate = [woman for woman in self._preference
                           if woman not in self._proposed]
        return women_candidate[0]

    def add_proposed_list(self, woman):
        self._proposed.append(woman)
        return
    def get_proposed_list(self,):
        return self._proposed

class Woman(Person):
    def __init__(self, i):
        Person.__init__(self, i)
        return

    def prefer_to_affianced(self, man_proposed):
        return self.__prefer(man_proposed, self._affianced)

    def __prefer(self, a, b):
        return self._preference.index(a) < self._preference.index(b)

class StableMarriage:
    def __init__(self, n):
        self._men = [Man(i) for i in range(n)]
        self._women = [Woman(i) for i in range(n)]
        for man in self._men:
            man.set_preference([w for w in self._women])
        for woman in self._women:
            woman.set_preference([m for m in self._men])
        # for debug
        self._pair_history = []
        return

    def main(self,):
        men_in_action = [man for man in self._men
                         if man.still_in_action(self._women)]
        while len(men_in_action) > 0:
            man = men_in_action[0]
            woman = man.get_woman_to_propose_to()
            man.add_proposed_list(woman)
            if woman.is_free():
                self.__start_seeing(man, woman)
            else:
                if woman.prefer_to_affianced(man):
                    cuckold = woman.get_affianced()
                    self.__start_seeing(man, woman)
                    cuckold.set_free()
                else:
                    # nothing happens
                    pass
            men_in_action = [man for man in self._men
                             if man.still_in_action(self._women)]
        return

    def __start_seeing(self, man, woman):
        woman.set_engaged(man)
        man.set_engaged(woman)
        self._pair_history.append((man, woman))
        return

    def print_result(self,):
        for man in self._men:
            if man.is_engaged():
                sys.stdout.write("%s is engaged with %s\n"
                                 %(man, man.get_affianced()))
            else:
                sys.stdout.write("%s is free\n" %man)
        for man in self._men:
            sys.stdout.write("%s propoesd to %s\n"
                             %(man, [woman for woman in man.get_proposed_list()]))
        for (m,w) in self._pair_history:
            sys.stdout.write("pairs: (%s,%s)\n" %(m ,w))
        return

def main():
    SM = StableMarriage(5)
    SM.main()
    SM.print_result()

if __name__ == '__main__':
    main()
