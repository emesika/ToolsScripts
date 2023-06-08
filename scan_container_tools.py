import os
import re
import yaml

def no_op(loader, tag_suffix, node):
    return node.value

yaml.SafeLoader.add_multi_constructor('', no_op)

def parse_containerfile(file_path):
    print(f"Parsing Containerfile: {file_path}")
    with open(file_path, 'r') as file:
        lines = file.readlines()

    image_id = next((line for line in lines if line.startswith('FROM ')), None)
    if image_id is None:
        print(f"No image ID found in Containerfile: {file_path}")
        return None, None
    image_id = image_id.strip().replace('FROM ', '')

    tools = extract_tools(lines[1:])
    print(f"Image ID: {image_id}, Tools: {tools}")
    return image_id, ','.join(tools)

def parse_pipeline_tools(file_path):
    print(f"Parsing pipeline: {file_path}")
    image_tool_map = {}
    with open(file_path, 'r') as file:
        pipelines = yaml.safe_load_all(file)
        for pipeline in pipelines:
            if pipeline and isinstance(pipeline, dict):
                for key in pipeline:
                    if isinstance(pipeline[key], dict) and 'image' in pipeline[key] and isinstance(pipeline[key]['image'], str):
                        image_id = pipeline[key]['image']
                        if 'script' in pipeline[key]:
                            script = pipeline[key]['script']
                            if isinstance(script, list):
                                script = ' '.join(script)
                            tools = extract_tools(script.splitlines())
                            image_tool_map[image_id] = ','.join(tools)
    print(f"image-tool map: {image_tool_map}")
    return image_tool_map

def extract_tools(lines):
    tools_pattern = re.compile(r'(?:RUN dnf install -y|pip install) (.*)')
    tools = []
    concatenated_lines = []
    current_line = ""
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.endswith("\\"):
            current_line += stripped_line[:-1]
        else:
            current_line += stripped_line
            concatenated_lines.append(current_line)
            current_line = ""
    for line in concatenated_lines:
        match = tools_pattern.search(line)
        if match:
            parts = match.group(1).split('&&')
            tools_list = parts[0].split()
            tools.extend([tool for tool in tools_list if not tool.startswith('-')])
    return tools
def scan_directory(directory):
    repo_map = {}
    for root, dirs, files in os.walk(directory):
        if ".git" in dirs or ".gitlab-ci.yml" in files or "Containerfile" in files:
            repo_name = os.path.basename(root)
            repo_map[repo_name] = {}
            for file in files:
                file_path = os.path.join(root, file)
                if file == 'Containerfile':
                    image_id, tools = parse_containerfile(file_path)
                    if image_id is not None:
                        repo_map[repo_name][image_id] = tools
                elif file == '.gitlab-ci.yml':
                    image_tool_map = parse_pipeline_tools(file_path)
                    repo_map[repo_name].update(image_tool_map)
    print("\nRepo map:")
    for repo, images in repo_map.items():
        if images:  # Print only repositories with detected images
            print(f"Repo: {repo}")
            for image, tools in images.items():
                print(f"  Image: {image}, Tools: {tools}")
    return repo_map

scan_directory('/home/emesika/toolchain/dws/')

