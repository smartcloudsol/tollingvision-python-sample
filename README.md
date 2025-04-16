# 🐍 Python Sample Application for Tolling Vision

This repository provides a sample Python application demonstrating how to use [Tolling Vision](https://tollingvision.com) — a Dockerized AI-powered service for tolling companies. Tolling Vision extracts key vehicle data from images or image sequences, including:

- **ANPR/ALPR** – Automatic Number Plate Recognition  
- **MMR** – Make and Model Recognition  
- **ADR** – Dangerous Goods Sign Recognition

Tolling Vision is highly scalable and integrates seamlessly via **gRPC**. For integration guidance, see the [How to use Tolling Vision](https://tollingvision.com/how-to-use-tolling-vision/) tutorial.

This sample leverages the `analyze` function in the `TollingVisionService` to process multiple images of a vehicle — such as **front**, **rear**, and **overview** shots — and extract license plates and vehicle model information.

---

## ✅ Prerequisites

Ensure the following tools are installed:

- **Python 3.6+**
- **Tolling Vision Python Client** — available on [PyPI](https://pypi.org/project/tollingvision-scsinfo/)
- **Tolling Vision service** — running locally or remotely (see [Get Started](https://tollingvision.com/get-started))

---

## 🚀 Getting Started

### 1. 📦 Install Dependencies

Use pip to install the required packages:

```bash
pip install grpcio-tools tollingvision-scsinfo
```

### 2. 🧾 Clone the Repository

```bash
git clone https://github.com/smartcloudsol/tollingvision-python-sample.git
cd tollingvision-python-sample
```

### 3. ▶️ Run the Sample

Run the application with:

```bash
python3 tollingvision-sample.py <ADDRESS> <SECURED> <THREAD_COUNT> <IMAGE_FOLDER> <RESULT_FILE> <GROUP_PATTERN> <FRONT_PATTERN> <REAR_PATTERN> <OVERVIEW_PATTERN>
```

---

## 🧩 Parameter Descriptions

| Parameter         | Description |
|------------------|-------------|
| `<ADDRESS>`       | Address of the Tolling Vision service in `ip:port` format. |
| `<SECURED>`       | `True` or `False` — whether the communication uses SSL/TLS encryption. |
| `<THREAD_COUNT>`  | Number of parallel requests (up to the limit of your license). |
| `<IMAGE_FOLDER>`  | Path to the folder containing images to process. |
| `<RESULT_FILE>`   | File path for saving results (CSV format). |
| `<GROUP_PATTERN>` | Regular expression for grouping images (e.g., `"^.{7}"` — by the first 7 characters). The first match group is used as the key. |
| `<FRONT_PATTERN>` | Regex for identifying front images (e.g., `".*front.*"`). |
| `<REAR_PATTERN>`  | Regex for identifying rear images (e.g., `".*rear.*"`). |
| `<OVERVIEW_PATTERN>` | Regex for identifying overview images (e.g., `".*scene.*"`). |

---

## 📚 Example Usage

```bash
python3 tollingvision-sample.py 192.168.1.100:443 True 4 ./images ./results.csv "^.{7}" ".*front.*" ".*rear.*" ".*scene.*"
```

---

## 📎 Resources

- [Official Website](https://tollingvision.com)
- [How to Use Tolling Vision](https://tollingvision.com/how-to-use-tolling-vision/)
- [Get Started Guide](https://tollingvision.com/get-started)

---

## 🛠️ License

This project is provided for demonstration purposes. See the [LICENSE](./LICENSE) file for more details.
