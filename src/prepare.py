import tarfile
import os

dataset = os.path.join('data','images.tar.gz')
destination = 'data'

print(f'Decompressing {dataset}...')
with tarfile.open(dataset, 'r:*') as tar:
    tar.extractall(path=destination)