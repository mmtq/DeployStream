#!/usr/bin/env python3
"""
DeployStream - Simple GitHub Project Deployment Tool
Deploys GitHub projects to Nginx server with minimal configuration.
"""

import subprocess
import os
import sys

def run_command(command):
    """Execute a shell command and return the result"""
    try:
        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"Success: {process.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if git and nginx are installed"""
    for tool in ["git --version", "nginx -v"]:
        if not run_command(tool):
            print(f"Please install {tool.split()[0]} first.")
            return False
    return True

def deploy_project(repo_url):
    """Deploy GitHub project to Nginx"""
    if os.geteuid() != 0:
        print("Error: This script must be run with sudo privileges")
        print("Usage: sudo python3 DeployStream.py <repository-url>")
        return False

    print("\n=== Starting DeployStream deployment ===")
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Set up paths
    target_dir = "/var/www/html/deploystream"
    
    # Clone repository
    print("\n1. Cloning repository...")
    if os.path.exists(target_dir):
        run_command(f"rm -rf {target_dir}")
    if not run_command(f"git clone {repo_url} {target_dir}"):
        return False
    
    # Configure Nginx
    print("\n2. Configuring Nginx...")
    nginx_config = f"""
server {{
    listen 80;
    server_name localhost;
    root {target_dir};
    index index.html index.htm;
    location / {{
        try_files $uri $uri/ =404;
    }}
}}
"""
    
    try:
        # Write nginx config
        with open('/etc/nginx/sites-available/deploystream', 'w') as f:
            f.write(nginx_config)
        
        # Create symbolic link
        if os.path.exists('/etc/nginx/sites-enabled/deploystream'):
            os.remove('/etc/nginx/sites-enabled/deploystream')
        os.symlink('/etc/nginx/sites-available/deploystream', 
                   '/etc/nginx/sites-enabled/deploystream')
        
        # Reload nginx
        if run_command("nginx -t"):
            run_command("systemctl reload nginx")
            print("\n=== Deployment Successful! ===")
            print("Your project is now accessible at: http://localhost")
            return True
            
    except Exception as e:
        print(f"Error configuring Nginx: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sudo python3 DeployStream.py <repository-url>")
        sys.exit(1)
        
    if deploy_project(sys.argv[1]):
        sys.exit(0)
    sys.exit(1)
