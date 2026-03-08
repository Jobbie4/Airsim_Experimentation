import numpy
import os
import pprint

#Note for you
#for every python class, there is an implicit call of the method __new__ that creates the class when it is defined. you don't actually have to call __new__
# This is different than c++ and java, which is why you found this confusing

#__init__ is a recognized implicitly defined method (keyword) in python and will also be run automatically when a class is defined
#__init__ can be used to define initial parameters within the class

#This is a basic class that is initialized with parameters, and includes a method to display those parameters
class basicClass:
    def __init__(self):
        #stuff to initialize the class
        self.how_it_feels_to_be_awesome = "awesome"
        self.what_is_good = "better"
        self.who_are_you ="I really wanna know"
     
    #stuff the class does
    def PrintStuff(self):
        print(self.how_it_feels_to_be_awesome)
 
    def PrintMoreStuff(self):
        print(self.how_it_feels_to_be_awesome)

    def PrintEvenMoreStuff(self):
        print(self.who_are_you)


def main():
    testClass =basicClass()
    print("first function call")
    testClass.PrintStuff()
    print("second function call")
    testClass.PrintMoreStuff()
    print("third function call")
    testClass.PrintEvenMoreStuff()

#main call
main()
##This allows for external file imports and for the dictating file to run things.  This is interesting functionality, but not realatedf to what I'm tryingf to learn
#if __name__ == "__main__":
#    mainhoser()
#    #try: #note, this doesn't work because the scope of self is within init only
#    #    print(testClass.how_I_feel_right_now())
#    #finally:
#    #    print(testClass.how_I_want_to_feel())
