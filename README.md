# Local Retrieval-Augmented Generation (RAG) for PDFs using Ollama

This project implements a command-line interface (CLI) based local retrieval-augmented generation (RAG) application that allows users to interact with PDF documents. It combines the power of **Ollama**, **ChromaDB**, and **uv** for generative AI responses, local retrieval and project management respectively.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Local Retrieval-Augmented Generation (RAG) application allows users to perform CLI-based intelligent document retrieval and conversational AI on their local PDFs. With the integration of **Ollama** (a local LLM), **ChromaDB** (vector database for document storage), and **uv** (a Rust-based Python packaging library), this tool facilitates extracting, searching, and generating insightful responses based on content from a set of PDF files.

This project makes it possible to:

- Perform document-based search.
- Get contextually relevant answers from PDFs.
- Generate text that augments user input based on the content of the document.

**Note**: Currently this project supports CLI based single prompt output. Chain prompting will be included in the further updates along with a chat ui application for ease of access. Refer [Future Work](#future-work) for more information.

## Features

- Local PDF retrieval and processing from data directory.
- Intelligent retrieval and document search using ChromaDB.
- AI-based text generation using Ollama for accurate, context-aware responses.
- Command-line interface for easy usage.
- Efficient dependency management and project setup using uv.

## Technologies Used

- [**Ollama**](https://ollama.com/): Local Language Model (LLM) used for text generation.
- [**ChromaDB**](https://docs.trychroma.com/docs/overview/introduction): Vector database to store and index document embeddings for fast retrieval.
- [**uv**](https://docs.astral.sh/uv/): Rust-based Python packaging library that streamlines dependency management and project setup.
- [**Python**](https://www.python.org/): The programming language used to build this tool.

## Installation

### Prerequisites

- uv installed for efficient dependency management
- Python 3.8+ installed using uv
- Download Ollama to run LLM's locally on your machine.
- Set of local PDF's file you want to process

### Steps to install

1. **Install uv**: **uv** is an extremely fast Python package installer and resolver, written in Rust, and designed as a drop-in replacement for `pip` and `pip-tools` workflows.

   - For macOS and Linux:

     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

   - For Windows:

     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

2. **Clone the repository**:

   ```bash
   git clone https://github.com/NidarshN/local_rag_ollama.git
   cd local_rag_ollama

3. **Initialize the project with uv**:

   ```bash
   uv init
   ```

4. **Install project dependencies**:

   ```bash
   uv install
   ```

5. **Dowload [**Ollama**](https://ollama.com/download) on to your system and set it up according to its installation guides if required. Post installation, start the Ollama server and pull the following models:**

    ```bash
    ollama pull nomic-embed-text
    ollama pull qwen2.5:1.5b
    ```

6. **Configure the environment variables or credentials necessary for the project. A [sample.env](./sample.env) file is provided in the repo for reference.**

## Usage

Once the installation is complete, follow these two steps sequentially:

### 1. Populate the database

There two ways to achieve this:

- Place all the PDF's to be processed in the 'data' folder in the project space and run the populate database command.

    ```bash
    uv run main.py --populate
    ```

    **OR**

- Provide the path to the directory containing the PDF's and run the populate database command as shown below.

    ```bash
    uv run main.py --populate --data-path /path/to/directory/ 
    ```

### 2. Running the Application

To use the RAG tool, run the following command:

```bash
uv run main.py --query-text "your query here"
```

This will process the PDF, perform a local retrieval, and generate a relevant response based on the content of the document.

### Example

```bash
uv run main.py --query-text "What is the main conclusion of this document?"
```

### Available Commands

- `-h`: To display usage of this project.
- `--populate`: To populate the database with the set of PDF documents.
- `--data-path`: Path to the directory containing the PDF files you want to process.
- `--query-text`: The question or prompt you want to ask based on the document's content.

## Future Work

Future enhancements for this project include:

- **Chain Prompting**: Implementing a series of prompts to guide the AI through a multi-step reasoning process, improving the quality and relevance of generated responses.
- **User Interface (UI)**: Developing a graphical user interface to make the tool more accessible to users who prefer not to use the command line.
- **Multi-Modal RAG (MM-RAG)**: Intergrating data from various modalities (text, images, audio, etc) to retrieve more context specific information and generate coherent responses.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
