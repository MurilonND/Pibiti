import os
import monai
import tempfile
from monai.apps import download_and_extract
from monai.bundle import ConfigParser
from monai.data import decollate_batch
from monai.handlers import MLFlowHandler
from monai.config import print_config
from monai.visualize.utils import blend_images

from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from skimage.measure import marching_cubes
import numpy as np

import torch

directory = os.environ.get("MONAI_DATA_DIRECTORY")
root_dir = tempfile.mkdtemp() if directory is None else directory

resource = "https://msd-for-monai.s3-us-west-2.amazonaws.com/Task09_Spleen.tar"
md5 = "410d4a301da4e5b2f6f86ec3ddba524e"

compressed_file = os.path.join(root_dir, "Task09_Spleen.tar")
data_dir = os.path.join(root_dir, "Task09_Spleen")
print(data_dir)
if not os.path.exists(data_dir):
    download_and_extract(resource, compressed_file, root_dir, md5)

os.system("find {data_dir}/imagesTs/spleen_* -type f | sort -zR | head -10 | tr '\n' '\0' | xargs -0 rm")

monai.bundle.download(name="wholeBody_ct_segmentation", bundle_dir="./zoo_dir")

os.system('python -m monai.bundle run evaluating \
    --meta_file "./zoo_dir/wholeBody_ct_segmentation/configs/metadata.json" \
    --config_file "./zoo_dir/wholeBody_ct_segmentation/configs/inference.json" \
    --logging_file "./zoo_dir/wholeBody_ct_segmentation/configs/logging.conf" \
    --dataset_dir "{data_dir}" \
    --bundle_root "./zoo_dir/wholeBody_ct_segmentation"')

output_dir = os.path.abspath("./monai_results")

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model_config_file = os.path.join("./zoo_dir", "wholeBody_ct_segmentation", "configs", "inference.json")
model_config = ConfigParser()
model_config.read_config(model_config_file)

model_config["bundle_root"] = "./zoo_dir"
model_config["output_dir"] = output_dir
model_config["dataset_dir"] = data_dir

checkpoint = os.path.join("./zoo_dir", "wholeBody_ct_segmentation", "models", "model_lowres.pt")

preprocessing = model_config.get_parsed_content("preprocessing")
model = model_config.get_parsed_content("network").to(device)
inferer = model_config.get_parsed_content("inferer")
postprocessing = model_config.get_parsed_content("postprocessing")
dataloader = model_config.get_parsed_content("dataloader")

model.load_state_dict(torch.load(checkpoint, map_location=device))
model.eval()

torch.cuda.memory_summary(device=None, abbreviated=False)

torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = False
torch.cuda.set_device(device)
torch.cuda.empty_cache()

model.groupnorm1 = torch.nn.GroupNorm(num_groups=8, num_channels=64)
torch.cuda.set_per_process_memory_fraction(0.5, 0)

d = next(iter(dataloader))
images = d["image"].to(device)
images.size()

img = images[:, :, 20:100, 20:100, 20:100]
img.size()

d["pred"] = inferer(img, network=model)

orig_img = d['image'][0]
reduced_img = orig_img[:, 20:100, 20:100, 20:100]

pred_img = d['pred'].argmax(1).cpu()

map_image = reduced_img + pred_img

slices = map_image.shape[-1]

for i in range(0, int(slices / 10)):
    slice_index = 10 * i

    plt.figure("blend image and label", (12, 4))

    plt.subplot(1, 3, 1)
    plt.title(f"image slice {slice_index}")
    plt.imshow(reduced_img[0, :, :, slice_index], cmap="gray")

    plt.subplot(1, 3, 2)
    plt.title(f"label slice {slice_index}")
    plt.imshow(pred_img[0, :, :, slice_index])

    map_image = (reduced_img + d['pred'].argmax(1).cpu())

    plt.subplot(1, 3, 3)
    plt.title(f"blend slice {slice_index}")
    plt.imshow(map_image[0, :, :, slice_index], cmap="gray")

    plt.show()