```markdown
# Cool Voice Assistant

Welcome to **Cool Voice Assistant**—a local voice assistant that listens to your commands, transcribes them with Whisper, and generates responses using GPT-3.5 Turbo. This project keeps all voice processing on your machine for fast, secure, and private interactions.

---

## Features

- **Voice Input:** Capture your commands via your microphone.
- **Speech-to-Text:** Transcribe audio using OpenAI's Whisper.
- **Conversational AI:** Generate smart responses with GPT-3.5 Turbo.
- **Text-to-Speech:** Hear responses via pyttsx3 (or macOS’s `say` command).
- **Local Execution:** All processing is done locally—no cloud dependency for voice processing.

---

## Prerequisites

- **Python 3.7+**
- **ffmpeg:** Required for audio decoding.
- **Virtual Environment (recommended):** Keep dependencies tidy.
- **Python Packages:**
  - `speech_recognition`
  - `openai`
  - `openai-whisper`
  - `pyttsx3`
  - `python-dotenv` (if using a `.env` file for your API key)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/cool-voice-assistant.git
   cd cool-voice-assistant
   ```

2. **Set Up a Virtual Environment:**

   ```bash
   python -m venv .venv
   ```

   Activate the environment:

   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```

3. **Install Dependencies:**

   If you have a `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

   Or install packages manually:
   ```bash
   pip install speechrecognition openai openai-whisper pyttsx3 python-dotenv
   ```

4. **Set Up Your API Key:**

   Create a file named **.env** in the project root with the following content:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Install ffmpeg:**

   - **Windows:**  
     Download from [ffmpeg.org](https://ffmpeg.org/download.html) or install via Chocolatey:
     ```powershell
     choco install ffmpeg
     ```
   - **Linux/macOS:**  
     Use your package manager (e.g., `sudo apt install ffmpeg` on Ubuntu).

   **Ensure ffmpeg is added to your system's PATH.**

---

## Usage

Run the assistant with:

```bash
python testmain.py
```

The assistant will:
1. Calibrate your microphone.
2. Listen for your voice prompt.
3. Transcribe your command using Whisper.
4. Process the prompt via GPT-3.5 Turbo.
5. Speak out the response.

Talk naturally and enjoy the seamless interaction!

---

## Troubleshooting

- **ffmpeg Not Found:**  
  Verify that ffmpeg is installed and its executable is in your system PATH. Try running:
  ```bash
  ffmpeg -version
  ```
- **Microphone Issues:**  
  Ensure your microphone is connected and working. To list available devices:
  ```python
  import speech_recognition as sr
  print(sr.Microphone.list_microphone_names())
  ```
- **API Key Issues:**  
  Confirm your `.env` file is correctly formatted and in the right location. You can debug by printing the API key in your code:
  ```python
  import os
  print(os.getenv("OPENAI_API_KEY"))
  ```

---

## Contributing

Contributions are welcome! Feel free to fork the repository, open issues, or submit pull requests. Let’s build something cool together.

---

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for more details.

---

Enjoy building and interacting with your very own voice assistant. Happy coding!
```
