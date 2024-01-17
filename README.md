# Table Line Detection with OpenCV

This repository contains a Python script for detecting lines in tables using OpenCV. The script uses techniques such as edge detection, Hough Line Transform, and k-means clustering to identify and draw horizontal and vertical lines in an input image.

## Features

- Detects and visualizes horizontal and vertical lines in tables.
- Adjustable parameters using trackbars for vertical and horizontal line spacing.
- Real-time visualization of the line detection with OpenCV windows.

## Getting Started

### Prerequisites

- Python
- OpenCV
- NumPy
- scikit-learn

```
pip install opencv-python numpy scikit-learn
```

### Usage

1. Clone the repository:

```
git clone https://github.com/ynstf/Real-time-Table-Segmentation-and-Line-Extraction-with-OpenCV.git
cd Real-time-Table-Segmentation-and-Line-Extraction-with-OpenCV
```

2. Run the script:

```
python main.py
```

## Acknowledgments

- The script uses OpenCV and scikit-learn for image processing and k-means clustering.
