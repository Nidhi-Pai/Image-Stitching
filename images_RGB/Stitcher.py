from panorama import Panorama
import imutils
import cv2
from PIL import Image
from PIL.ExifTags import TAGS
import exifread

#place both Stitcher and panorama in the same folder as that of the images. 

print("Enter the number of images you want to concantenate:")
no_of_images = int(input())
print("Enter the names of the images from left to right in the way of concantenation:")
#like 1.jpg, 2.jpg, 3.jpg .... n.jpg
filename = []

for i in range(no_of_images):
    print("Enter the %d image:" %(i+1))
    filename.append(input())

images = []
   
for i in range(no_of_images):
    images.append(cv2.imread(filename[i]))

#We need to modify the image resolution and keep our aspect ratio, use the function imutils.
for i in range(no_of_images):
    images[i] = imutils.resize(images[i], width=600)

for i in range(no_of_images):
    images[i] = imutils.resize(images[i], height=400)


panorama = Panorama()
if no_of_images == 2:
    (result, matched_points) = panorama.stitch([images[0], images[1]], match_status=True)
else:
    (result, matched_points) = panorama.stitch([images[no_of_images-2], images[no_of_images-1]], match_status=True)
    for i in range(no_of_images - 2):
        (result, matched_points) = panorama.stitch([images[no_of_images-i-3],result], match_status=True)

#to show the images, the valid matched points and the resulting image
for i in range(no_of_images):
    cv2.imshow("Image {k}".format(k = i+1), images[i])

cv2.imshow("Keypoint Matches", matched_points)
cv2.imshow("Panorama", result)

#this saves the two images in the same folder as that of the images
cv2.imwrite("Matched_points.jpg",matched_points)
cv2.imwrite("Panorama_image.jpg",result)

cv2.waitKey(5000)
cv2.destroyAllWindows()

img = ""
print("Enter the image whose exif data is to be read:")
img = input()

# Open image file for reading (binary mode)
f = open(img, 'rb')

# Return Exif tags
tags = exifread.process_file(f)

for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        print ("%s : %s" %(tag, tags[tag]))

#stores the exif data in byte format into the mentioned file
with open('exif_data.txt', 'w') as file:
    file.write(str(tags))
