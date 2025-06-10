# Financial Agent: Conversational Financial Analysis Tool

A conversational financial analysis tool using [agno](https://github.com/agnos-ai/agno) agents for web search and financial data.

## Features

- **Conversational interface** for financial queries
- **Web search integration** (DuckDuckGo)
- **Financial data analysis** (Yahoo Finance)
- **Multi-agent teamwork** for comprehensive answers
- **Context-aware responses** with sources and tables

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Aditya-4987/Financial_agent-very-basic-.git
   cd financial-agent
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file if your agno agents require API keys or secrets (see [agno documentation](https://github.com/agnos-ai/agno)).

## Usage

Run the script:

```sh
python financial_agent.py
```

You will be prompted to enter your financial questions.  
Type `quit`, `exit`, or `q` to stop the program.

## Example

```
Enter your question (or 'quit' to exit): What is the latest news about TATAMOTORS.NS?
```

## Notes

- This tool uses the [agno](https://github.com/agnos-ai/agno) library for multi-agent orchestration.
- Make sure you have the necessary API keys if required by agno or its tools.

## License

MIT License