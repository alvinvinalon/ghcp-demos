
# GitHub Copilot Demos

This repository contains demos where GitHub Copilot is used to build various applications using the latest preview models, technical and public features, as well as generally available features such as Copilot Edits. Copilot Edits allows GitHub Copilot to directly make changes to a file without the developer typing.

## Demo Contents

### Python
- [Autonomous Snake duelling game](python/auto-snake.py)
- [Gravity enabled ball in a Hexagon](python/ball-hexagon.py)

### JavaScript

All of these samples use the three.js 3D framework and are coded in a single HTML file. To preview, simply double-click the HTML file from the file explorer.

- [Big Bang Expansion](javascript/bigbang.html)
- [Spinning Galaxy](javascript/galaxy.html)
- [Moving Water Molecules](javascript/h2o.html)
- [3D Solar System](javascript/solar-system.html)


## Instructions

The files are pre-populated with the necessary code to run the demos. These demos were created using the prompts available in the [Build Prompts](./prompts/build-prompts.md) file.

To test out the prompt, you can delete the contents of a demo file, and use one of the prompts available. I suggest using the GitHub Copilot Edits feature get the code automatically generated in the editor.

### Assumptions

- You have access to GitHub Copilot and the latest preview models (o3-mini, Claude 3.5 Sonnet)
- You already know how to clone a repository
- You know who to run a Python, JavaScript, or HTML file

## Getting Started

To get started with the demos, clone this repository and follow the instructions in each demo's directory.

```bash
git clone https://github.com/yourusername/ghcp-demos.git
cd ghcp-demos
```

## Contributing

We welcome contributions to enhance these demos. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
