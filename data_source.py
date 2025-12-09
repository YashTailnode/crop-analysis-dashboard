import kagglehub

# Download latest version
path = kagglehub.dataset_download("pyatakov/india-agriculture-crop-production")

print("Path to dataset files:", path)

# Path to dataset files: /home/yash/.cache/kagglehub/datasets/pyatakov/india-agriculture-crop-production/versions/4