from src import retriever  
docs = retriever.retrieve('What is the exit load for the large cap fund?')  
for d in docs: print('CHUNK:', d['content'][:100].replace('\n', ' '))  
