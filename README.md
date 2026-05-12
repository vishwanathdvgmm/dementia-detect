# Dementia Detect

Dementia Detect is an end-to-end clinical AI application designed for the automated classification and progression analysis of Alzheimer's Disease using high-resolution axial MRI slices.

The system utilizes an **EfficientNet-B4** convolutional neural network, fine-tuned via transfer learning, to categorize MRI scans into clinical stages. It features a robust **GradCAM** (Gradient-weighted Class Activation Mapping) integration that provides transparent, explainable visualizations of the neural network's regions of interest (e.g., Hippocampus, Entorhinal Cortex).

## Features

- **Automated Inference**: Instant classification across 4 stages (NonDemented, VeryMildDemented, MildDemented, ModerateDemented).
- **Explainable AI (XAI)**: Interactive GradCAM overlays that highlight the specific neurological regions driving the model's prediction.
- **Clinical Interface**: A precision-focused, dark-themed UI built for medical professionals.
- **Comprehensive Reporting**: Generates downloadable, styled PDF reports containing the patient ID, diagnostic confidence, and side-by-side ROI imagery.
- **Demo Mode**: Includes a built-in positive sample for immediate stakeholder demonstration.

## Technology Stack

- **AI Pipeline**: PyTorch, Torchvision (`EfficientNet-B4`), Grad-CAM, OpenCV.
- **Backend API**: FastAPI, Uvicorn, Python 3.10.
- **Frontend**: React, Vite, Tailwind CSS v4, Lucide React.
- **Reporting**: ReportLab.

---

## Local Development Setup

To run this application locally, you will need two terminal windows: one for the FastAPI backend and one for the React frontend.

### 1. Backend Setup (FastAPI)

1. Open a terminal and navigate to the project root:
    ```bash
    cd dementia-detect
    ```
2. Create and activate a Python virtual environment:

    ```bash
    python -m venv .venv

    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```

3. Install the required backend dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```
4. Start the FastAPI server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    _The backend will now be running at `http://localhost:8000`._

### 2. Frontend Setup (React/Vite)

1. Open a **second terminal** and navigate to the frontend directory:
    ```bash
    cd dementia-detect/frontend
    ```
2. Install the Node.js dependencies:
    ```bash
    npm install
    ```
3. Start the Vite development server:
    ```bash
    npm run dev
    ```
    _The frontend will now be running at `http://localhost:5173`._

---

## Usage Guide

1. Open your browser and navigate to `http://localhost:5173`.
2. **Acquire MRI Scan**: Drag and drop an axial MRI slice (JPG/PNG) into the upload zone, or click the **"Load Clinical Demo Scan"** button to automatically run a pre-configured ModerateDemented case.
3. **Viewer & Analytics**: Review the model's primary diagnosis, confidence scores, and probability breakdown.
4. **GradCAM Toggle**: Use the "Toggle Heatmap" button to swap between the raw MRI input and the neural network's activation heatmap.
5. **Clinical Report**: Click "Generate Report" to navigate to the summary page, then click "Export PDF Report" to download a formalized PDF of the findings.

## License

_This software is designed for research and demonstrative purposes only and is not certified for clinical diagnostic use._
