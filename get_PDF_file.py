import requests

pdf_url = 'https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf'
response = requests.get(pdf_url)

pdf_path = 'attention_is_all_you_need.pdf'
with open(pdf_path, 'wb') as file:
    file.write(response.content)