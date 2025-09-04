from realsense import RealSenseCamera
import pyrealsense2 as rs
from PIL import Image

RS455_PID = 0x0B5C
RS435I_PID = 0x0B3A
RS405_PID = 0x0B5B

camera_version_dict = {
    RS455_PID: "RS455",
    RS435I_PID: "RS435I",
    RS405_PID: "RS405",
}

if __name__ == "__main__":
    realsense_ctx = rs.context()
    connected_devices = {version: [] for version in camera_version_dict.values()}

    for device in realsense_ctx.devices:
        id = device.get_info(rs.camera_info.serial_number)
        product_id = int(device.get_info(rs.camera_info.product_id), 16)
        camera_version = camera_version_dict[product_id]
        print(
            f"Detected Camera: {id}, Product ID: {product_id}, Camera Version: {camera_version}"
        )
        camera = RealSenseCamera(camera_id=id, width=320, height=240)
        bgr_img = Image.fromarray(camera.get_bgr_image())
        bgr_img.save('bgr_img.png')
        depth_img = Image.fromarray(camera.get_depth_image())
        depth_img.save('depth_img.png')
        camera.stop()