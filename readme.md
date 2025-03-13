# Yocto Poky Build Automation Script

This project provides a Python script to automate the setup and build process of Yocto Project (Poky) images inside a Docker container. The script simplifies cloning the Poky repository, configuring the environment, and building a target image for a specified machine.

## Features

- Checks for required dependencies.
- Clones the Poky repository with a specified branch (e.g., `kirkstone`).
- Configures build settings in `local.conf`.
- Limits the number of CPU cores used for the build (default is 2).
- Automatically builds the target image using `bitbake`.
- Cleans up temporary files after the build.
- Optional cleanup of the working directory.

## Requirements

- **Docker**: Ensure Docker and Docker Compose are installed on your system.
  - On Ubuntu: `sudo apt-get install docker.io docker-compose`

## Project Structure

- `build_poky.py`: The main Python script.
- `Dockerfile`: Docker image build configuration.
- `docker-compose.yml`: Docker Compose configuration.
- `restart.sh`: Bash script to restart the container.
- `README.md`: This file.

## Installation and Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/yocto-poky-build.git
   cd yocto-poky-build
   ```

2. **Run the build with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Restart the build (if needed)**:
   ```bash
   ./restart.sh
   ```

## Configuration

- **Poky Branch**: Modify `POKY_VERSION` in `build_poky.py` (e.g., `kirkstone` or `master`).
- **Target Machine**: Change `MACHINE` in `build_poky.py` (e.g., `qemux86-64`).
- **Image**: Adjust `IMAGE` in `build_poky.py` (e.g., `core-image-minimal`).
- **Number of Cores**: Update `THREADS` in `build_poky.py` to control build load (default is 2).

## Output

Built images will be saved in the `poky-build/build/tmp/deploy/images/<MACHINE>` directory inside the container, which is mounted to the local `./poky-build` directory.

## Notes

- Ensure sufficient disk space is available (at least 50 GB recommended).
- Build time may vary depending on your system resources and configuration.
