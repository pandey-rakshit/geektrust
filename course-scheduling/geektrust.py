from sys import argv
from constants import Status, Messages



class MainApp:
    def __init__(self, file_path):
        self.file_path = file_path
        # self.manager = 
        

    def run(self):
        try:
            self.validate_arguments()
            self.process_file()
        except Exception as e:
            print(f"Error: {e}")

    def validate_arguments(self):
        if len(argv) != 2:
            raise ValueError(Status.FILE_PATH_NOT_ENTERED)

    def process_file(self):
        with open(self.file_path, "r") as file:
            commands = file.readlines()

        # self.manager.process_commands(commands)


if __name__ == "__main__":
    try:
        file_path = argv[1]
        app = MainApp(file_path)
        app.run()
    except IndexError:
        print(Messages.USAGE)
    except Exception as e:
        print(f"Error: {e}")
