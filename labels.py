from yattag import Doc, indent
import cv2
import os
import glob
from PIL import Image

path = 'images'
imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
for imagePath in imagePaths:
    doc, tag, text = Doc().tagtext()
    dirpath = os.getcwd()
    path = os.path.join(dirpath, imagePath)
    imagePath = imagePath.split('\\')
    img = cv2.imread(path)
    dimensions = img.shape
    folder = imagePath[0]
    filename = imagePath[1].split(".")[0]
    database = 'Unknown'
    xmax = dimensions[1]
    ymax = dimensions[0]
    width = xmax
    height = ymax
    depth = 1
    segmented = 0
    name = 'XRay'
    pose = 'Unspecified'
    truncated = 0
    difficult = 0
    xmin = 1
    ymin = 1
    with tag('annotation'):
        with tag('folder'):
            text(folder)
        with tag('filename'):
            text(filename + '.jpg')
        with tag('path'):
            text(path)
        with tag('source'):
            with tag('database'):
                text(database)
        with tag('size'):
            with tag('width'):
                text(xmax)
            with tag('height'):
                text(ymax)
            with tag('depth'):
                text(depth)
        with tag('segmented'):
            text(segmented)
        with tag('object'):
            with tag('name'):
                text(name)
            with tag('pose'):
                text(pose)
            with tag('truncated'):
                text(truncated)
            with tag('difficult'):
                text(difficult)
            with tag('bndbox'):
                with tag('xmin'):
                    text(xmin)
                with tag('ymin'):
                    text(ymin)
                with tag('xmax'):
                    text(xmax)
                with tag('ymax'):
                    text(ymax)
    result = indent(
        doc.getvalue(),
        indentation = ' ' * 4,
        newline = '\n'
    )
    f = open(('images\\' + filename + '.xml'), "w+")
    f.write(result)
    del(doc)
    f.close()