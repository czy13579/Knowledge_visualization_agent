end_token='<|im_end|>'

## 各种图的提示词
bubble_map_instruction=f'我将给你一个文本，请找出文本的中心事件，并根据文本总结中心事件的相关属性和简短的描述，并按下面格式输出。\n \
## 中心事件:[中心事件名称]\n \
### 属性1:[属性名]\n \
#### 属性描述:[简短的描述]\n\
### 属性2:[属性名]\n \
#### 属性描述:[简短的描述]\n\
### 属性n:[属性名]\n \
#### 属性描述:[简短的描述]\n\
{end_token}'

double_bubble_map_instruction=f'我将给你一个用于比较两个事物的文本，请找出两个事物，并根据下面格式总结两个事物的共同点和不同点。\n \
## 比较对象: [对象1]，[对象2]\n \
### 相同点:\n \
#### 相同点1:[简短的描述]\n\
#### 相同点2:\n \
#### 相同点n:\n \
### 对象1独有的特点:\n\
#### 特点1:[简短的描述]\n \
#### 特点2:\n \
#### 特点n:\n \
### 对象2独有的特点:\n\
#### 特点1:[简短的描述]\n \
#### 特点2:\n \
#### 特点n:\n \
{end_token}'

tree_map_instruction=f'我将给你一个用于介绍某个事物相关类别的文本，请找出中心事物，并根据下面格式简短地总结事物的主要类别。\n \
## 一级类别: [中心事物]\n \n \
### 二级类别1:\n \
- 三级类别1:[简短的描述]\n \
- 三级类别2:\n \
- 三级类别n:\n \
\n \
### 二级类别2:\n \
- 三级类别1:[简短的描述]\n \
- 三级类别2:\n \
- 三级类别n:\n \
\n \
### 二级类别m:\n \
- 三级类别1:[简短的描述]\n \
- 三级类别2:\n \
- 三级类别n:\n \
{end_token}'

#parts=['背景','过程','意义']
brace_map_instruction='我将给你一个文本，请先找出中心事件，然后分背景、过程、意义几个部分总结文本，请按下面格式输出。\n \
## 中心事件:[中心事件名称]\
### 部分1：[名称]\n\
 - \
 - \
### 部分2：\n\
 - \
 - \
### 部分n：\n\
 - \
 - \
'+end_token

flow_map_instruction=f'我将给你一个文本，请按时间顺序将事件划分为若干个阶段(不超过5个),每个阶段包括若干个子事件，并按下面格式进行总结。\n \
## 阶段1:\n \
- 子事件1:[简短的描述]\n \
- 子事件2:\n \
- 子事件m:\n \
## 阶段2:\n \
- 子事件1:[简短的描述]\n \
- 子事件2:\n \
- 子事件m:\n \
## 阶段n:\n \
- 子事件1:[简短的描述]\n \
- 子事件2:\n \
- 子事件m:\n \
{end_token}'

multi_flow_map_instruction=f'我将给你一个描述了一个事件的文本，请找出事件名称，并简短地总结事件的原因和影响，按下面格式输出。\n \
## 事件:[事件名称]\n \
### 原因：\
- 原因1 \
- 原因2 \
- 原因n \
### 影响：\
- 影响1 \
- 影响2 \
- 影响m \
{end_token}'


# 多提示路由模板
MULTI_PROMPT_ROUTER_TEMPLATE = """给语言模型一个原始文本输入，\
让其选择最适合输入的模型提示。\
系统将为您提供可用提示的名称以及最适合改提示的描述。\
如果你认为修改原始输入最终会导致语言模型做出更好的响应，\
你也可以修改原始输入。


<< 格式 >>
返回一个带有JSON对象的markdown代码片段，该JSON对象的格式如下：
```json
{{{{
    "destination": 字符串 \ 使用的提示名字或者使用 "DEFAULT"
    "next_inputs": 字符串 \ 原始输入的改进版本
}}}}



记住：“destination”必须是下面指定的候选提示名称之一，\
或者如果输入不太适合任何候选提示，\
则可以是 “DEFAULT” 。
记住：如果您认为不需要任何修改，\
则 “next_inputs” 可以只是原始输入。

<< 候选提示 >>
{destinations}

<< 输入 >>
{{input}}

<< 输出 (记得要包含 ```json)>>

样例:
<< 输入 >>
"总结地球的气候类型"
<< 输出 >>
```json
{{{{
    "destination": 字符串 \ 使用的提示名字或者使用 "DEFAULT"
    "next_inputs": 字符串 \ 原始输入的改进版本
}}}}

"""

## 各种类型图的指令
instruction_dict={
    '气泡图':bubble_map_instruction,
    '双泡图':double_bubble_map_instruction,
    '树形图':tree_map_instruction,
    '组织图':brace_map_instruction,
    '流程图':flow_map_instruction,
    '复流程图':multi_flow_map_instruction
}
descriptions=[
    '擅长找出中心事物的多个属性，进而将输入文本结构化成气泡图所需形式。',
    '擅长对比两个事物，能够找出两个事物的相同点和不同点，进而将输入文本结构化成双泡图所需形式。',
    '擅长对事物进行分类，能够找出中心事物的主要类别，能够把进而将输入文本结构化成树形图所需形式。',
    '擅长总结出事情的背景、过程、意义，进而将输入文本结构化成组织图所需形式。',
    '擅长梳理事件的顺序，能够按时间顺序将事件划分为若干个阶段，进而将输入文本结构化成流程图所需形式。',
    '擅长总结事件的原因和影响，进而将输入文本结构化成复流程图所需形式。',
]

name_list=list(instruction_dict.keys())
prompt_infos=[
    {
        '名字':name_list[i],
        '描述':descriptions[i],
    } for i in range(len(name_list))
]

