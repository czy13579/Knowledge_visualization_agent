from prompts import instruction_dict,MULTI_PROMPT_ROUTER_TEMPLATE,prompt_infos
from langchain_core.prompts import ChatPromptTemplate

destinations = [f"{p['名字']}: {p['描述']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

## 指令prompt
alpaca_prompt = """下面是描述任务的指令，并配有提供进一步上下文的输入。请按指令要求给出合适的回答。

### 指令:
{instruct}

### 输入:
{input}

### 回答:
"""
def run_MultiPromptChain(llm,instruct,input):
    from langchain.chains.router import MultiPromptChain  #导入多提示链
    from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain 

    ## 准备多个路由并封装成链

    ## 设置默认路由
    default_prompt = ChatPromptTemplate.from_template(alpaca_prompt.format(instruct='{input}',input=input))
    default_chain = LLMChain(llm=llm, prompt=default_prompt)

    ## 构造destination_chains
    destination_chains = {}
    for p_info in prompt_infos:
        name = p_info["名字"]
        prompt_template = alpaca_prompt.format(instruct=instruction_dict[name],input=input)
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chains[name] = chain  

    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
        destinations=destinations_str
    )

    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )

    router_chain = LLMRouterChain.from_llm(llm, router_prompt)

    #使用MultiPromptChain选择某个链，然后再去执行此链
    chain = MultiPromptChain(router_chain=router_chain,    #l路由链路
                             destination_chains=destination_chains,   #目标链路
                             default_chain=default_chain,      #默认链路
                             verbose=True   
                            )
    print(chain)
    results=chain.run(instruct)
    return results