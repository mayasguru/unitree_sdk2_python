#!/usr/bin/env python3
import multiprocessing
from unitree_sdk2py.core.channel import (
    ChannelFactory,
    ChannelFactoryInitialize,
)
from image import Image
from g1_bot.cameras.realsense import RealSenseCamera
import numpy as np
import pyrealsense2 as rs
import time
import cv2
from user_data import UserData
from cyclonedds.qos import Qos, Policy


def image_publisher(output_interface="wlan0"):
    ChannelFactoryInitialize(0, output_interface)
    realsense_ctx = rs.context()
    id = None
    for device in realsense_ctx.devices:
        id = device.get_info(rs.camera_info.serial_number)


    face_camera = RealSenseCamera(camera_id=id)
    factory = ChannelFactory()
    factory.Init(0, output_interface, qos=Qos(Policy.Reliability.Reliable(0)))
    
    # Create channel with reliable QoS
    pub = factory.CreateChannel("face_camera", Image)
    pub.SetWriter()  # Uses factory's QoS
    while True:
        frame = face_camera.get_bgr_image()
        resized_frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
        image_data = resized_frame.astype(np.uint8).flatten().tolist()
        msg = Image(image_data=image_data)
        pub.Write(msg, 0.5)
        print("Published Image")
        time.sleep(1)

def main():
    img_proc = multiprocessing.Process(target=image_publisher)
    img_proc.start()

    try:
        img_proc.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
        img_proc.terminate()


if __name__ == "__main__":
    main()
