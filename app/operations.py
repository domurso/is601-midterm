class Operation:

    @staticmethod
    def addition(a: float,b:float) -> float:
        
        """
        Adds two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Sum of *a* and *b*
        """
        return a+b
    
    @staticmethod
    def subtraction(a:float,b:float) -> float:
        """
        Subracts two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: difference of *a* and *b*
        """
        return a-b


    @staticmethod
    def multiply(a:float,b:float) -> float:
        """
        multiply two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: multiplcation of *a* and *b*
        """
        return a*b



    @staticmethod
    def divide(a:float,b:float) -> float:
        """
        Subracts two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*:  division of *a* and *b*
        """
        if(b == 0):
            raise ValueException("Divide By Zero Error")
        return a/b



    @staticmethod
    def pow(a:float,b:float) -> float:
        """
        multiply two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: power of *a* to the *b*
        """
        return pow(a,b)


    @staticmethod
    def root(a:float,b:float) -> float:
        """
        root of  two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: root of *a* and *b*
        """
        if(b == 0):
            raise ValueException("Divide By Zero Error")
        return pow(a,1/b)



    @staticmethod
    def multiply(a:float,b:float) -> float:
        """
        multiply two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: multiplcation of *a* and *b*
        """
        return a*b



    @staticmethod
    def modulo(a:float,b:float) -> float:
        """
        modulo two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*:  modulo of *a* and *b*
        """
        if(b == 0):
            print("Divide By Zero Error")
            raise ValueException("Divide By Zero Error")
        return a%b
