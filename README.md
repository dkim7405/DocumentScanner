# DocumentScanner
Program that performs document scanning using OpenCV.
It takes an input image, processes it to find a document within the image, and then warps the document to make it appear as if it were scanned flat.
![image](https://github.com/dkim7405/DocumentScanner/assets/122648295/62ca861b-bed4-40c3-bf51-e7709a70a537)
![image](https://github.com/dkim7405/DocumentScanner/assets/122648295/ffde0164-2a92-4ad2-9fb1-8a46996b38b3)
![image](https://github.com/dkim7405/DocumentScanner/assets/122648295/069dfa4b-0553-4a2e-b8b9-24594d84f140)

#Code Structure
*`DocumentScanner` class encapsulates the document scanning process.
*The `scan` method performs the complete document scanning process.
*It includes methods for image thresholding, finding the document blob, identifying corners, reordering corners, and displaying the scanned image.

#Future Improvements
*This program still needs fine tuning to work with different types of documents and lighting conditions.
*Creating a user interface for the program
*Working on saving files (document)
*Creating function to customize capturing the borders of document
*Document image quality improvement

