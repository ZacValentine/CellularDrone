# import libraries
from vidgear.gears import VideoGear
from vidgear.gears import NetGear
from vidgear.gears import CamGear
import cv2

options = {
    "STREAM_RESOLUTION": '240p',  # '240p'
}
stream = VideoGear(source=0, **options).start()
#stream = CamGear(

options = {"flag": 0, "copy": False, "track": False}
server = NetGear(
    address="100.80.57.27",
    port="5000",
    protocol="tcp",
    pattern=1,
    logging=True,
    **options
)


# infinite loop until [Ctrl+C] is pressed
while True:
    try:
        frame = stream.read()
        # read frames

        # check if frame is None
        if frame is None:
            # if True break the infinite loop
            break

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        # break the infinite loop
        break

# safely close video stream
stream.stop()
