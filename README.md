# 👁️ Real-Time Color Blindness Filter

A live video filtering application designed to help people with color vision deficiencies (CVD) see critical details in images, graphs, and videos. 

As a colorblind person myself, I understand how important it is to distinguish subtle color differences. This tool captures live video from any connected source (or a virtual camera mirroring your screen), processes it through an extensive mathematical filtering algorithm, and outputs a color-corrected feed in real-time.

## ✨ Features
* **Real-Time Processing:** Applies heavy mathematical color transformations to live video feeds.
* **Multiple Deficiency Modes:** Select the specific type of color blindness to correct (e.g., Tritanopia, Deuteranopia, Protanopia).
* **Flexible Input Sources:** Automatically detects and lets you choose from any available video ports connected to your machine.
* **Simple GUI:** Built using [Gooey](https://github.com/chriskiehl/Gooey) to wrap the complex Python backend into an easy-to-use desktop interface.

## ⚡ Performance Note
Because the core of this application relies on deep, pixel-by-pixel mathematical transformations, it is highly CPU-intensive. On my personal machine, it runs at approximately 15 FPS. Performance will scale significantly on devices with more powerful processors.

---

## 📸 Screenshots & Demos

### Application Interface
The GUI allows you to easily select the deficiency type and the video input port:

![Dalton GUI Interface](https://github.com/user-attachments/assets/c96b7dd1-810d-41b8-8722-762669fdabd4)

### Correction Example (Tritanopia)
Here is an example demonstrating the mathematical color shift on a standard color vision test.

| Before Correction | After Tritanopia Correction |
| :---: | :---: |
| ![Original Image](https://github.com/user-attachments/assets/4c33d394-2bcb-41ad-88a7-2143dc69740d) | ![Corrected Image](https://github.com/user-attachments/assets/9ff5f718-27e2-43e4-9471-2ef5e66c051e) |

---

## 🙏 Credits & Inspiration
The mathematical approach and foundational inspiration for this project were drawn from [joergdietrich/daltonize](https://github.com/joergdietrich/daltonize).
