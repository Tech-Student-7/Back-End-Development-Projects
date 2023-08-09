# Import ABC and abstractmethod from the module abc (which stands for abstract base classes)
from abc import ABC, abstractmethod

#1 Class Bank
class Bank(ABC):

    # create the basicinfo()
    def basicinfo(self) -> None:
        print("This is a generic bank")
        return "Generic bank: 0"        

    @abstractmethod
    def withdraw(self) -> None:
        pass

# Class Swiss
class Swiss(Bank):

    # create a constructor
    def __init__(self) -> None:
        self.bal = 1000

    def basicinfo(self) -> None:
        print("This is the Swiss Bank")
        return (f"Swiss Bank: {self.bal}")

    def withdraw(self, amount) -> None:
        self.amount = amount

        if self.amount > self.bal:
            print("Insufficient funds!")
            return self.bal
        else:
            self.bal -= self.amount
            print(f"Withdrawn amount: {self.amount}")
            print(f"New balance: {self.bal}")
            return self.bal

# Driver Code
def main():
    assert issubclass(Bank, ABC), "Bank must derive from class ABC"
    s = Swiss()

    print(s.basicinfo())

    s.withdraw(30) # First withdrawal transaction
    s.withdraw(1000) # Second withrawal transaction

    j = Swiss()
    j.withdraw(500)
    j.withdraw(581)

if __name__ == "__main__":
    main()