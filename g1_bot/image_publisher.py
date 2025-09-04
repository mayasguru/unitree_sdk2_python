#!/usr/bin/env python3
import multiprocessing
from unitree_sdk2py.core.channel import (
    ChannelPublisher,
    ChannelFactoryInitialize,
)
from g1_bot.msgs.Image import Image
from g1_bot.cameras.realsense import RealSenseCamera
import numpy as np
import pyrealsense2 as rs

def image_publisher(output_interface="wlan0"):
    ChannelFactoryInitialize(0, output_interface)
    realsense_ctx = rs.context()
    id = None
    for device in realsense_ctx.devices:
        id = device.get_info(rs.camera_info.serial_number)

    print(id)
    print(type(id))
    face_camera = RealSenseCamera(camera_id=id)
    pub = ChannelPublisher("g1/face_images", Image)
    pub.Init()
    while True:
        image_data = face_camera.get_bgr_image().astype(np.uint8).flatten().tolist()
        msg = Image(image_data=image_data)
        pub.Write(msg)

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
