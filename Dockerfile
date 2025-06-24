FROM node:20-bullseye-slim

# Install Python
RUN apt update && apt install -y python3 python3-pip python3-venv

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "toolsv2.py"]

