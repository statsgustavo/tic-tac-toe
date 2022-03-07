class BadMarkError(Exception):
    def __init__(self, value, message=None):
        self.message = (
            "Tic-tac-toe is played with x's and o's." 
            if message is None 
            else message
        )
        self.value = value
        super().__init__(self.message)


class MarkedPositionError(Exception):
    def __init__(self, value, message=None):
        self.message = (
            "Position was already chosen by another player." 
            if message is None 
            else message
        )
        self.value = value
        super().__init__(self.message)


class BadCliUserInputError(Exception):
    def __init__(self, value, message=None):
        self.message = (
            (
                "Values for rows are ('1', '2' or '3') and " 
                + "for columns are ('a', 'b' or 'c')."
            )
            if message is None 
            else message
        )
        self.value = value
        super().__init__(self.message)
