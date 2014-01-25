#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
from StableMarriage import Man,Woman,StableMarriage

class Student(Man):
    def get_lab_to_enroll(self,):
        return self.get_woman_to_propose_to()
    def add_enroll_list(self, lab):
        return self.add_proposed_list(lab)
    def get_enroll_list(self,):
        return self.get_proposed_list()

    def set_enrolled(self, lab):
        return self.set_engaged(lab)

class Lab(Woman):
    def __init__(self, i):
        Woman.__init__(self, i)
        self._capacity = 0
        self._affianced = []
        # copy it to use parent functions
        self._students = self._affianced
        return

    def is_free(self):
        return len(self._students) < self._capacity
    def is_engaged(self,):
        return self.is_free == False
    def set_free(self,):
        self._students = []
        return True

    def has_affianced(self,):
        return self.is_engaged()
    def add_student(self, student):
        return self._students.append( student )
    def remove_student(self, student):
        return self._students.remove( student )

    def get_least_preferred_student(self,):
        least_preferred_student = None
        rank = -1
        for student in self._students:
            this_rank = self._preference.index(student)
            if this_rank > rank:
                least_preferred_student = student
                rank = this_rank
        return least_preferred_student
    def get_students(self,):
        return self.get_affianced()

    def set_capacity(self, capacity):
        self._capacity = capacity
        return True

class StableLabAssignment(StableMarriage):
    def __init__(self,
                 students_num, labs_num,
                 capacities = None):
        if isinstance(capacities, list) == False or len(capacities) != labs_num:
            capacities = self.__dispatch_capacities(students_num, labs_num)
        # initialize
        self._students = [Student(i) for i in range(students_num)]
        self._labs = [Lab(i) for i in range(labs_num)]
        for i in range(len(self._labs)):
            lab = self._labs[i]
            lab.set_capacity(capacities[i])
        # copy them to use parent functions
        self._men = self._students
        self._women = self._labs
        # for debug
        self._pair_history = []
        return

    def __dispatch_capacities(self, students_num, labs_num):
        # dispatch equally
        res = [students_num / labs_num for i in range(labs_num)]
        # dispatch remaining students
        for target_lab in random.sample(range(labs_num), students_num % labs_num):
            res[target_lab] += 1
        return res

    def main(self,):
        student_unassigned = [student for student in self._students
                              if student.is_free()
                              and student.still_has_hope( all_candidate = self._labs )]
        while len(student_unassigned) > 0:
            student = student_unassigned[0]
            lab = student.get_lab_to_enroll()
            student.add_enroll_list(lab)
            if lab.is_free():
                self.__enroll(student, lab)
            else:
                downsize_candidate = lab.get_least_preferred_student()
                if lab.prefer(student, downsize_candidate):
                    self.__enroll(student, lab)
                    lab.remove_student(downsize_candidate)
                    downsize_candidate.set_free()
                else:
                    # nothing happens
                    pass
            student_unassigned = [student for student in self._students
                                  if student.is_free()
                                  and student.still_has_hope( all_candidate = self._labs )]
        return

    def __enroll(self, student, lab):
        student.set_enrolled(lab)
        lab.add_student(student)
        self._pair_history.append((student, lab))
        return

    def print_result(self,):
        StableMarriage.print_result(self,)
        sys.stdout.write("Labs assignment:\n")
        for lab in self._labs:
            sys.stdout.write("    %s's students: %s\n"
                             %(lab, [student for student in lab.get_students()]))
        return

def main():
    SLA = StableLabAssignment(students_num = 12, labs_num = 5)
    SLA.set_preferences()
    SLA.main()
    SLA.print_result()

if __name__ == '__main__':
    main()
