"""Calculator implementation."""

import Ice
import RemoteCalculator as rc

class Calculator(rc.Calculator):
    def sum(a,b,current):
        """Sum two numbers."""
        return a + b
    
    def sub(a,b,current):  
        """Subtract two numbers."""
        return a - b
    
    def mult(a,b,current):
        """Multiply two numbers."""
        return a * b
    
    def div(a,b,current):
        """Divide two numbers."""
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b
