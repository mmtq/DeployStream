# **DeployStream**

DeployStream is a GitHub Workflow designed to streamline the process of deploying files from a GitHub repository to a VPS using SSH and `rsync`. This workflow simplifies continuous deployment for projects by automating file synchronization with secure credentials.

---

## **Features**
- Automatically deploy files to your VPS when changes are pushed to the `main` branch.
- Utilizes `rsync` for efficient file synchronization.
- Securely manages SSH credentials using GitHub Secrets.
- Customizable file paths for local and remote directories.

---

## **Usage**

### **Example Workflow**
Add the following example workflow to your `.github/workflows/deploy.yml` file:

```yaml
name: Deploy on Push

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Sync Files to VPS
        uses: Sayemahamed/DeployStream/.github/actions/fileSync@main 
        with:
          SSH_USERNAME: ${{ secrets.SSH_USERNAME }}
          SSH_IPADDRESS: ${{ secrets.SSH_IPADDRESS }}
          SSH_PASSWORD: ${{ secrets.SSH_PASSWORD }}
          LOCAL_PATH: ${{ secrets.LOCAL_PATH }}
          REMOTE_PATH: ${{ secrets.REMOTE_PATH }}
```

---

## **Inputs**
The action requires the following inputs:

| Input          | Description                           | Required |
|----------------|---------------------------------------|----------|
| `SSH_USERNAME` | SSH username for the VPS.            | Yes      |
| `SSH_IPADDRESS`| IP address of the VPS.               | Yes      |
| `SSH_PASSWORD` | Password for SSH authentication.     | Yes      |
| `LOCAL_PATH`   | Path to the files in the repository to sync (e.g., `./`). | Yes      |
| `REMOTE_PATH`  | Path on the VPS where files will be deployed. | Yes      |

---

## **Setting Up GitHub Secrets**
To securely provide the required inputs, add the following secrets to your repository:

1. **`SSH_USERNAME`**: Your SSH username.
2. **`SSH_IPADDRESS`**: The IP address of your VPS.
3. **`SSH_PASSWORD`**: Your SSH password.
4. **`LOCAL_PATH`**: The path in your repository to sync (e.g., `./`).
5. **`REMOTE_PATH`**: The destination path on the VPS.

To add these secrets:
1. Go to your GitHub repository.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret** and add each of the above secrets.

---

## **How It Works**
1. **Trigger**: The workflow is triggered on every push to the `main` branch.
2. **File Checkout**: The repository is checked out using `actions/checkout`.
3. **File Sync**: The files specified in `LOCAL_PATH` are synced to the remote VPS at `REMOTE_PATH` using `rsync` via SSH.

---

## **Demo**

Want to see DeployStream in action? Check out our showcase repository: [DeployStream-Demo](https://github.com/mmtq/DeployStream-Demo)  

This repository demonstrates how to integrate and use DeployStream in a real-world scenario. It includes a sample project and step-by-step examples to help you get started quickly.  


---


## **Contributing**
Contributions are welcome! Feel free to open an issue or submit a pull request to improve DeployStream.

---

## **License**
DeployStream is licensed under the [MIT License](LICENSE).

