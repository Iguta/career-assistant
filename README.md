# 🤖 Career Assistant – ChatGPT-Powered

A career assistant application that uses ChatGPT to answer recruiter questions based on your CV and background information. The application features a Gradio-based web interface for interactive Q&A sessions.

## 📋 Features

- **Automatic Profile Extraction**: Builds a structured career profile from your CV (PDF) and background information
- **Interactive Q&A Interface**: Gradio-based web UI for recruiter questions
- **ChatGPT Integration**: Uses OpenAI's GPT models to generate professional responses

## 🛠️ Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- A PDF resume/CV file
- A background information text file

## 🚀 Setup Instructions

### 1. Create a Python Virtual Environment

#### On Windows:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

Once your virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `openai` - OpenAI API client
- `gradio` - Web UI framework
- `pypdf` - PDF text extraction
- `python-dotenv` - Environment variable management

### 3. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# Create .env file
touch .env
```

Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

**Note**: Make sure to add `.env` to your `.gitignore` file to keep your API key secure.

### 4. Prepare Your Files

Ensure you have the following files in the project directory:
- `cv.pdf` or `Resume.pdf` - Your resume in PDF format
- `background.txt` - A text file containing additional background information

**Note**: If your files have different names, update the file paths in the notebook accordingly.

## 📖 Usage

1. Open the Jupyter notebook `lab_1.ipynb`
2. Make sure your virtual environment is activated and has all dependencies installed
3. Run all cells in the notebook
4. The Gradio interface will launch automatically in your browser
5. Enter recruiter questions in the interface to get AI-generated responses based on your profile

## 📁 Project Structure

```
career-assistant/
├── lab_1.ipynb          # Main Jupyter notebook
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Environment variables (create this)
├── Resume.pdf          # Your resume/CV
└── backrounds.txt      # Background information
```

## 🔧 Troubleshooting

- **ModuleNotFoundError**: Make sure your virtual environment is activated and you've run `pip install -r requirements.txt`
- **API Key Error**: Verify your `.env` file exists and contains a valid `OPENAI_API_KEY`
- **File Not Found**: Check that `cv.pdf` (or `Resume.pdf`) and `background.txt` exist in the project directory

## 📝 Notes

- The application uses GPT-4o-mini for profile extraction and GPT-4o for answering questions
- Make sure you have sufficient OpenAI API credits
- The Gradio interface will display a local URL when launched (typically `http://127.0.0.1:7860`)

## 📄 License

This project is for personal/educational use.

