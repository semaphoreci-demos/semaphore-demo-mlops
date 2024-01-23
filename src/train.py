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
data_path = join('data', 'images')
metrics_path = 'metrics'
models_path = 'models'

# Instantiate dataloader
dls = ImageDataLoaders.from_name_func(
        os.getcwd(), 
        get_image_files(data_path), 
        valid_pct=params['train']['valid_pct'],           
        seed=params['train']['seed'],                     
        label_func=is_cat,                          
        item_tfms=Resize(params['train']['resize_img'])  
)
print(f"Image count for dataset")
print(f"- Training: {len(dls.train_ds)}")
print(f"- Validation: {len(dls.valid_ds)}")

# Fine-tune model
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(0)

# Export model files
learn.export(join(models_path, 'model.pkl'))
learn.model.eval()
torch.save(learn.model.state_dict(), join(models_path, 'model.pth'))

# Plot fine-tuning results
learn.show_results(max_n=9, figsize=(7,8))
plt.savefig(join(metrics_path, 'finetune_results.png'))
plt.close()


# In this section we calculate a few benchmarks for the model

## Classification Report
from sklearn.metrics import classification_report
with open(join(metrics_path, 'classification.md'), 'w') as f:
    preds, targets = learn.get_preds()
    predictions = np.argmax(preds, axis=1)
    f.write("# Classification Report\n\n```\n")
    f.write(classification_report(targets, predictions, target_names=['Dog', 'Cat']))
    f.write("```")

## Confusion matrix
interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix(figsize=(8, 8))
plt.savefig(join(metrics_path, 'confusion_matrix.png'))
plt.close()

## Top losses
interp.plot_top_losses(8, nrows=2)
plt.savefig(join(metrics_path, 'top_losses.png'))
plt.close()

