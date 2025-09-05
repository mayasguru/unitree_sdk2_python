#!/usr/bin/env python3
import multiprocessing
from cyclonedds.qos import Qos, Policy
from unitree_sdk2py.core.channel import (
    ChannelFactory,
    ChannelFactoryInitialize,
)
from image import Image
import numpy as np
from PIL import Image as pilImage
import time

def image_subscriber(input_interface="en0"):
    ChannelFactoryInitialize(0, input_interface)
    factory = ChannelFactory()
    factory.Init(0, input_interface, qos=Qos(Policy.Reliability.Reliable(0)))
    
    # Create channel with reliable QoS
    sub = factory.CreateChannel("face_camera", Image)
    sub.SetReader()  # Uses factory's QoS
    img_num = 0
    while True:
        msg = sub.Read(timeout=3.0)
        if msg:
            print("Received Image")
            if isinstance(msg.image_data, bytes):
                image_array = np.frombuffer(msg.image_data, dtype=np.uint8).reshape(240, 320, 3)
            else:
                image_array = np.array(msg.image_data, dtype=np.uint8).reshape(240, 320, 3)
            
            img = pilImage.fromarray(image_array)
            img.save(f"image_{img_num}.png")
            img_num += 1
        time.sleep(1.0)
            
        

def main():
    img_proc = multiprocessing.Process(target=image_subscriber)
    img_proc.start()

    try:
        img_proc.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
        img_proc.terminate()


if __name__ == "__main__":
    main()
