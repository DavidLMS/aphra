# Short Article Workflow

The Short Article workflow implements a comprehensive 5-step translation process designed for articles, blog posts, and general text content.

## Overview

This workflow provides high-quality translation through a multi-stage process that ensures accuracy, context awareness, and natural language flow.

### When to Use

This workflow is suitable for:
- Articles and blog posts
- General text content
- Documents requiring high translation quality
- Content where context and nuance are important

### Workflow Steps

1. **Analysis** - Identify key terms and concepts in the source text
2. **Search** - Generate contextual explanations using web search
3. **Translation** - Create initial translation based on analysis and context
4. **Critique** - Evaluate translation quality and identify improvements
5. **Refinement** - Produce final improved translation incorporating feedback

## Workflow Diagram

![Short Article Workflow Diagram](workflow-diagram.png)

For the interactive Mermaid version, see [workflow-diagram.md](workflow-diagram.md).

## Configuration

### Default Models
- **Writer**: `anthropic/claude-sonnet-4` (for analysis, translation, and refinement)
- **Searcher**: `perplexity/sonar` (for web search and context gathering)
- **Critiquer**: `anthropic/claude-sonnet-4` (for translation evaluation)

### Customization

You can override the default configuration in your `config.toml`:

```toml
[short_article]
writer = "different/model"
searcher = "different/search-model"
critiquer = "different/critique-model"
```

## Usage Examples

### Basic Usage

```python
from aphra import translate

translation = translate(
    source_language="Spanish",
    target_language="English", 
    text="Your text here",
    config_file="config.toml"
)
```

### Direct Workflow Usage

```python
from aphra.workflows.short_article import ShortArticleWorkflow
from aphra.core.context import TranslationContext
from aphra.core.llm_client import LLMModelClient

workflow = ShortArticleWorkflow()
model_client = LLMModelClient('config.toml')

context = TranslationContext(
    model_client=model_client,
    source_language="Spanish",
    target_language="English",
    log_calls=False
)

result = workflow.run(context, "Your text here")
```

For more examples, see the [examples directory](../examples/).

## Testing

The workflow includes comprehensive tests that make real API calls to validate functionality:

```bash
python -m pytest aphra/workflows/short_article/tests/ -v
```

## Implementation Details

- **Auto-Discovery**: Automatically detected by the system
- **Self-Contained**: All workflow code, prompts, and configuration in one directory
- **Extensible**: Inherit from this workflow to create specialized versions
- **Configurable**: User can override any model or parameter

## Performance

- **Average Time**: 20-30 seconds for typical articles (varies by content length and API response times)
- **API Calls**: 5-7 calls per translation (depending on search results)
- **Quality**: High-quality translations with context awareness and critique-driven refinement