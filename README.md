Timed Boolean Functions
=======================

Timed Boolean Function is a function B(t) -> B(t) - where B(t) is a 
signal space - collection of mappings (R, B) where R is real number, 
representing time and B is Bool {0,1}. So full TBF function signature 
is the following [1]

(R, B) -> (R, B)

tbf module allow you define a system of timed boolean functions defined 
in the following way:

functionName (riseDelay , fallDelay ) = functionExpression

and execute this system in the real time domain or as fast as possible.

Usage
~~~~~

    >>> import tbf
    >>> tbf.runSimple("A(1000,100)=!A")

References
~~~~~~~~~~

    1. William K. C. Lam, Robert K. Brayton, Timed Boolean Functions: 
        A Unified Formalism for Exact Timing Analysis
        http://books.google.ru/books/about/Timed_Boolean_Functions.html?id=iFIe4JkCF5UC&redir_esc=y

