# 1. Use the official Playwright Python image. 
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements first to leverage Docker layer caching.
COPY requirements.txt .

# 4. Install Python dependencies and clean cache to keep it "light"
RUN pip install --no-cache-dir -r requirements.txt

# 5. install only Chrome
RUN playwright install chromium

# 6. copy rest of project
COPY . .

# 7. Default command to run tests
CMD ["pytest"]