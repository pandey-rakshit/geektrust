from sys import argv
from src.Runable import Runnable

class Main:
    def __init__(self):
        self.r = Runnable()

    def main(self):
        if len(argv) != 2:
            raise Exception("File path not entered")
        file_path = argv[1]
        # Open and read the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.r.process_commands(lines)
            
if __name__ == "__main__":
    Main().main()