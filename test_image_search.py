import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

from config import *

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.


analyze_url = VISION_BASE_URL + "analyze"

image_path = '/Users/kenziyuliu/Desktop/NewYork.png'
image_data = open(image_path, 'rb').read()

headers = {'Ocp-Apim-Subscription-Key': IMG_SEARCH_AZURE_KEY, "Content-Type": "application/octet-stream" }
params  = {'visualFeatures': 'Categories,Description,Color'}
# data    = {'url': image_url}
response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
print(analysis)
image_caption = analysis["description"]["captions"][0]["text"].capitalize()

# Display the image and overlay it with the caption.
# image = Image.open(BytesIO(requests.get(image_url).content))
image = Image.open(BytesIO(image_data))
plt.imshow(image)
plt.axis("off")
_ = plt.title(image_caption, size="x-large", y=-0.1)