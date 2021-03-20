import logic
import automation

def prompt():
    msg = input('Type a message: ')
    logic.getAnswer(msg, automation.phone_number)
    if not msg == "exit":
        prompt()

prompt()