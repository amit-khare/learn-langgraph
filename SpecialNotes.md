# Special Commands & Notes

## Pandoc - Document Conversion

### What is Pandoc?
Pandoc is a universal document converter that can convert files between different markup formats.

### Converting Word (.docx) to Markdown (.md)

**Basic Command:**
```bash
pandoc "input.docx" -o "output.md"
```

**Example Used:**
```bash
pandoc "/Users/amit/workspace/learning/learn-langgraph/Langgraph Notes.docx" -o "/Users/amit/workspace/learning/learn-langgraph/LangGraphNotes.md"
```

### Common Options:

- `-o` or `--output`: Specify the output file
- `-f` or `--from`: Specify input format (usually auto-detected)
- `-t` or `--to`: Specify output format (usually inferred from extension)
- `--standalone`: Produce a standalone document with headers/footers

**Convert with specific formats:**
```bash
pandoc -f docx -t markdown input.docx -o output.md
```

**Convert to other formats:**
```bash
# Word to HTML
pandoc input.docx -o output.html

# Markdown to PDF (requires LaTeX)
pandoc input.md -o output.pdf

# Markdown to Word
pandoc input.md -o output.docx
```

### Installation:
- macOS: `brew install pandoc`
- Linux: `sudo apt-get install pandoc`
- Windows: Download from [pandoc.org](https://pandoc.org/installing.html)

### Check if Pandoc is installed:
```bash
which pandoc
# or
pandoc --version
```
