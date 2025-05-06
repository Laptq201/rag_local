from typing import List 
import re 
from collections import deque 



def text_chunk(text: str, max_length: int = 1000) -> List[str]:
    #split to sentences (sentences = ending = . ! ?)
    sentences = deque(re.split(r'(?<=[.!?])\s', text.replace('\n', ' ')))
    chunks = []
    chunk_text = ""

    while sentences:
        sentence = sentences.popleft()
        if sentence:
            #Nếu độ dài của câu lớn hơn độ dài max_length và chunk_text không rỗng thì thêm chunk_text vào chunks
            if len(sentence) + len(chunk_text) > max_length and chunk_text:
                chunks.append(chunk_text)
                chunk_text = sentence 
            else:
                chunk_text += sentence + " "
    
    #Thêm toàn bộ từ dư còn lại vào chunks
    if chunk_text:
        chunks.append(chunk_text)
    
    return chunks