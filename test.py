import msvcrt
import threading
import time

class TestClass:
    def __init__(self):
        self.run = True
        self.thread_manager()

        while self.run:
            print("La aplicación está corriendo...")
            time.sleep(2)

    def thread_manager(self):
        t1 = threading.Thread(target=self.__keypress)
        t1.start()

    def __keypress(self):
        while self.run:
            if msvcrt.kbhit():
                try:
                    key = msvcrt.getch().decode('utf-8').upper()
                except Exception as e:
                    continue

                if key == "Q":
                    print("Saliendo de la aplicación...")
                    self.__quit_app()
                else:
                    print(key)
    
    def __quit_app(self):
        self.run = False

if __name__ == "__main__":
    test = TestClass()