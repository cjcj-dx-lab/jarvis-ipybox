# Installation

```bash
pip install jarvis_ipybox
```

## Docker image

Before using `jarvis-ipybox`, you need to build a Docker image. This image contains all required dependencies for executing Python code in stateful and isolated sessions.

### Default build

To build an `jarvis-ipybox` Docker image with default settings:

```bash
python -m jarvis_ipybox build
```

This creates a Docker image tagged as `jarvis-ipybox` containing the base Python dependencies required for the code execution environment.

!!! note

    By default, containers created from this image will run with the same user and group IDs as the user who built the image, ensuring proper file permissions on mounted host directories. If you use the `-r` or `--root` option when building the image, the container will run as root.

### Custom build

To create a custom `jarvis-ipybox` Docker image with additional dependencies, create a dependencies file (e.g., `dependencies.txt`). For example:

```toml title="dependencies.txt"
pandas = "^2.2"
scikit-learn = "^1.5"
matplotlib = "^3.9"
```

Then build the image with a custom tag and dependencies:

```bash
python -m jarvis_ipybox build -t my-box:v1 -d path/to/dependencies.txt
```

The dependencies file should use the [Poetry dependency specification format](https://python-poetry.org/docs/dependency-specification/). These packages will be installed alongside the base dependencies required for the execution environment. You can also [install additional dependencies at runtime](usage.md#installing-dependencies-at-runtime).
