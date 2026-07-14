# Google Cloud Vision OCR — Installation and Setup

This guide explains how to configure Google Cloud Vision API and run the OCR application on Windows using PowerShell.

## Prerequisites

Make sure the following tools are installed:

- Python 3.10 or later
- Google Cloud CLI
- A Google Cloud account with billing enabled

## 1. Install Google Cloud CLI

Download and install the Google Cloud CLI by following the official documentation:

[Install Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk)

After installation, verify that the `gcloud` command is available:

```powershell
gcloud --version
```

## 2. Authenticate with Google Cloud

Open PowerShell and run:

```powershell
gcloud auth login
```

A browser window will open. Sign in with the Google account associated with your Google Cloud project.

## 3. Create and configure a Google Cloud project

Create a new project from the Google Cloud Console:

[Google Cloud Console](https://console.cloud.google.com/)

After creating the project, configure it as the active project:

```powershell
gcloud config set project YOUR_PROJECT_ID
```

Replace `YOUR_PROJECT_ID` with the ID of your Google Cloud project.

Example:

```powershell
gcloud config set project tank-serial-ocr
```

## 4. Enable the Google Cloud Vision API

Enable the Vision API for the selected project:

```powershell
gcloud services enable vision.googleapis.com
```

You can verify that the API is enabled with:

```powershell
gcloud services list --enabled
```

## 5. Configure Application Default Credentials

Authenticate the local Python application:

```powershell
gcloud auth application-default login
```

This command creates the local credentials used by the Google Cloud Vision client library.

## 6. Create a Python virtual environment

From the project root directory, run:

```powershell
python -m venv .venv
```

> Do not include `Activate.ps1` in the `python -m venv` command. The command only receives the directory where the virtual environment will be created.

## 7. Activate the virtual environment

In Windows PowerShell, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should display the virtual environment name:

```text
(.venv)
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 8. Upgrade `pip`

Run:

```powershell
python -m pip install --upgrade pip
```

## 9. Install the project dependencies

If the project includes a `requirements.txt` file, run:

```powershell
pip install -r requirements.txt
```

Alternatively, install the Google Cloud Vision library directly:

```powershell
pip install google-cloud-vision
```

## 10. Run the OCR application

Execute the application by providing the path to the image:

```powershell
python main.py images/tank_serial.jpeg
```

General usage:

```powershell
python main.py <image_path>
```

Example with another image:

```powershell
python main.py images/tank_example.jpg
```

## Project structure

```text
project/
├── .venv/
├── images/
│   └── tank_serial.jpeg
├── main.py
├── requirements.txt
└── README.md
```

## Common errors

### `gcloud` is not recognized

Restart PowerShell after installing Google Cloud CLI. Then verify the installation:

```powershell
gcloud --version
```

### Unable to create the virtual environment

Make sure you are running only:

```powershell
python -m venv .venv
```

The following command is incorrect:

```powershell
python -m venv .venv .\.venv\Scripts\Activate.ps1
```

The virtual environment must be created first and activated in a separate command.

### Authentication credentials were not found

Run:

```powershell
gcloud auth application-default login
```

### Vision API is disabled

Run:

```powershell
gcloud services enable vision.googleapis.com
```

### Deactivate the virtual environment

When you finish working with the application, run:

```powershell
deactivate
```
