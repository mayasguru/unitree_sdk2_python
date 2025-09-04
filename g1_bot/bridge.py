#!/usr/bin/env python3
import multiprocessing
from unitree_sdk2py.core.channel import (
    ChannelSubscriber,
    ChannelPublisher,
    ChannelFactoryInitialize,
)
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_
from g1_bot.msgs.Image import Image
from g1_bot.cameras.realsense import RealSenseCamera
import numpy as np
import pyrealsense2 as rs


def subscriber_process(queue, input_interface="eth0"):
    """Subscribe on eth0 and send raw LowState_ objects to queue."""
    ChannelFactoryInitialize(0, input_interface)
    sub = ChannelSubscriber("rt/lowstate", LowState_)
    sub.Init()
    print(f"[SUB] Listening on {input_interface}...")

    while True:
        msg = sub.Read(timeout=0.5)
        if msg:
            try:
                queue.put(msg, timeout=0.5)
            except:
                print("Queue full, dropping message.")


def publisher_process(queue, output_interface="wlan0"):
    """Receive raw LowState_ objects from queue and publish on wlan0."""
    ChannelFactoryInitialize(0, output_interface)
    pub = ChannelPublisher("topic", LowState_)
    pub.Init()
    print(f"[PUB] Republishing on {output_interface}...")

    while True:
        msg = queue.get()  # blocks until message available
        pub.Write(msg)

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
    queue = multiprocessing.Queue(maxsize=10)

    # sub_proc = multiprocessing.Process(target=subscriber_process, args=(queue, "eth0"))
    # pub_proc = multiprocessing.Process(target=publisher_process, args=(queue, "wlan0"))
    img_proc = multiprocessing.Process(target=image_publisher)

    # sub_proc.start()
    # pub_proc.start()
    img_proc.start()

    try:
        # sub_proc.join()
        # pub_proc.join()
        img_proc.join()
    except KeyboardInterrupt:
        print("\nShutting down...")
        # sub_proc.terminate()
        # pub_proc.terminate()
        img_proc.terminate()


if __name__ == "__main__":
    main()
