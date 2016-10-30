###############################################################################
# This Module is a rudimentary CAS that should on completion be able to
# Calculate the basic Gaussian Error regressian in Polynomial structures
# Moast code was Developt in Collaboration with m3ssias (can be found on
# GitHub)
# Authors: m3ssias, Alexander Becker
# Date of Creation: 30.10.16
###############################################################################

#================================= imports ====================================
# None yet
#==============================================================================

################################## The Tree Structure #########################
#This is the Parent Class that defines that every node has a funktion
# that derives or prints this part of the tree.
class Node:
    def derive(self):
        pass
    def __str__(self):
        pass

#================================= Subclasses to node =========================
# This Subclass represents a number in the algebraic tree
class NumberNode(Node):
    def __init__(self, value):
        self.value = value
    def derive(self):
        return NumberNode(0)
    # we answer with the String as the output of the print Funktion
    def __str__(self):
        return str(self.value)

# This Node represents a variable in the Tree
class VariableNode(Node):
    def __init__(self, name):
        self.value = name
    def deive(self, dx):
        if dx == name:
            return NumberNode(1)
        else:
            return NumberNode(0)

# This node is the representation of addition
class AdditionNode(Node):
    def __init__(self, left, right):
        self.rightside = right
        self.leftside = left
    def derive(self):
        return AdditionNode(self.leftside.derive(), self.rightside.derive())
    def __str__(self):
        return '('+str(self.leftside)+'+'+str(self.rightside)')'

# This node is the representation of the Subtraction
class SubtractionNode(Node):
    def __init__(self, left, right):
        self.minuend = left
        self.subtrahend = right
    def derive(self):
        return SubtractionNode(minuend.derive(),subtrahend.derive())
    def __str__(self):
        return '('+str(self.leftside)+'-'+str(self.rightside)')'

# This node is the Representation of the Multiplication
class MultiplicationNode(Node):
    def __init__(self, left, right):
        self.rightside = right
        self.leftside = left
    def derive(self):
        left = MultiplicationNode(self.leftside.derive(),self.rightside)
        right = MultiplicationNode(self.leftside, self.rightside.derive())
        return AdditionNode(left,right)
    def __str__(self):
        return '('+str(self.leftside)+'*'+str(self.rightside)')'

# This Node is the Representation of the Division
class DivisionNode(Node):
    def __init__(self, left, right):
        self.p = right
        self.q = left
    def derive(self):
        p = AdditionNode(MultiplicationNode(p.derive(),q), MultiplicationNode(NumberNode(-1),MultiplicationNode(p,q.derive())))
        q = MultiplicationNode(q,q)
        return DivisionNode(p,q)
    def __str__(self):
        return '('+str(self.p)+'/'+str(self.q)')'

class NaturalLogarithmNode(Node):
    def __init__(self, input):
        self.loginput = input
    def derive(self):
        return DivisionNode(self.loginput.derive()/self.loginput)
    def __str__(self):
        return 'ln('+str(self.loginput)+')'

class ExponentNode(Node):
    def __init__(self, left, right):
        self.base = right
        self.exponent = left
    def derive(self):
        firstpart = MultiplicationNode(self.exponent,MultiplicationNode(ExponentNode(self.base,SubtractionNode(exponent,1)),self.base.derive())
        secondpart = MultiplicationNode(MultiplicationNode(ExponentNode(self.base,self.exponent),NaturalLogarithmNode(self.base)),self.exponent.derive())
        return AdditionNode(firstpart,secondpart)
    def __str__(self):
        return '('+str(self.base)+'^'+str(self.exponent)')'
#================================= End of Subclasses===========================

################################## End  of Tree Structure #####################

#================================= Funktions ==================================
def parse(string):
    i = 0
    position = None
    operator = None
    while i < len(string):
        if string[i] == '(':
            while string[i+1] != ')':
                i+=1
        elif string[i] == '+':
            position = i
            operator = '+'
            break
        elif string[i] = '-':
            position = i
            operator = '-'
            break
        elif string[i] == '*':
            position = i
            operator = '*'
        elif string[i] == '/' and operator != '*':
            position = i
            operator = '/'
        elif string[i] == '^'
            position = i
            operator 
        i+=1
    if operator != None:
        if operator == '+':
            return AddNode(parse(string[0:i]), parse(string[i+1:]))
        elif operator == '*':
            return MulNode(parse(string[0:position]), parse(string[position+1:]))
        elif operator == '/':
            return DivNode(parse(string[0:position]), parse(string[position+1:]))
        elif operator == '^':
            return ExponentNode(parse(string[0:position]), parse(string[position+1:]))
    i = 0
    while i < len(string):
        c = string[i]
        if c == '(':
            j = i
            while string[j+1] != ')':
                j+=1
            return parse(string[i+1:j+1])
        if c == '.':
            num = None
            j = i+1
            while j < len(string) and string[j].isnumeric():
                j+=1 
            return NumNode(float(string[i:j]))
        if c.isnumeric():
            dot = None
            num = None
            j = i+1
            while j < len(string):
                if string[j].isnumeric():
                    num = True
                if string[j] == '.':
                    dot+=1
                j+=1 
            if dot == 0 or dot == 1:
                return NumNode(float(string[i:j]))
        if c.isalpha():
            return VarNode(c)
        i+=1
################################## ENDE #######################################
