# 🧪 Testing Docker Setup

Quick guide to test if your Docker setup is working correctly.

## Prerequisites Check

1. **Verify Docker is installed and running**:
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Ensure you have required files**:
   - `.env` file with your API keys
   - `cv.pdf` - Your resume
   - `background.txt` - Background information

## Step-by-Step Testing

### Step 1: Build the Docker Image

```bash
docker-compose build
```

**Expected output**: Should complete without errors, showing "Successfully built" message.

**If you see errors**: Check that all files are present and Docker is running.

### Step 2: Start the Container

```bash
docker-compose up
```

**Expected output**: You should see Jupyter Lab starting up with messages like:
```
[I 2024-XX-XX XX:XX:XX.XXX ServerApp] Jupyter Server X.X.X is running at:
[I 2024-XX-XX XX:XX:XX.XXX ServerApp] http://0.0.0.0:8888/lab
```

**Keep this terminal open** - the container runs in the foreground.

### Step 3: Test Jupyter Lab

1. **Open your browser** and go to: `http://localhost:8888`
2. **You should see**: Jupyter Lab interface
3. **Open `Lab1.ipynb`** from the file browser
4. **Run the first cell** - it should import all packages without errors

**✅ Success indicators**:
- Jupyter Lab loads in browser
- No import errors in the notebook
- All cells can execute

### Step 4: Test the Application

1. **Run all cells** in `Lab1.ipynb` in order
2. **When you reach the Gradio cell**, it should:
   - Launch the Gradio interface
   - Show a message like: "Running on local URL: http://127.0.0.1:7860"
   - Display a public URL if `share=True`

3. **Open the Gradio URL** in your browser
4. **Test the chat interface**:
   - Type a question like "Tell me about your experience"
   - The assistant should respond
   - Check that streaming works (text appears incrementally)

**✅ Success indicators**:
- Gradio interface loads
- Can send messages
- Receives responses
- Streaming works (if implemented)

### Step 5: Test Pushover (Optional)

If you have Pushover configured:
1. **Ask a question the agent can't answer** (should trigger `record_unknown_question`)
2. **Express interest** (should trigger `record_recruiters_interest`)
3. **Check your Pushover app** - you should receive notifications

## Running in Background (Detached Mode)

To run the container in the background:

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

## Common Issues and Solutions

### Issue: "Port already in use"

**Solution**: Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8889:8888"  # Use 8889 instead of 8888
  - "7861:7860"  # Use 7861 instead of 7860
```

### Issue: "Cannot connect to Docker daemon"

**Solution**: Make sure Docker Desktop is running

### Issue: "Module not found" errors

**Solution**: Rebuild the image:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Issue: ".env file not found"

**Solution**: Make sure `.env` exists in the project root:
```bash
# Create .env file
touch .env
# Add your keys
nano .env  # or use your editor
```

### Issue: "cv.pdf not found"

**Solution**: Make sure `cv.pdf` exists in the project root directory

## Quick Test Script

You can also run this quick test:

```bash
# Build and start
docker-compose up --build -d

# Wait a few seconds for startup
sleep 5

# Check if container is running
docker-compose ps

# Check logs
docker-compose logs

# Test if Jupyter is accessible (should return HTML)
curl http://localhost:8888

# Stop
docker-compose down
```

## Verification Checklist

- [ ] Docker builds without errors
- [ ] Container starts successfully
- [ ] Jupyter Lab accessible at http://localhost:8888
- [ ] Can open and run notebook cells
- [ ] No import errors
- [ ] Gradio launches when running the notebook
- [ ] Gradio interface is accessible
- [ ] Can send messages and receive responses
- [ ] Streaming works (if implemented)
- [ ] Pushover notifications work (if configured)

If all items are checked, your Docker setup is working correctly! 🎉

