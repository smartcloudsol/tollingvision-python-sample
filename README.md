# Python Example Program for Tolling Vision

This repository contains a sample Python application that demonstrates how to use [Tolling Vision](https://tollingvision.com). Tolling Vision is a Dockerized service for tolling companies utilizing AI-based recognition engines. It extracts ANPR/ALPR (Automatic Number Plate Recognition), MMR (Make and Model Recognition), and ADR (Dangerous Goods Signs Recognition) information from images and image sequences.

Tolling Vision is highly scalable and can be easily integrated into existing systems via gRPC (visit our [How to use Tolling Vision](https://tollingvision.com/how-to-use-tolling-vision/) tutorial for more details), enabling seamless image analysis directly within your application pipeline. The sample program in this repository specifically utilizes the `analyze` function of the TollingVisionService, which is designed for complex analysis scenarios. This function processes multiple images of a vehicle — such as front, rear, and overview shots — to determine the front and rear license plates, as well as to extract MMR (Make and Model recognition) information.

## 📖 Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: Make sure you have Python 3.6 or higher installed.
- **Tolling Vision Python Client**: Ensure [Tolling Vision Python Client](https://pypi.org/project/tollingvision-scsinfo/) is installed on your system.
- **Tolling Vision**: Tolling Vision application should be installed and running. See our [Get Started](https://tollingvision.com/get-started) page for detailed instructions.

## 📋 Instructions

### 💻 Install dependencies

Use PIP to install dependencies:
```bash
pip install grpcio-tools tollingvision-scsinfo
```

### 👨‍💻 Clone the Repository

```bash
git clone https://github.com/smartcloudsol/tollingvision-python-sample.git
cd tollingvision-python-sample
```

### 🚘 Run the Sample

You can run the application using the following command:
```bash
python3 tollingvision-sample.py <ADDRESS> <SECURED> <THREAD_COUNT> <IMAGE_FOLDER> <RESULT_FILE> <GROUP_PATTERN> <FRONT_PATTERN> <REAR_PATTERN> <OVERVIEW_PATTERN>
```

Explanation of Parameters:
  - **ADDRESS**: The address of the Tolling Vision service in <code>ip:port</code> format.
  - **SECURED**: <code>True</code>/<code>False</code> to indicate whether the communication channel is encrypted (SSL/TLS).
  - **THREAD_COUNT**: Number of parallel requests to the Tolling Vision service (set this to the number of images you want to process simultaneously, up to the maximum allowed by your license).
  - **IMAGE_FOLDER**: Directory path containing the images to be processed.
  - **RESULT_FILE**: Path to the file where the results will be saved in CSV format.
  - **GROUP_PATTERN**: Regular expression used to group images for the analyze function (e.g., <code>"^.{7}"</code> - based on the first 7 characters of the file names).
  - **FRONT_PATTERN**: Regular expression to identify front images within each group (e.g., <code>".\*front.\*"</code> - files in the group that contains the "front" word).
  - **REAR_PATTERN**: Regular expression to identify rear images within each group (e.g., <code>".\*rear.\*"</code> - files in the group that contains the "rear" word).
  - **OVERVIEW_PATTERN**: Regular expression to identify overview images within each group (e.g., <code>".\*scene.\*"</code> - files in the group that contains the "scene" word).
