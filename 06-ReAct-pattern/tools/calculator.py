def calculate(expression:str ) -> str:
    try:
        return str(eval(expression))
    except Exception as e:
        return f"error: {str(e)}"