import eel
import os
from queue import Queue


class ChatBot:
    """A class representing the ChatBot with Eel integration."""
    started = False
    userinputQueue = Queue()

    @staticmethod
    def isUserInput():
        """Check if there is user input in the queue."""
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        """Pop user input from the queue."""
        return ChatBot.userinputQueue.get()

    @staticmethod
    def close_callback(route, websockets):
        """Handle application close events."""
        if not websockets:
            print('Application closed!')
        exit()

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        """Expose this method to receive user input from JavaScript."""
        ChatBot.userinputQueue.put(msg)
        print(f"User input received: {msg}")

    @staticmethod
    def close():
        """Close the chatbot application."""
        ChatBot.started = False

    @staticmethod
    def addUserMsg(msg):
        """Send a user message to the front end."""
        eel.addUserMsg(msg)

    @staticmethod
    def addAppMsg(msg):
        """Send an application message to the front end."""
        eel.addAppMsg(msg)

    @staticmethod
    def start():
        """Start the Eel application."""
        path = os.path.dirname(os.path.abspath(__file__))
        web_dir = os.path.join(path, 'web')
        eel.init(web_dir, allowed_extensions=['.js', '.html'])

        try:
            eel.start(
                'index.html',
                mode='chrome',
                host='localhost',
                port=27005,
                block=False,
                size=(350, 480),
                position=(10, 100),
                disable_cache=True,
                close_callback=ChatBot.close_callback
            )
            ChatBot.started = True
            print("ChatBot has started.")

            # Run the Eel event loop
            while ChatBot.started:
                eel.sleep(0.1)

        except Exception as e:
            print(f"Error occurred: {e}")
            ChatBot.started = False
