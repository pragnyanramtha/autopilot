# Complex Workflow Enhancement

## Overview

The AI Brain has been significantly enhanced to handle complex, multi-step commands that require:
- Web research
- Content generation
- Authentication to external services
- Multi-page navigation
- Sequential task execution

## What's New

### 1. Enhanced Command Parsing

The Gemini client now distinguishes between:
- **Simple commands**: Single actions (click, type, open app)
- **Complex commands**: Multi-step workflows (research + write + post)

#### Example Complex Command
```
"Write an article about AI and post to X"
```

This is automatically broken down into:
1. Research AI topics
2. Generate article content
3. Open browser
4. Navigate to X (Twitter)
5. Login to X
6. Post the article

### 2. Improved Workflow Generation

The `WorkflowGenerator` now supports:

#### New Action Types
- `search_web` - Perform web searches
- `navigate_to_url` - Navigate to specific URLs
- `login` - Handle authentication flows
- `fill_form` - Fill out web forms
- `generate_content` - Generate text content using Gemini
- `post_to_social` - Post to social media platforms
- `multi_step` - Complex workflows with sub-tasks

#### Complex Workflow Structure
```python
{
    "complexity": "complex",
    "action": "multi_step",
    "target": "overall goal description",
    "parameters": {
        "sub_tasks": [
            {
                "action": "search_web",
                "target": "AI trends",
                "parameters": {"query": "latest AI trends 2025"},
                "description": "Research AI topics"
            },
            {
                "action": "generate_content",
                "target": "article",
                "parameters": {"topic": "AI", "length": "medium"},
                "description": "Write article about AI"
            },
            # ... more sub-tasks
        ],
        "requires_research": true,
        "requires_authentication": true,
        "requires_content_generation": true
    }
}
```

### 3. Content Generation Integration

The AI Brain can now generate content using Gemini:

```python
# Generate articles, posts, emails, etc.
content = gemini_client.generate_content(
    topic="AI trends",
    content_type="article",
    parameters={
        "length": "medium",  # short, medium, long
        "style": "informative",
        "tone": "professional"
    }
)
```

### 4. Research Capabilities

The AI Brain can research topics before generating content:

```python
# Research a topic
research = gemini_client.research_topic("latest AI trends")
# Returns: {
#     "summary": "...",
#     "key_points": [...],
#     "trends": [...],
#     "examples": [...]
# }
```

### 5. Enhanced User Experience

#### Complex Workflow Detection
When a complex command is detected, the system:
1. Shows a breakdown of all sub-tasks
2. Identifies special requirements (research, auth, content generation)
3. Performs content generation/research before workflow execution
4. Shows preview of generated content
5. Warns about manual steps (like authentication)

#### Example Output
```
Complex Multi-Step Workflow Detected

Breakdown of 6 sub-tasks:
  1. Research AI topics
  2. Write article about AI
  3. Open browser
  4. Go to X
  5. Login to X
  6. Post the article

Special Requirements:
  • Web research needed
  • Authentication required (may need manual login)
  • Content generation required

→ Generating content with Gemini...
✓ Content generated (487 characters)

Preview: Artificial Intelligence continues to transform...

→ Researching topic with Gemini...
✓ Research complete
  Key points: 5 found
```

## Supported Complex Commands

### Content Creation & Publishing
- "Write an article about [topic] and post to X"
- "Research [topic] and create a summary"
- "Generate a blog post about [topic] and save it"

### Web Automation
- "Go to [website], login, and fill the form"
- "Search for [query], open first result, and extract text"
- "Navigate to [URL], click [element], and download file"

### Multi-Platform Workflows
- "Open Gmail, compose email to [recipient], and send"
- "Post the same message to X, Facebook, and LinkedIn"
- "Search [topic], summarize results, and email to team"

## Architecture Changes

### GeminiClient (`ai_brain/gemini_client.py`)
- Enhanced `_build_command_prompt()` with complex command understanding
- Added `generate_content()` for content generation
- Added `research_topic()` for research capabilities

### WorkflowGenerator (`ai_brain/workflow_generator.py`)
- Added `_generate_complex_workflow()` for multi-step workflows
- Added `_generate_steps_for_action()` helper for sub-task processing
- New action generators:
  - `_generate_navigate_steps()`
  - `_generate_login_steps()`
  - `_generate_fill_form_steps()`
  - `_generate_content_generation_steps()`
  - `_generate_social_post_steps()`

### AIBrainApp (`ai_brain/main.py`)
- Split `_process_command()` into simple and complex handlers
- Added `_handle_complex_workflow()` for complex command processing
- Added `_extract_content_topic()` and `_extract_research_query()` helpers
- Enhanced UI with better feedback for complex workflows

## Configuration

No additional configuration required! The enhancements work with existing setup.

### Optional: Adjust Gemini Parameters
In `config.json`:
```json
{
  "gemini": {
    "api_key": "YOUR_KEY",
    "model": "gemini-2.5-flash",
    "temperature": 0.7
  }
}
```

## Usage Examples

### Example 1: Simple Command (unchanged)
```
> Click the submit button

→ Analyzing command with Gemini...
Parsed Intent: action=click, target=submit button
→ Generating workflow...
→ Sending workflow to automation engine...
✓ Workflow sent
```

### Example 2: Complex Command (new)
```
> Write an article about Python best practices and post to X

→ Analyzing command with Gemini...

Complex Multi-Step Workflow Detected

Breakdown of 6 sub-tasks:
  1. Research Python topics
  2. Write article about Python
  3. Open browser
  4. Go to X
  5. Login to X
  6. Post the article

Special Requirements:
  • Web research needed
  • Authentication required (may need manual login)
  • Content generation required

→ Generating content with Gemini...
✓ Content generated (523 characters)

Preview: Python best practices have evolved significantly...

→ Researching topic with Gemini...
✓ Research complete
  Key points: 4 found

→ Generating complex workflow...
✓ Workflow created with 15 steps

Note: This workflow requires authentication.
You may need to manually log in when prompted.

Execute this complex workflow? [y/n]: y
```

## Limitations & Future Improvements

### Current Limitations
1. **Authentication**: Login steps are placeholders - requires manual intervention
2. **Content Storage**: Generated content is stored in workflow metadata but not persisted
3. **Error Recovery**: Complex workflows don't have automatic retry logic
4. **Platform-Specific**: Social media posting requires platform-specific implementations

### Future Improvements
1. **Credential Management**: Secure storage and retrieval of login credentials
2. **Content Persistence**: Save generated content to files or database
3. **Smart Retry**: Automatic retry with exponential backoff for failed steps
4. **Platform Adapters**: Dedicated adapters for X, Facebook, LinkedIn, etc.
5. **Visual Feedback**: Real-time progress updates during execution
6. **Workflow Templates**: Pre-built templates for common complex tasks
7. **Learning**: Learn from successful workflows to improve future generations

## Testing

Test the enhancements with these commands:

### Simple Commands (should work as before)
```
Click the OK button
Type hello world
Open Chrome
Search for Python tutorials
```

### Complex Commands (new functionality)
```
Write an article about AI and post to X
Research Python best practices and create a summary
Generate a blog post about machine learning
Search for latest tech news and summarize
```

## Troubleshooting

### Low Confidence Warnings
If you see low confidence warnings, try:
- Being more specific in your command
- Breaking down very complex tasks into smaller commands
- Checking that your Gemini API key is valid

### Workflow Validation Errors
If workflows fail validation:
- Check that coordinates are within screen bounds
- Ensure all required parameters are provided
- Review the workflow steps for logical errors

### Authentication Issues
For commands requiring login:
- Be prepared to manually authenticate when prompted
- Consider using browser profiles with saved credentials
- Future versions will support credential management

## Performance

### Simple Commands
- Parsing: ~1-2 seconds
- Workflow generation: <1 second
- Total: ~2-3 seconds

### Complex Commands
- Parsing: ~2-3 seconds
- Content generation: ~3-5 seconds
- Research: ~2-4 seconds
- Workflow generation: ~1-2 seconds
- Total: ~8-14 seconds

## Security Considerations

1. **API Keys**: Store Gemini API key in environment variables
2. **Generated Content**: Review generated content before posting
3. **Authentication**: Never store passwords in plain text
4. **Workflow Review**: Always review workflows before execution
5. **Rate Limiting**: Be mindful of API rate limits

## Conclusion

The enhanced AI Brain now provides robust support for complex, multi-step automation tasks. It intelligently breaks down complex commands, generates content, performs research, and coordinates multi-platform workflows - all while maintaining the simplicity of natural language commands.
