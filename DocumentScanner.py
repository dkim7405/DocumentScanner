import cv2
import numpy as np

class DocumentScanner:

    def __init__(self, imagePath):
        self.windowName = "Document Scanned"
        self.window = cv2.namedWindow("Document Scanned")
        self.documentImage = cv2.imread(imagePath)

    def scan(self):
        print(self.documentImage.shape)
        documentHeight, documentWidth, documentChannel = self.documentImage.shape
        documentArea = documentWidth * documentHeight

        imgCoordinates = [[[0, 0]],
                          [[documentWidth, 0]],
                          [[documentWidth, documentHeight]],
                          [[0, documentHeight]]]

        copyThreshold = self.thresholdImg().copy()
        contour = self.findDocumentBlob(copyThreshold, documentArea)
        corners = self.findCorners(contour)
        rearrangedCorners = self.cornersToRightOrder(corners, imgCoordinates)

        scannedImg = self.showDocumentFitImg(rearrangedCorners, imgCoordinates, documentWidth, documentHeight)

        cv2.imshow("Document Scanned", scannedImg)

    def thresholdImg(self):
        grayDocument = cv2.cvtColor(self.documentImage, cv2.COLOR_BGR2GRAY)
        grayBlurredDocument = cv2.GaussianBlur(grayDocument, (5, 5), 0)
        threshValue, threshedImage = cv2.threshold(grayBlurredDocument, 200, 255, cv2.THRESH_BINARY)
        
        kernel1 = np.ones((5, 5), np.uint8)
        kernel2 = np.ones((3, 3), np.uint8)

        threshedImage = cv2.dilate(threshedImage, kernel1, iterations=3)
        threshedImage = cv2.erode(threshedImage, kernel2, iterations=3)
        cv2.imshow("ThresholdImg", threshedImage)

        return threshedImage

    def findDocumentBlob(self, threshedImage, areaOfImg):
        contours, hierarchy = cv2.findContours(threshedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(self.documentImage, contours, -1, (0, 255, 0), 3)

        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area > areaOfImg * 0.4:
                return contour
            
        return None
                
    def findCorners(self, rectContour):
        perim = cv2.arcLength(rectContour, True)
        epsilon = 0.02 * perim
        approxCorners = cv2.approxPolyDP(rectContour, epsilon, True)

        print(approxCorners)

        if len(approxCorners) == 4:
            return approxCorners
        else:
            return None
    
    def cornersToRightOrder(self, corners, imgCoordinate):

        newArrangedCorners = []

        for imgCorner in imgCoordinate:
            newArrangedCorner = self.findClosestCorner(corners, imgCorner)
            newArrangedCorners.append(newArrangedCorner)

        return newArrangedCorners
            

    def showDocumentFitImg(self, corners, imgCoordinates, imgWidth, imgHeight):

        numPyArrayImgCorner = np.array(imgCoordinates, np.float32)

        numPyArrayCorner = np.array(corners, np.float32)
        
        print(numPyArrayCorner)
        print(numPyArrayImgCorner)

        h, status = cv2.findHomography(numPyArrayCorner, numPyArrayImgCorner)
        warped = cv2.warpPerspective(self.documentImage, h, (imgWidth,imgHeight))

        return warped
    
    def findClosestCorner(self, corners, imgCorner):
        
        minDistance = self.distance(corners[0][0], imgCorner[0])
        minCorner = corners[0][0]

        for corner in corners:
            if(self.distance(corner[0], imgCorner[0]) < minDistance):
                minDistance = self.distance(corner[0], imgCorner[0])
                minCorner = corner[0]
        
        return [minCorner]

    def distance(self, point1, point2):
        xDiff = point1[0] - point2[0]
        yDiff = point1[1] - point2[1]

        return (xDiff**2 + yDiff**2)**0.5


#-------------------------------------------------------------------------------

documentScanner = DocumentScanner("images/document.jpg")
documentScanner.scan()

imageOriginal = cv2.imread("images/document.jpg")
cv2.imshow("Original", imageOriginal)

while True:
    if cv2.waitKey(0):
        break