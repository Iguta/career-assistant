# 🤖 Career Assistant – ChatGPT-Powered

A career assistant application that uses ChatGPT to answer recruiter questions based on your CV and background information. The application features a Gradio-based web interface for interactive Q&A sessions.

## 📋 Features

- **Automatic Profile Extraction**: Builds a structured career profile from your CV (PDF) and background information
- **Interactive Q&A Interface**: Gradio-based web UI for recruiter questions
- **ChatGPT Integration**: Uses OpenAI's GPT models to generate professional responses

## 🎨 About Gradio

[Gradio](https://www.gradio.app/) is an open-source Python library that makes it easy to build and share interactive web interfaces for machine learning models and Python functions. In this project, Gradio provides the user-friendly web interface where recruiters can ask questions and receive AI-generated responses in real-time.

**Key benefits of Gradio:**
- **Easy to use**: Create web UIs with just a few lines of Python code
- **No frontend knowledge required**: Build beautiful interfaces without HTML, CSS, or JavaScript
- **Automatic sharing**: Gradio can create public links to share your interface (via `share=True`)
- **Real-time streaming**: Supports streaming responses for a smooth user experience
- **Built-in components**: Pre-built components like chatbots, text inputs, and buttons

When you run the notebook, Gradio automatically launches a web interface in your browser where you can interact with the career assistant. The interface is accessible locally and can be shared publicly if needed.

## 🛠️ Prerequisites

**Choose one setup method:**

### For Docker Setup (Recommended):
- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- **Git** - Version control system ([Download Git](https://git-scm.com/downloads))
- **OpenAI API key** - ([Get one here](https://platform.openai.com/api-keys))
- **Pushover account** - For receiving notifications (see setup instructions below)
- **A PDF resume/CV file** - Your resume in PDF format
- **A background information text file** - Additional context about your background

### For Manual Setup:
- **Git** - Version control system ([Download Git](https://git-scm.com/downloads))
- **Python 3.12 or higher** - Programming language runtime (required for `openai-agents` package)
- **OpenAI API key** - ([Get one here](https://platform.openai.com/api-keys))
- **Pushover account** - For receiving notifications (see setup instructions below)
- **A PDF resume/CV file** - Your resume in PDF format
- **A background information text file** - Additional context about your background
- **Code Editor** - Use your favorite editor like [Cursor](https://cursor.sh/) or [VS Code](https://code.visualstudio.com/)

## 🚀 Setup Instructions

### Option A: Docker Setup (Recommended - No Compatibility Issues!)

Docker ensures everyone runs the exact same environment, eliminating Python version and dependency compatibility issues.

#### Prerequisites for Docker:
- **Docker Desktop** - [Download for Windows/Mac](https://www.docker.com/products/docker-desktop/) or install Docker Engine for Linux
- **Docker Compose** - Usually included with Docker Desktop

#### Quick Start with Docker:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd career-assistant
   ```

2. **Create your `.env` file** (if you haven't already):
   ```bash
   # Create .env file with your API keys
   OPENAI_API_KEY=your_openai_api_key_here
   PUSHOVER_USER=your_pushover_user_key_here
   PUSHOVER_TOKEN=your_pushover_api_token_here
   ```

3. **Ensure you have your files**:
   - `cv.pdf` - Your resume/CV
   - `background.txt` - Your background information

4. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

5. **Access the application**:
   - **Jupyter Lab**: Open http://localhost:8888 in your browser
   - **Gradio** (after running notebook): Will be available at http://localhost:7860

6. **Test if it's working**:
   - Open Jupyter Lab at http://localhost:8888
   - Open `Lab1.ipynb` and run the first cell
   - If imports work without errors, Docker setup is successful!
   - See `TEST_DOCKER.md` for detailed testing instructions

#### Docker Commands:

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Stop the container
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up --build
```

#### Manual Docker (without docker-compose):

```bash
# Build the image
docker build -t career-assistant .

# Run the container
docker run -it --rm \
  -p 8888:8888 \
  -p 7860:7860 \
  -v $(pwd)/.env:/app/.env:ro \
  -v $(pwd)/cv.pdf:/app/cv.pdf:ro \
  -v $(pwd)/background.txt:/app/background.txt:ro \
  -v $(pwd)/Lab1.ipynb:/app/Lab1.ipynb \
  career-assistant
```

**Benefits of Docker:**
- ✅ No Python version issues - uses Python 3.13
- ✅ No dependency conflicts - isolated environment
- ✅ Works the same on Windows, Mac, and Linux
- ✅ Easy to share and deploy
- ✅ No need to run setup scripts manually

---

### Option B: Manual Setup (Local Installation)

### 0. Verify Python Version

**Important**: This project requires Python 3.12 or higher. Check your Python version:

```bash
python --version
# or
python3 --version
```

If you see Python 3.11 or earlier, you'll need to upgrade:
- **Windows/macOS**: Download Python 3.12+ from [python.org](https://www.python.org/downloads/)
- **Linux**: Use your package manager to install Python 3.12+

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
- `nest-asyncio` - For nested event loops in Jupyter notebooks
- `openai-agents` - OpenAI Agents SDK

### 2.5. Apply Uvicorn Compatibility Patch (Important!)

**⚠️ Required for Python 3.12+ users:** Due to a compatibility issue between `nest-asyncio` and `uvicorn`, you need to apply a patch after installing dependencies. This is especially important if you're using Python 3.13+.

Run the setup script:

```bash
python setup_uvicorn_patch.py
```

**What this does:**
- Patches uvicorn to work with `nest-asyncio` (required for Jupyter notebooks)
- Fixes the `loop_factory` parameter compatibility issue
- Only needs to be run once after installing dependencies

**Note:** If you see "✅ Uvicorn is already patched!", you're all set. If you encounter errors, make sure:
1. Your virtual environment is activated
2. You've run `pip install -r requirements.txt` first
3. You're running the script from the project root directory

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

3. **Open the Jupyter notebook** `Lab1.ipynb`

4. **Make sure your virtual environment is activated** and has all dependencies installed

5. **Apply the uvicorn patch** (if you haven't already):
   ```bash
   python setup_uvicorn_patch.py
   ```

6. **Run all cells in the notebook**

7. **The Gradio interface will launch automatically** in your browser

8. **Enter recruiter questions** in the interface to get AI-generated responses based on your profile

9. **Receive notifications** via Pushover when:
   - Recruiters express interest in your profile
   - Questions are asked that you can't answer (so you can follow up)

## 📁 Project Structure

```
career-assistant/
├── Lab1.ipynb              # Main Jupyter notebook
├── requirements.txt         # Python dependencies
├── setup_uvicorn_patch.py  # Setup script for uvicorn compatibility patch
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Files to exclude from Docker build
├── README.md               # This file
├── .env                    # Environment variables (create this - not tracked by git)
├── .gitignore              # Git ignore rules
├── cv.pdf                  # Your resume/CV (or Resume.pdf)
└── background.txt          # Background information
```

## 🔧 Troubleshooting

- **ModuleNotFoundError**: Make sure your virtual environment is activated and you've run `pip install -r requirements.txt`
- **API Key Error**: Verify your `.env` file exists and contains valid `OPENAI_API_KEY`, `PUSHOVER_USER`, and `PUSHOVER_TOKEN`
- **File Not Found**: Check that `cv.pdf` (or `Resume.pdf`) and `background.txt` exist in the project directory
- **KeyError: ~TContext when importing agents**: 
  - This error occurs when using Python 3.11 or earlier
  - **Solution**: The `openai-agents` package requires **Python 3.12 or higher**
  - Upgrade Python to 3.12+ and recreate your virtual environment:
    ```bash
    # Check your Python version
    python --version
    
    # If it's < 3.12, install Python 3.12+ from python.org
    # Then recreate your virtual environment:
    python -m venv venv
    venv\Scripts\activate  # Windows
    # or: source venv/bin/activate  # macOS/Linux
    pip install -r requirements.txt
    ```
- **Uvicorn/Gradio Launch Error (TypeError: loop_factory)**: 
  - This is a compatibility issue between `nest-asyncio` and `uvicorn` on Python 3.12+
  - **Solution 1 (Automated)**: Run `python setup_uvicorn_patch.py` after installing dependencies
  - Make sure your virtual environment is activated when running the patch script
  - **Solution 2 (Manual)**: If the automated script fails, see "Manual Patching Instructions" below
  - If the error persists, check that you're using Python 3.12 or higher
- **Pushover Notifications Not Working**: 
  - Verify your Pushover credentials are correct in the `.env` file
  - Make sure you're logged into the Pushover app on your device
  - Check that your Pushover account is active (free trial or paid)
- **Git Issues**: Make sure Git is installed and accessible from your command line (`git --version`)
- **Docker Issues**: 
  - Make sure Docker Desktop is running
  - Check Docker version: `docker --version` and `docker-compose --version`
  - If you get permission errors on Linux, add your user to the docker group: `sudo usermod -aG docker $USER`
  - If ports are already in use, change the port mappings in `docker-compose.yml`
  - If the container won't start, check logs: `docker-compose logs`

## 🔨 Manual Patching Instructions (Fallback)

If the automated `setup_uvicorn_patch.py` script fails, you can manually patch uvicorn:

### Step 1: Locate the File

Find the uvicorn `_compat.py` file in your virtual environment:

**Windows:**
```
venv\Lib\site-packages\uvicorn\_compat.py
```

**macOS/Linux:**
```
venv/lib/python3.x/site-packages/uvicorn/_compat.py
```

### Step 2: Open and Edit the File

Open `_compat.py` in your text editor and find the section for Python 3.12+ or 3.13+.

### Step 3: Replace the Code

**For Python 3.13+**, find this line:
```python
if sys.version_info >= (3, 13):
    asyncio_run = asyncio.run
```

Replace it with:
```python
if sys.version_info >= (3, 13):
    # Workaround for nest_asyncio compatibility: nest_asyncio patches asyncio.run()
    # and the patched version doesn't support loop_factory parameter.
    # This wrapper accepts loop_factory for compatibility but ignores it when calling
    # the potentially-patched asyncio.run().
    def asyncio_run(
        main: Coroutine[Any, Any, _T],
        *,
        debug: bool = False,
        loop_factory: Callable[[], asyncio.AbstractEventLoop] | None = None,
    ) -> _T:
        # Call asyncio.run() without loop_factory to work with nest_asyncio's patched version
        # Python 3.13+ still supports loop_factory, but nest_asyncio's patch doesn't
        return asyncio.run(main, debug=debug)
```

**For Python 3.12**, find this line:
```python
elif sys.version_info >= (3, 12):
    asyncio_run = asyncio.run
```

Replace it with:
```python
elif sys.version_info >= (3, 12):
    # For Python 3.12, nest_asyncio may also patch asyncio.run(), so we need
    # a wrapper that handles loop_factory compatibility
    def asyncio_run(
        main: Coroutine[Any, Any, _T],
        *,
        debug: bool = False,
        loop_factory: Callable[[], asyncio.AbstractEventLoop] | None = None,
    ) -> _T:
        # Try to use loop_factory if nest_asyncio hasn't patched asyncio.run()
        try:
            return asyncio.run(main, debug=debug, loop_factory=loop_factory)
        except TypeError:
            # nest_asyncio's patched version doesn't support loop_factory
            return asyncio.run(main, debug=debug)
```

### Step 4: Save and Test

Save the file and try running your Gradio application again. The error should be resolved.

**Note**: If you reinstall uvicorn or recreate your virtual environment, you'll need to apply this patch again.

## 📝 Notes

- The application uses GPT-4o for profile extraction and answering questions
- Make sure you have sufficient OpenAI API credits
- The Gradio interface will display a local URL when launched (typically `http://127.0.0.1:7860`)
- Pushover notifications are optional - the app will work without them, but you won't receive alerts about recruiter interest or unanswered questions
- You can use any code editor you prefer - Cursor and VS Code are both excellent choices
- **Python Version Requirement**: This project requires **Python 3.12 or higher**. The `openai-agents` package uses typing features that are only available in Python 3.12+. If you're using Python 3.11 or earlier, you'll get a `KeyError: ~TContext` error when importing the agents module.
- **Python 3.12+ Compatibility**: If you're using Python 3.12 or 3.13+, you must run `setup_uvicorn_patch.py` after installing dependencies. This patches uvicorn to work with `nest-asyncio` (required for Jupyter notebooks). The patch is safe and only affects the compatibility layer.

## 📄 License

This project is for personal/educational use.

