# Microsoft for Startups Technical Content

## Contributing

### Setup

The easiest way to start contributing is to use GitHub Codespaces:

1. Select Code and open in Codespace from GitHub
1. After the codespaces has initialized, press `F5` to start the server and launch the site in Edge. The site will live update as you make changes

### Creating pages

To create a page, open the terminal in VS Code (`` Ctrl + Shift + ` ``) run this command:

```bash
hugo new first-deploy/get-ready/config
```

This will create a page called "Config" nested under **First Deploy > Get Ready**.

### Menu Ordering

To change the order of pages in the menu, you can use the `weight` parameter in the Markdown frontmatter:

```text
---
title: "Get your app ready"
date: 2021-12-23T23:10:50Z
weight: 1
---
```

### Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
