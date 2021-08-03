import logic
import automation

def prompt():
    msg = input('Type a message: ')
    print(logic.getAnswer(msg, automation.phone_number))
    if not msg == "exit":
        prompt()

prompt()
