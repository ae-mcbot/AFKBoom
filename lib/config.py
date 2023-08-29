def config():
    import yaml
    file_path = "config/config.yaml"
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
