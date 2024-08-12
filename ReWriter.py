def instruct_rewriter(llm,instruct):
    instruct_rewriter_prompt="""
    下面给出一个指令，你需要对其进行重写，请保证重写后的指令包含原始指令所有信息，尽可能详细，请以“我需要“开头。
    原始指令:{instruct}
    重写后指令：
    """
    from langchain_core.prompts import ChatPromptTemplate
    instruct_rewriter_prompt_template = ChatPromptTemplate.from_template(instruct_rewriter_prompt)
    prompt= instruct_rewriter_prompt_template.format_messages(
        instruct=instruct
    )
    new_instruct = llm(prompt).content
    return new_instruct

def contents_rewriter(llm,instruct,input):
    from langchain_core.prompts import ChatPromptTemplate
    rewriter_prompt="""
    {instruct}。下面给出几个段落，你需要对其进行重写，请保证重写后的文本尽可能详细，内容完整流畅、顺序正确，并适当\
    补充你认为需要补充的内容。
    输入:{input}
    重写结果：
    """
    rewriter_prompt_template = ChatPromptTemplate.from_template(rewriter_prompt)
    #print(rewriter_prompt_template)
    prompt= rewriter_prompt_template.format_messages(
        instruct=instruct,
        input=input
    )
    rewrited_input = llm(prompt).content
    return rewrited_input