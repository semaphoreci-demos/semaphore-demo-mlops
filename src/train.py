# fine-tune a pretrained CNN model using the Oxfort-IIIT Pets dataset 
# These are images of cats and dogs of different breeds.
# Cats filenames begin with an Uppercase
# Dogs filenames begin with a lowercase
# that's your labeling right there

from os.path import join
from fastai.vision.all import *
from utils import is_cat
import yaml

with open("params.yaml", "r") as stream:
    params = yaml.safe_load(stream)

# Paths
data_path = join('data', 'images')  # training/validation images
metrics_path = 'metrics'            # where to store model metrics and plots
models_path = 'models'              # where to save trained models

# Instantiate dataloader
dls = ImageDataLoaders.from_name_func(
        os.getcwd(), 
        get_image_files(data_path), 
        valid_pct=params['train']['valid_pct'],           # ratio reserved for validation test (eg. 0.2)
        seed=params['train']['seed'],                     # random split of training/validation sets
        label_func=is_cat,                          # the labeling function (True=Cat, False=Dog)
        item_tfms=Resize(params['train']['resize_img'])  # resize training images to square NxN pixels
)
print(f"Number of training images: {len(dls.train_ds)}")
print(f"Number of validation images: {len(dls.valid_ds)}")


# Fine-tune model
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(0)


# Plot fine-tuning results
learn.show_results(max_n=9, figsize=(7,8))
plt.savefig(join(metrics_path, 'finetune_results.png'))
plt.close()


# Plot confusion matrix
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix(figsize=(8, 8))
plt.savefig(join(metrics_path, 'confusion_matrix.png'))
plt.close()


# Plot top losses
interp.plot_top_losses(8, nrows=2)
plt.savefig(join(metrics_path, 'top_losses.png'))
plt.close()


# Export model to pkl and pth files
learn.export(join(models_path, 'model.pkl'))
learn.model.eval()
torch.save(learn.model.state_dict(), join(models_path, 'model.pth'))