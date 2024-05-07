# Image Compressor

## Description
This project is an image compression tool that allows users to optimize their images to reduce file size without significantly affecting quality. The software supports various image formats including JPG, JPEG, PNG, BMP, and GIF. It features a GUI built with CustomTkinter, making it user-friendly and accessible for both technical and non-technical users.

## Features
- Support for multiple image formats.
- Automatic quality adjustment based on image size.
- Display of optimization progress and results.
- Simple and intuitive graphical user interface.

## Compression Example

Below is a visual comparison between an original image and its compressed version using our Image Compressor. The example demonstrates the effectiveness of the compression with minimal loss of quality.

<table>
  <tr>
    <th>Original Image</th>
    <th>Compressed Image</th>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/Emy69/Image-Compressor/blob/main/resources/Example/Original.png" alt="Original Image" width="300"/>
      <br>
      Size: 1.35 MB
    </td>
    <td>
      <img src="https://github.com/Emy69/Image-Compressor/blob/main/resources/Example/Compressed.png" alt="Compressed Image" width="300"/>
      <br>
      Size: 0.98 MB
    </td>
  </tr>
</table>

As shown in the table above, the compressed version retains substantial visual quality while significantly reducing the file size. This example used a compression setting that balances quality with file size reduction.



## Running the Application

Follow these steps to optimize your images:

1. **Start the Application**: Double-click the executable (`.exe`) to launch the application.

2. **Upload Images**: 
   - Click on the **Upload Images** button within the application.

3. **Optimize Images**:
   - After selecting the images, click on the **Open** button. The images will be automatically optimized.

4. **Save Optimized Images**:
   - The optimized images will be automatically saved in a folder named `optimized`.
   - This folder will be located in the same directory where your executable (`.exe`) is located.


## Downloads

- **Download the Latest Version**: Visit the [releases page](https://github.com/Emy69/Image-Compressor/releases) to download the latest version of the application.

### Installation

#### Prerequisites
- Python 3.6 or higher. Ensure `tkinter` is installed, which is included with many Python installations. On some Linux distributions, you may need to install it separately via your package manager.

#### Setup
Clone this repository and navigate into the project directory. Install the required dependencies with:
```bash
git clone https://github.com/Emy69/Image-Compressor.git
```
```bash
pip install -r requirements.txt
