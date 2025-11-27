# Temporal Interactive Deep Research Demo using OpenAI Agents SDK

This repository builds on the Temporal Interactive Deep Research Demo by @steveandroulakis, adding a Streamlit-based user interface.


For detailed information about the research agents in this repo, see [openai_agents/workflows/research_agents/README.md](openai_agents/workflows/research_agents/README.md)
Access original repo [here](https://github.com/steveandroulakis/openai-agents-demos)


## Prerequisites

1. **Python 3.10+** - Required for the demos
2. **Temporal Cloud Account**
3. **OpenAI API Key** - Set as environment variable `OPENAI_API_KEY` in .env file (note, you will need enough quota on in your [OpenAI account](https://platform.openai.com/api-keys) to run this demo)
4. **PDF Generation Dependencies** - Required for PDF output (optional)
5. Streamlit for UI Interface

### Connect to Temporal Cloud

```bash
# Update Temporal Connection info in .env File
TEMPORAL_API_KEY=''
TEMPORAL_NAMESPACE=''
TEMPORAL_ENDPOINT=''
TEMPORAL_TASK_QUEUE='research-queue'

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Set your OpenAI API key:
   ```bash
   Add OpenAI API key file in the .env
   ```
   OPENAI_API_KEY=''

### PDF Generation (optional)


For PDF generation functionality, you'll need WeasyPrint and its system dependencies:

#### macOS (using Homebrew)
```bash
brew install weasyprint
# OR install system dependencies for pip installation:
brew install pango glib gtk+3 libffi
```

#### Linux (Ubuntu/Debian)
```bash
# For package installation:
sudo apt install weasyprint

# OR for pip installation:
sudo apt install python3-pip libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0
```

#### Linux (Fedora)
```bash
# For package installation:
sudo dnf install weasyprint

# OR for pip installation:
sudo dnf install python-pip pango
```

#### Windows
1. Install Python from Microsoft Store
2. Install MSYS2 from https://www.msys2.org/
3. In MSYS2 shell: `pacman -S mingw-w64-x86_64-pango`
4. Set environment variable: `WEASYPRINT_DLL_DIRECTORIES=C:\msys64\mingw64\bin`

**Note:** PDF generation gracefully degrades when dependencies are unavailable - workflows will still generate markdown reports.

## Running the Demos

### Step 1: Start the Worker

In one terminal, start the worker that will handle all workflows:

```bash
uv run openai_agents/run_worker.py
```

Keep this running throughout your demo sessions. The worker registers all available workflows and activities.
You can run multiple copies of workers for faster workflow processing



### Run the Demo: Multi-Agent Interactive Research Workflow

An enhanced version of the research workflow with interactive clarifying questions to refine research parameters before execution and optional PDF generation.

This example is designed to be similar to the OpenAI Cookbook: [Introduction to deep research in the OpenAI API](https://cookbook.openai.com/examples/deep_research_api/introduction_to_deep_research_api)

**Files:**
- `openai_agents/workflows/interactive_research_workflow.py` - Interactive research workflow
- `openai_agents/workflows/research_agents/` - All research agent components
- `openai_agents/run_interactive_research_workflow.py` - Interactive research client
- `openai_agents/workflows/pdf_generation_activity.py` - PDF generation activity
- `openai_agents/workflows/research_agents/pdf_generator_agent.py` - PDF generation agent

**Agents:**
- **Triage Agent**: Analyzes research queries and determines if clarifications are needed
- **Clarifying Agent**: Generates follow-up questions for better research parameters
- **Instruction Agent**: Refines research parameters based on user responses
- **Planner Agent**: Creates web search plans
- **Search Agent**: Performs web searches
- **Writer Agent**: Compiles final research reports
- **PDF Generator Agent**: Converts markdown reports to professionally formatted PDFs

**To run:**
```streamlit run ui/streamlit_app.py
```
This will launch the Interactive Research App on http://localhost:8501

![UI Interface](ui/ui_img.png "UI Interface Img")


**Output:**
- `research_report.md` - Comprehensive markdown report
- `pdf_output/research_report.pdf` - Professionally formatted PDF (if PDF generation is available)

**Note:** The interactive workflow may take 2-3 minutes to complete due to web searches and report generation.

## Development

### Code Quality Tools

```bash
# Format code
uv run -m black .
uv run -m isort .

# Type checking
uv run -m mypy --check-untyped-defs --namespace-packages .
uv run pyright .
```

## Key Features

- **Temporal Workflows**: This demo uses Temporal for reliable workflow orchestration
- **OpenAI Agents**: Powered by the OpenAI Agents SDK for natural language processing
- **Multi-Agent Systems**: The research demo showcases complex multi-agent coordination
- **Interactive Workflows**: Research demo supports real-time user interaction
- **Tool Integration**: Tools demo shows how to integrate external activities
- **PDF Generation**: Interactive research workflow generates professional PDF reports alongside markdown

## License

MIT License - see the original project for full license details.
