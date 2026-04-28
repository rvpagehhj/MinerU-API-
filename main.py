import requests

file_path = ["你的本地文件路径"]
token = "官网获得的API Token"
url = "https://mineru.net/api/v4/file-urls/batch"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "files": [
        {"name":"demo.pdf", "data_id": "abcd"}
    ],
    "model_version":"vlm"
}

try:
    response = requests.post(url,headers=header,json=data)
    if response.status_code == 200:
        result = response.json()
        print('response success. result:{}'.format(result))
        if result["code"] == 0:
            batch_id = result["data"]["batch_id"]
            urls = result["data"]["file_urls"]
            print('batch_id:{},urls:{}'.format(batch_id, urls))
            for i in range(0, len(urls)):
                with open(file_path[i], 'rb') as f:
                    res_upload = requests.put(urls[i], data=f)
                    if res_upload.status_code == 200:
                        print(f"{urls[i]} upload success")
                    else:
                        print(f"{urls[i]} upload failed")
        else:
            print('apply upload url failed,reason:{}'.format(result["msg"]))
    else:
        print('response not success. status:{} ,result:{}'.format(response.status_code, response))
except Exception as err:
    print(err)

from time import sleep
sleep(3)

url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])
full_zip_url = res.json()["data"]["extract_result"][0]["full_zip_url"]
print(full_zip_url)

import zipfile
import io

response = requests.get(full_zip_url)
if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        for name in zf.namelist():
            if name.endswith('full.md'):
                with zf.open(name) as md_file:
                    md_content = md_file.read().decode('utf-8')
                    output_path = 'full.md'
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                    print(f"full.md 文件已成功提取到: {output_path}")
else:
    print(f"下载压缩文件失败，状态码: {response.status_code}")