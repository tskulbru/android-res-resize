
"""
    Version 0.1 alpha
    (c) 2011 Johannes Lindenbaum
    
    License: Do what you want, give credit where credit is due
    
    Description:
        The script will traverse a directory, assuming it's the folder
        containing your xhdpi images.
        It will resize each image and store it in ../drawable-SCALE-TYPE/
        Assuming your folder containing xhdpi images, you will end up
        with the following folder structure:
            drawable/
            drawable-ldpi/
            drawable-mdpi/
            drawable-hdpi/
        The scaling values are used from the android developer site and are:
            xhdpi = 1
            hdpi = 0.75
            mdpi = 0.5
            ldpi = 0.5 * 0.75
    
    Usage:
        python android-res-resize.py --foler FOLDER-TO-PROCESS
    
"""

import argparse
import os
import Image


class AndroidResResize:

    SCALES = {
        'hdpi': 0.75,
        'mdpi': 0.5,
        'ldpi': 0.5 * 0.75,
    }

    ACCEPTED_EXTENSIONS = ['.png', '.jpg']

    SILENCE = False

    """
    Set verbosity level of application.
    Supports verbose or silent
    """
    def setVerbosity(self, silence):
        if silence:
            self.SILENCE = silence;

    def resizeAllInFolder(self, path):
        if self.SILENCE == False:
            print "Processing folder " + path

        # determine trailing slash
        if path[-1:] != "/":
            path = path + "/"

        for fileName in os.listdir(path):
            fullPath = path + fileName
            baseName, fileExtension = os.path.splitext(path + fileName)

            if fileExtension in self.ACCEPTED_EXTENSIONS and fullPath[-6:] != ".9.png":

                for scale in self.SCALES:
                    if self.SILENCE == False:
                        print "Processing (" + scale + "): " + fullPath

                    # get scale value
                    scaleValue = self.SCALES[scale]

                    # resize image
                    image = Image.open(fullPath)
                    imageSize = image.size
                    newWidth = int(round(imageSize[0] * scaleValue))
                    newHeight = int(round(imageSize[1] * scaleValue))
                    imageHdpi = image.resize((newWidth, newHeight), Image.ANTIALIAS)

                    # determine if where we're writing to exists
                    outputPath = path + "../drawable-" + scale + "/"
                    if os.path.exists(outputPath) == False:
                        if self.SILENCE == False:
                            print "Creating output directory for image."

                        try:
                            os.makedirs(outputPath)
                        except error:
                            print "Could not create directory: " + outputPath
                            return

                        if self.SILENCE == False:
                            print "Saving: " + outputPath + fileName

                        imageHdpi.save(outputPath + fileName)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Automatically resize images for Android res/")
    argParser.add_argument("--folder", default=None, required=True, dest="folderPath")
    argParser.add_argument("--silence", default=False, dest="option_silence")
    args = argParser.parse_args()

    resizer = AndroidResResize()
    resizer.setVerbosity(args.option_silence)
    resizer.resizeAllInFolder(args.folderPath)

    if args.option_silence == False:
    print "Done."
