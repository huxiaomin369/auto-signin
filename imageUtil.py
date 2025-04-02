from PIL import Image
import base64
import io
def url_to_image(data_uri):
    # # 分割 Data URI 以获取 Base64 编码的部分
    _, encoded_image = data_uri.split(',', 1)
    # 解码 Base64 字符串为二进制数据
    decoded_image = base64.b64decode(encoded_image)
    # 使用 PIL 库将二进制数据转换为图像对象
    image = Image.open(io.BytesIO(decoded_image))
    return image
  
def url_to_imageBytes(data_uri):
    # # 分割 Data URI 以获取 Base64 编码的部分
    _, encoded_image = data_uri.split(',', 1)
    # 解码 Base64 字符串为二进制数据
    decoded_image = base64.b64decode(encoded_image)
    return decoded_image
  
def get_image_width(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return image.width
