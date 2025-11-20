# 🤖 Career Assistant – ChatGPT-Powered

A career assistant application that uses ChatGPT to answer recruiter questions based on your CV and background information. The application features a Gradio-based web interface for interactive Q&A sessions.

## 📋 Features

- **Automatic Profile Extraction**: Builds a structured career profile from your CV (PDF) and background information
- **Interactive Q&A Interface**: Gradio-based web UI for recruiter questions
- **ChatGPT Integration**: Uses OpenAI's GPT models to generate professional responses

## 🛠️ Prerequisites

- **Git** - Version control system ([Download Git](https://git-scm.com/downloads))
- **Python 3.8 or higher** - Programming language runtime
- **OpenAI API key** - ([Get one here](https://platform.openai.com/api-keys))
- **Pushover account** - For receiving notifications (see setup instructions below)
- **A PDF resume/CV file** - Your resume in PDF format
- **A background information text file** - Additional context about your background
- **Code Editor** - Use your favorite editor like [Cursor](https://cursor.sh/) or [VS Code](https://code.visualstudio.com/)

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

### 3. Set Up Pushover (Optional but Recommended)

Pushover is used to send notifications when recruiters express interest or ask questions you can't answer. It's free for 30 days with no credit card required!

1. **Visit [Pushover.net](https://pushover.net/)** and sign up for an account
2. **Download the Pushover app** on your device:
   - [Android - Google Play](https://play.google.com/store/apps/details?id=net.superblock.pushover)
   - [iOS - App Store](https://apps.apple.com/app/pushover-notifications/id506088175)
3. **Log in** to the Pushover app with your account
4. **Get your credentials**:
   - Go to [Pushover Dashboard](https://pushover.net/dashboard) after logging in
   - Copy your **User Key** (you'll need this)
   - Create an **Application** and copy the **API Token/Key** (you'll need this too)

**Note**: Pushover offers a 30-day free trial with no credit card required. After the trial, it's a one-time purchase per platform.

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# Create .env file
touch .env
```

Add your API keys to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
PUSHOVER_USER=your_pushover_user_key_here
PUSHOVER_TOKEN=your_pushover_api_token_here
```

**Note**: Make sure to add `.env` to your `.gitignore` file to keep your API keys secure. The `.env` file is already configured to be ignored by git.

### 5. Prepare Your Files

Ensure you have the following files in the project directory:
- `cv.pdf` or `Resume.pdf` - Your resume in PDF format
- `background.txt` - A text file containing additional background information

**Note**: If your files have different names, update the file paths in the notebook accordingly.

## 📖 Usage

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd career-assistant
   ```

2. **Open the project** in your favorite editor:
   - [Cursor](https://cursor.sh/) - AI-powered code editor
   - [VS Code](https://code.visualstudio.com/) - Popular code editor
   - Or any other editor you prefer

3. **Open the Jupyter notebook** `Lab2.ipynb` (or `lab_1.ipynb`)

4. **Make sure your virtual environment is activated** and has all dependencies installed

5. **Run all cells in the notebook**

6. **The Gradio interface will launch automatically** in your browser

7. **Enter recruiter questions** in the interface to get AI-generated responses based on your profile

8. **Receive notifications** via Pushover when:
   - Recruiters express interest in your profile
   - Questions are asked that you can't answer (so you can follow up)

## 📁 Project Structure

```
career-assistant/
├── Lab2.ipynb          # Main Jupyter notebook
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Environment variables (create this - not tracked by git)
├── .gitignore          # Git ignore rules
├── cv.pdf              # Your resume/CV (or Resume.pdf)
└── background.txt      # Background information
```

## 🔧 Troubleshooting

- **ModuleNotFoundError**: Make sure your virtual environment is activated and you've run `pip install -r requirements.txt`
- **API Key Error**: Verify your `.env` file exists and contains valid `OPENAI_API_KEY`, `PUSHOVER_USER`, and `PUSHOVER_TOKEN`
- **File Not Found**: Check that `cv.pdf` (or `Resume.pdf`) and `background.txt` exist in the project directory
- **Pushover Notifications Not Working**: 
  - Verify your Pushover credentials are correct in the `.env` file
  - Make sure you're logged into the Pushover app on your device
  - Check that your Pushover account is active (free trial or paid)
- **Git Issues**: Make sure Git is installed and accessible from your command line (`git --version`)

## 📝 Notes

- The application uses GPT-4o for profile extraction and answering questions
- Make sure you have sufficient OpenAI API credits
- The Gradio interface will display a local URL when launched (typically `http://127.0.0.1:7860`)
- Pushover notifications are optional - the app will work without them, but you won't receive alerts about recruiter interest or unanswered questions
- You can use any code editor you prefer - Cursor and VS Code are both excellent choices

## 📄 License

This project is for personal/educational use.

