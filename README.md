# 🖼️ Elsakr Image Converter

<p align="center">
  <img src="assets/Sakr-logo.png" alt="Elsakr Logo" width="120">
</p>

<p align="center">
  <strong>Batch convert images between different formats</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python">
  <img src="https://img.shields.io/badge/Platform-Windows-green?style=flat-square&logo=windows">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square">
</p>

---

## ✨ Features

- 🖼️ **Multi-format Support**: PNG, JPEG, WebP, BMP, TIFF, GIF, ICO
- 📦 **Batch Conversion**: Convert multiple files at once
- 🎚️ **Quality Control**: Adjustable quality for lossy formats
- 📂 **Folder Import**: Add entire folders of images
- 📊 **Statistics**: Track conversions and space saved
- 🌑 **Premium Dark UI**: Modern, sleek interface
- ⚡ **Fast**: Multi-threaded processing

---

## 📸 Screenshot

<p align="center">
  <img src="assets/Screenshot.png" alt="App Screenshot" width="800">
</p>

---

## 🚀 Quick Start

### Option 1: Run from Source

```bash
# Clone the repository
git clone https://github.com/khalidsakrjoker/elsakr-image-converter.git
cd elsakr-image-converter

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Option 2: Download EXE

Download the latest release from [Releases](https://github.com/khalidsakrjoker/elsakr-image-converter/releases).

---

## 🛠️ Build Executable

```bash
pip install pyinstaller

pyinstaller --noconsole --onefile --icon="assets/fav.ico" --name="Elsakr Image Converter" --add-data "assets;assets" main.py
```

---

## 📦 Supported Formats

| Format | Input | Output | Notes |
|--------|-------|--------|-------|
| PNG    | ✅    | ✅     | Lossless |
| JPEG   | ✅    | ✅     | Quality adjustable |
| WebP   | ✅    | ✅     | Quality adjustable |
| BMP    | ✅    | ✅     | Uncompressed |
| TIFF   | ✅    | ✅     | Lossless |
| GIF    | ✅    | ✅     | Animated not supported |
| ICO    | ✅    | ✅     | Icon format |

---

## 📄 License

MIT License - [Elsakr Software](https://elsakr.company)

---

<p align="center">
  Made with ❤️ by <a href="https://elsakr.company">Elsakr</a>
</p>
