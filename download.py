from tcia_utils import nbia
from monai.bundle import download

datadir = '.\data'

cart_name = "nbia-56561691129779503"
cart_data = nbia.getSharedCart(cart_name)
df = nbia.downloadSeries(cart_data, format="df", path = datadir)

model_name = "wholeBody_ct_segmentation"
download(name=model_name, bundle_dir=datadir, source='github')