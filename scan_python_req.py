import os
import re
from packaging import version

def scan_python_packages(directory):
    repo_package_map = {}
    
    for root, dirs, files in os.walk(directory):
        if ".git" in dirs or "requirements.txt" in files:
            repo_name = os.path.basename(root)
            repo_package_map[repo_name] = {}
            for file in files:
                if file == 'requirements.txt':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            # Ignore lines containing '@' or starting with '--'
                            if not '@' in line and not line.startswith('--'):
                                # Replace '==' with '-' and remove line continuation '\'
                                split_line = re.sub('==', '-', line.replace("\\", "")).rsplit("-", 1)
                                if len(split_line) == 2:
                                    package_name, package_version = split_line
                                    package_name = package_name.replace('_', '-')
                                    if package_name not in repo_package_map[repo_name] or version.parse(package_version) > version.parse(repo_package_map[repo_name][package_name]):
                                        repo_package_map[repo_name][package_name] = package_version

    # print the packages per repository
    for repo in sorted(repo_package_map.keys()):
        for package in sorted(repo_package_map[repo].keys()):
            print(f"{repo}, {package}-{repo_package_map[repo][package]}")

scan_python_packages('/home/emesika/toolchain/dws/')

