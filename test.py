import kagglehub

# Download latest version
path = kagglehub.model_download("umeradnaan/yolo-v8/other/default")

print("Path to model files:", path)