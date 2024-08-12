from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain.document_loaders import TextLoader
import os

def load_file(file_path):
    file_type = file_path.split('.')[-1]
    if file_type == 'pdf':
        return PyMuPDFLoader(file_path)
    elif file_type == 'md':
        return UnstructuredMarkdownLoader(file_path)
    else:
        return TextLoader(file_path,encoding='utf-8')

def get_docs(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    # 遍历文件路径并把实例化的loader存放在loaders里
    loaders = [load_file(file_path) for file_path in file_paths]
            
    docs = []
    for loader in loaders: 
        docs.extend(loader.load())
    return docs

def split_docs(docs):
    # 分割文本
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,  # 每个文本块的大小。这意味着每次切分文本时，会尽量使每个块包含 1500 个字符。
        chunk_overlap = 150,  # 每个文本块之间的重叠部分。
        separators=["\n\n", "\n", "(?<=\。 )", " ", ""]
    )
    splitted_docs = text_splitter.split_documents(docs)
    return splitted_docs


def add_to_chormadb(folder_path,embedding,persist_directory='MyChroma'):
    docs=get_docs(folder_path)
    splitted_docs=split_docs(docs)
    from langchain.vectorstores.chroma import Chroma
    vectordb = Chroma.from_documents(
        documents=splitted_docs, 
        embedding=embedding,## 最大8k
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )
    vectordb.persist()
    print(f"向量库中存储的数量：{vectordb._collection.count()}")
    return vectordb

def retrieval(instruct,vectordb,k=4):
    sim_docs = vectordb.similarity_search(instruct,k=k)
    sim_docs_list=[doc.page_content for doc in sim_docs]
    input='\n\n'.join(sim_docs_list)
    return input

if __name__ == "__main__":
    from embeddings import DashScopeEmbeddings,ZhipuAIEmbeddings
    embedding = DashScopeEmbeddings(
        model="text-embedding-v2",
    )
    mode='build'
    if mode=='build':
        folder_path = 'notebook/test_input'
        vectordb=add_to_chormadb(folder_path,embedding,'MyChroma')
    else:
        from langchain.vectorstores.chroma import Chroma
        vectordb=Chroma(persist_directory='MyChroma',embedding_function=embedding)