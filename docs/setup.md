# Setup
## Prerequisites
1. VSCode
2. Docker (and Docker Desktop)
3. The [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VSCode
4. This repository

## Steps
1. Start docker desktop (which starts "the docker daemon")
2. Open this repo in VSCode
4. Open the command pallette (Ctrl/CMD + Shift + P)
5. Search for the action "Dev Containers: Open Folder in Container"
![Screen Shot 2023-01-25 at 9 49 47 PM](https://user-images.githubusercontent.com/8062248/214756285-963b27c5-f19c-4877-8432-db8b5cfc9449.png)
6. Select the 'backend' folder (or frontend, if you wish to do frontend development) and click open
![Screen Shot 2023-01-25 at 9 49 56 PM](https://user-images.githubusercontent.com/8062248/214756375-5f4bbe93-912d-4c70-bc68-1ce7e8f1e6dd.png)
7. Wait.
8. Navigate to `localhost:3000` for the frontend and `localhost:8000` for the backend.
9. (Optional) Once the first dev container is set up you can open a new VSCode window, and repeat steps 4-6 for the other (front/back-end) container as well. This way, you'll have one window for frontend and one for backend open simultaneously. 
