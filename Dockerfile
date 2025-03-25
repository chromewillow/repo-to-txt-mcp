FROM node:18-slim

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy Python requirements
COPY requirements.txt ./

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make start script executable
RUN chmod +x smithery-wrapper.js

# Expose port (default MCP port)
EXPOSE 8000

# Set environment variable
ENV PORT=8000

# Start the MCP server
CMD ["node", "smithery-wrapper.js"]