import time
from stem import Signal
from stem.control import Controller


def rotate_tor_ip():
    print("Initiating Tor proxy circuit rotation...")
    try:
        with Controller.from_port(address="127.0.0.1", port="9051") as controller:
            controller.authenticate()

            if controller.is_newnym_available():
                controller.signal(Signal.NEWNYM)
                print("Tor identity rotated successfully!")
                time.sleep(3)
            else:
                print("Newnym request rate-limited by Tor. Waitign for cooldown...")
    except Exception as e:
        print(f"Failed to communicate with Tor ContrilPort: {e}")
