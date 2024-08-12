import argparse
my_parser = argparse.ArgumentParser(description='文本结构化工具')

# Add the arguments
my_parser.add_argument("-i",    "--instruct", type=str, help="输入指令", default=None, dest='instruct')
my_parser.add_argument("-ip",    "--input_path", type=str, help="输入文本路径", default=None, dest='input_path')
my_parser.add_argument("-m",    "--model_name", type=str, help="模型名称", default="qwen2-7b-instruct", dest='model_name')
my_parser.add_argument("-me",    "--method", type=str, help="方法名称:RAG,generate,None", default=None, dest='method')
my_parser.add_argument("-pd",    "--persist_directory", type=str, help="数据库持久化路径", default=None, dest='persist_directory')
my_parser.add_argument("-rp",    "--resources_path", type=str, help="资源库路径", default=None, dest='resources_path')
my_parser.add_argument("-op",    "--output_path", type=str, help="输出路径", default='output.md', dest='output_path')
my_parser.add_argument("-rc",    "--rewrite_content", type=bool, help="是否重写输入", default=False, dest='rewrite_content')
my_parser.add_argument("-ri",    "--rewrite_instruct", type=bool, help="是否重写输入", default=False, dest='rewrite_instruct')
my_parser.add_argument("-mt",    "--map_type", type=str, help="绘制的图像类型", default=None, dest='map_type')
my_parser.add_argument("-sp",    "--save_path", type=str, help="输出图像路径", default='output', dest='save_path')
args = my_parser.parse_args()

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(),override=True)

from langchain.chat_models import ChatOpenAI
model_name=args.model_name
llm = ChatOpenAI(model=model_name,temperature=0)
instruct=args.instruct
if args.rewrite_instruct:
    from ReWriter import instruct_rewriter
    instruct=instruct_rewriter(llm,instruct)
    print('rewrited_instruct:',instruct)

def read_file(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        data=f.read()
    return data

def save_llm_respond(respond,save_path):
    with open(save_path,'w',encoding='utf-8') as f:
        f.write(respond)

if args.method=='RAG':
    from RAG import add_to_chormadb,retrieval
    from embeddings import DashScopeEmbeddings,ZhipuAIEmbeddings
    embedding = DashScopeEmbeddings(
            model="text-embedding-v2",
    )
    persist_directory=args.persist_directory
    if args.resources_path:
        folder_path = args.resources_path
        vectordb=add_to_chormadb(folder_path,embedding,persist_directory)
    from langchain.vectorstores.chroma import Chroma
    vectordb=Chroma(persist_directory=persist_directory,embedding_function=embedding)
    input=retrieval(instruct,vectordb,k=4)
elif args.method=='generate':
    from KnowledgeGenerator import KnowledgeGenerator
    input=KnowledgeGenerator(llm=llm,instruct=instruct)
else:
    input=read_file(args.input_path)

if args.rewrite_content:
    from ReWriter import contents_rewriter
    input=contents_rewriter(llm=llm,instruct=instruct,input=input)

from Structured_doc import run_MultiPromptChain
results=run_MultiPromptChain(llm=llm,instruct=instruct,input=input)
from IPython.display import display_markdown
display_markdown(results,raw=True)


save_llm_respond(results,args.output_path)
if args.map_type:
    from visual_tools import draw_map
    draw_map(args.map_type,args.output_path,args.save_path)
