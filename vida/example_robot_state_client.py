import time

from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_


if __name__ == "__main__":
    ChannelFactoryInitialize(0, "en0")
    # Create a subscriber to subscribe the data defined in UserData class
    sub = ChannelSubscriber("topic", LowState_)
    sub.Init()

    while True:
        msg = sub.Read(timeout=3.0)
        if msg is not None:
            print("Subscribe success. msg:", msg)
        else:
            print("No data subscribed.")
            break
    sub.Close()
