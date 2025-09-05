# 🤖 Annoying Assistant

The **Annoying Assistant** is a virtual assistant designed to be deliberately irritating.  
He takes his sweet time performing simple tasks, occasionally plays hide-and-seek, and will bore you with random facts just when you don’t need them.

---

## ✨ Features

- Open and close applications on your machine  
- Ask and answer simple questions  
- Navigate to specific URLs on command  
- Perform a Google search if he doesn’t know the answer—and redirect you to the results  

---

## ⚙️ Requirements

1. Install **[Ollama](https://ollama.com)**  
   This project relies on Ollama for running language models.  

2. Install a model  
   We recommend **`qwen3:8b`**, which balances performance and size.  

   Run the following in your terminal:
   ```bash
   ollama run qwen3:8b


## 🖥️ Installation and Setup

### Clone the Repository
```bash
git clone git@github.com:taaziz1/annoying-assistant.git
```

### Create and Activate Virtual Environment

**Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Install Dependencies

Dependencies are listed in `requirements.txt`. Install them using:
```bash
pip3 install -r requirements.txt
```

