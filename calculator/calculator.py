"""Calculator implementation."""

import Ice
import RemoteCalculator as rc

class Calculator(rc.Calculator):
    def sum(self,a,b,current):
        """Sum two numbers."""
        return a + b
    
    def sub(self,a,b,current):  
        """Subtract two numbers."""
        return a - b
    
    def mult(self,a,b,current):
        """Multiply two numbers."""
        return a * b
    
    def div(self,a,b,current):
        """Divide two numbers.
        Raises ZeroDivisionError if b is zero."""
        if b == 0:
<<<<<<< HEAD
            raise rc.ZeroDivisionError
=======
            raise rc.ZeroDivisionError()
>>>>>>> separar-comunicador
        return a / b
