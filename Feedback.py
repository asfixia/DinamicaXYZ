class Feedback():
    @staticmethod
    def pushConsoleInfo(message):
        print(message)

    @staticmethod
    def setProgress(percentage):
        print("Progress: " + str(percentage))

    @staticmethod
    def setProgressText(message):
        print(message)

    @staticmethod
    def isCanceled():
        return False

