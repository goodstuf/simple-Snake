from pynput import keyboard

UPkeyReleased = True
RIGHTkeyReleased = True
LEFTkeyReleased = True
DOWNkeyReleased = True

def newInputDetection():
    def on_press(key):
        global UPkeyReleased, RIGHTkeyReleased, LEFTkeyReleased, DOWNkeyReleased
        if str(key) == "Key.up" and UPkeyReleased:
            print("up clicked")
            UPkeyReleased = False
        if str(key) == "Key.right" and RIGHTkeyReleased:
            RIGHTkeyReleased = False
        if str(key) == "Key.left" and LEFTkeyReleased:
            print("left clicked")
            LEFTkeyReleased = False
        if str(key) == "Key.down" and DOWNkeyReleased:
            DOWNkeyReleased = False
        #print(key, LEFTkeyReleased)

    def on_release(key):
        global UPkeyReleased, RIGHTkeyReleased, LEFTkeyReleased, DOWNkeyReleased
        
        if str(key) == "Key.up" and not UPkeyReleased:
            print("up")
            UPkeyReleased = True
        elif str(key) == "Key.right" and not RIGHTkeyReleased:
            RIGHTkeyReleased = True
        elif str(key) == "Key.left" and not LEFTkeyReleased:
            print("left")
            LEFTkeyReleased = True
        elif str(key) == "Key.down" and not DOWNkeyReleased:
            DOWNkeyReleased = True

    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

newInputDetection()