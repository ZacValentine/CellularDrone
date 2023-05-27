# import libraries
from vidgear.gears import VideoGear
from vidgear.gears import NetGear
from vidgear.gears import CamGear

options = {"flag": 0, "copy": False, "track": False}

#stream = VideoGear(source='test.mp4').start()  # Open any video stream
stream = CamGear(source=0).start()

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

        # do something with frame here

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        # break the infinite loop
        break

# safely close video stream
stream.stop()
# safely close server
writer.close()
