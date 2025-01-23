# -*- coding: iso-8859-1 -*-
from typing import Tuple, List

import numpy
import sys
from numba import jit
from gooey import Gooey, GooeyParser
import cv2
import time


@jit
def execute(RGB, color_deficit):

    if color_deficit == 'd':
        lms2lms_deficit = lms2lmsd

    elif color_deficit == 'p':
        lms2lms_deficit = lms2lmsp

    elif color_deficit == 't':
        lms2lms_deficit = lms2lmst
    # Transform to LMS space

    LMS = numpy.zeros_like(RGB)
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            rgb = RGB[i, j, :3]
            LMS[i, j, :3] = numpy.dot(rgb2lms, rgb)

    # Calculate image as seen by the colorblind
    _LMS = numpy.zeros_like(RGB)

    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            lms = LMS[i, j, :3]
            _LMS[i, j, :3] = numpy.dot(lms2lms_deficit, lms)
    _RGB = numpy.zeros_like(RGB)
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            _lms = _LMS[i, j, :3]
            _RGB[i, j, :3] = numpy.dot(lms2rgb, _lms)
    # Calculate error between images
    error = (RGB - _RGB)
    # Daltonize
    ERR = numpy.zeros_like(RGB)

    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            err = error[i, j, :3]
            ERR[i, j, :3] = numpy.dot(err2mod, err)

    dtpn = ERR + RGB
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            dtpn[i, j, 0] = max(0, dtpn[i, j, 0])
            dtpn[i, j, 0] = min(255, dtpn[i, j, 0])
            dtpn[i, j, 1] = max(0, dtpn[i, j, 1])
            dtpn[i, j, 1] = min(255, dtpn[i, j, 1])
            dtpn[i, j, 2] = max(0, dtpn[i, j, 2])
            dtpn[i, j, 2] = min(255, dtpn[i, j, 2])
    result = dtpn.astype('uint8')
    return result


def listing_ports() -> tuple[list[int], list[str]]:
    is_working = True
    current_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        camera = cv2.VideoCapture(current_port)
        if not camera.isOpened():
            is_working = False
        else:
            is_reading, img = camera.read()
            if is_reading:
                working_ports.append(str(current_port))
            else:
                available_ports.append(current_port)
        current_port += 1

    return available_ports, working_ports


@Gooey(advanced=True,
       default_size=(500, 500),
       required_cols=1,
       program_name='Dalton, made by Volynets',
       show_preview_warning=False)
def start():
    global lms2lmsd
    global lms2lmsp
    global lms2lmst
    global lms2rgb
    global err2mod
    global rgb2lms

    # Transformation matrix for Deuteranope (a form of red/green color deficit)
    lms2lmsd = numpy.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]])
    # Transformation matrix for Protanope (another form of red/green color deficit)
    lms2lmsp = numpy.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]])
    # Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
    lms2lmst = numpy.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]])

    # Colorspace transformation matrices
    rgb2lms = numpy.array([[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])
    lms2rgb = numpy.linalg.inv(rgb2lms)

    # Daltonize image correction matrix
    err2mod = numpy.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])

    # find available port to get video from
    available_ports, working_ports = listing_ports()

    gui = GooeyParser()
    gui.add_argument('Type', help="Type of dalton", widget='Listbox', choices=['Deuteranope', 'Protanope', 'Tritanope'],
                     nargs='*')
    gui.add_argument('Port', help="Port of Camera", widget='Listbox', choices=working_ports, nargs='+')
    args = vars(gui.parse_args())

    if not args['Port'][0] in working_ports:
        print("Given port does not exist")
        sys.exit(1)
    print("Please wait. Launching...")
    colorblindness = {'Deuteranope': 'd',
                      'Protanope': 'p',
                      'Tritanope': 't'}

    for col_deficit in args['Type']:
        cam = cv2.VideoCapture(int(args['Port'][0]))
        cam.set(3, 280)
        cam.set(4, 225)
        rval = True

        if not cam.isOpened():
            rval = False
        while rval:
            rval, frame = cam.read()

            start = time.time()
            file = execute(numpy.asarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), dtype=float), colorblindness[f'{col_deficit}'])
            cv2.imshow(col_deficit, cv2.cvtColor(file, cv2.COLOR_RGB2BGR))

            end = time.time()
            seconds = end - start
            print(f'{round(1/seconds, 3)} FPS')

            key = cv2.waitKey(20)
            if key == 27:
                break
        cam.release()
        cv2.destroyWindow(col_deficit)


if __name__ == '__main__':
    start()

