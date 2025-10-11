def add(x,y):
    return x+y 
def subtract(x,y):
    return x-y  
def multiply(x,y):
     return x*y
def divide(x,y):
    if y==0:
     return "Error! Division by zero."
    else:
     return x/y
def exponent(x,y):
     return x**y
def modulus(x,y):
      return x%y
def floor_divide(x,y):
    if y==0:
        return "Error! Division by zero."
    else:
            return x//y
#single -input operations
import math

def square_root(x): 
    if x<0:
        return "cannot take square root of negative number"
    else:
            return math.sqrt(x)

def log10(x):
    if x <= 0:
        return "logarithm undefined for non-positive numbers"
    else:
        return math.log10(x)
        
def natural_log(x):
    if x<=0:

        return "natural log undefined for non -positive numbers"
    
    else:
        return math.log(x)
