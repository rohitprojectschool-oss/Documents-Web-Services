# Stage 1: Build Frontend
FROM node:20-slim AS frontend-build
WORKDIR /frontend
# Using public URL for the build to avoid auth issues in Docker
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/rohitprojectschool-oss/Documents-Web-UI.git .
RUN npm install
RUN npm run build

# Stage 2: Final Backend Image
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy built frontend from Stage 1
COPY --from=frontend-build /frontend/dist ./dist

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
