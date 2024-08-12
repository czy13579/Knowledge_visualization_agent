def KnowledgeGenerator(llm,instruct):
    generate_knowledge_prompt="""
    我需要{instruct}。请保证生成完成该任务所需要的知识提示，请保证生成的知识提示尽可能详细，覆盖到所有有必要的内容。
    知识提示：
    """
    from langchain_core.prompts import ChatPromptTemplate
    generate_knowledge_prompt_template = ChatPromptTemplate.from_template(generate_knowledge_prompt)
    prompt= generate_knowledge_prompt_template.format_messages(
        instruct=instruct
    )
    generated_knowledge=llm(prompt).content
    return generated_knowledge