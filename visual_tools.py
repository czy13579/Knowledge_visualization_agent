from graphviz import Digraph  
import matplotlib.pyplot as plt
import matplotlib.style as mls
mls.use('ggplot')

def show_map(save_path):
    image=plt.imread(save_path+'.png')
    h,w=image.shape[:2]
    plt.figure(figsize=(w*2/plt.rcParams['figure.dpi'], h*2/plt.rcParams['figure.dpi']))
    plt.imshow(image,aspect='auto')
    plt.axis('off')
    plt.show()

def prepare_text(text,max_len=10):
    new_text=[]
    while True:
        if len(text)>max_len:
            new_text.append(text[:max_len])
            text=text[max_len:]
        else:
            new_text.append(text+' '*(max_len*2-2*len(text)))
            break
    return '\\n'.join(new_text)

def draw_Bubble_Map(input,save_path='气泡图'):
    input=input.replace('<|im_end|>','').replace('\n\n','\n').replace('\n',' ')
    title='气泡图'
    dot = Digraph(comment=title,format='png',engine='circo') 
    dot.graph_attr['rankdir'] = 'LR'
    #dot.graph_attr['splines'] = 'line'
    dot.attr('node', fontname='simhei', fontsize='12')  
    dot.attr('edge', fontname='simhei', fontsize='10')  
    attribute_list=input.split(' ### ')
    root=attribute_list[0].split('## ')[-1]
    dot.node(root,root)
    for i,attribute in enumerate(attribute_list[1:]):
        attribute_name=attribute.split(' #### ')[0]
        description=attribute.split(' #### ')[-1]
        description=prepare_text(description.replace(' ',''))
        dot.node(attribute_name,attribute_name)
        dot.node(attribute_name+'描述',description,shape='none')
        dot.edge(root,attribute_name,color='red')
        dot.edge(attribute_name,attribute_name+'描述',color='red')
    dot.render(save_path, view=False, cleanup=True)

def draw_double_Bubble_Map(input,save_path='双泡图'):
    input=input.replace('<|im_end|>','').replace('\n\n','\n').replace('\n',' ')
    title='双泡图'
    dot = Digraph(comment=title,format='png',engine='circo') 
    dot.graph_attr['mindist'] = '2.0' 

    dot.attr('node', fontname='simhei', fontsize='20')   
    dot.attr('edge', fontname='simhei', fontsize='10') 
    attribute_list=input.split(' ### ')
    objects=attribute_list[0].split('## ')[-1].split('，')
    root1=objects[0]
    root2=objects[1]
    dot.node(root1,root1,shape='circle')
    dot.node(root2,root2,shape='circle')
    commonds=attribute_list[1].split(' #### ')[1:]
    for i,commond in enumerate(commonds):
        commond_name=commond
        commond_name=prepare_text(commond_name.replace(' ',''))
        dot.node(commond_name,commond_name)
        dot.edge(root1,commond_name,color='red')
        dot.edge(root2,commond_name,color='red')

    features1=attribute_list[2].split(' #### ')[1:]
    for i,feature in enumerate(features1):
        feature_name=feature
        feature_name=prepare_text(feature_name.replace(' ',''))
        dot.node(feature_name,feature_name)
        dot.edge(root1,feature_name,color='blue')

    features2=attribute_list[3].split(' #### ')[1:]
    for i,feature in enumerate(features2):
        feature_name=feature
        feature_name=prepare_text(feature_name.replace(' ',''))
        dot.node(feature_name,feature_name)
        dot.edge(root2,feature_name,color='blue')
    dot.render(save_path, view=False,cleanup=True)


def draw_tree_map(input,save_path='树状图'):
    input=input.replace('<|im_end|>','').replace('\n\n','\n').replace('**','').replace('\n',' ')
    title='树状图'
    dot = Digraph(comment=title,format='png',engine='dot') 
    dot.graph_attr['rankdir'] = 'LR'
    #dot.graph_attr['splines'] = 'line' 
    dot.attr('node', fontname='simhei', fontsize='12')   
    dot.attr('edge', fontname='simhei', fontsize='6') 
    attribute_list=input.split(' ### ')
    root=attribute_list[0].split('## ')[-1]
    dot.node(root,root)
    attribute_list=attribute_list[1:]
    for i,attribute in enumerate(attribute_list):
        attribute_name=attribute.split(' - ')[0]
        dot.node(attribute_name,attribute_name)
        dot.edge(root,attribute_name,color='red',arrowhead='none')
        features=attribute.split('-')[1:]
        for j,feature in enumerate(features):
            feature_name=feature.split(':')[0]
            description=feature.split(':')[-1]
            description=prepare_text(description.replace(' ',''))
            dot.node(description,description,shape='box')
            dot.node(feature_name,feature_name)
            dot.edge(attribute_name,feature_name,color='blue',arrowhead='none')
            dot.edge(feature_name,description,color='blue',arrowhead='none')
    dot.render(save_path, view=False,cleanup=True)


def draw_brace_map(input,save_path='组织图'):
    input=input.replace('<|im_end|>','').replace('\n\n','\n').replace('\n',' ')
    title='组织图'
    dot = Digraph(comment=title,format='png',engine='dot') 
    dot.graph_attr['rankdir'] = 'LR'
    dot.graph_attr['splines'] = 'line' 
    dot.attr('node', fontname='simhei', fontsize='12') 
    dot.attr('edge', fontname='simhei', fontsize='6')  
    attribute_list=input.split(' ### ')
    root=attribute_list[0].split('## ')[-1]
    dot.node(root,root)
    attribute_list=attribute_list[1:]
    for i,attribute in enumerate(attribute_list):
        attribute_name=attribute.split(' - ')[0]
        dot.node(attribute_name,attribute_name)
        dot.edge(root,attribute_name,color='red',tailport='e',headport='w',arrowhead='none')
        features=attribute.split(' - ')[1:]
        for j,feature in enumerate(features):
            description=feature.replace('\n','')
            description=prepare_text(description.replace(' ',''))
            dot.node(description,description,shape='box')
            dot.edge(attribute_name,description,color='blue',tailport='e',headport='w',arrowhead='none')
    dot.render(save_path, view=False,cleanup=True)

def draw_flow_map(input,save_path='流程图'):
    input=input.replace('<|im_end|>','').replace('\n','')
    title='流程图'
    stage_list=input.split('## ')[1:]
    node_name=['阶段'+str(i+1) for i in range(len(stage_list))]
    things_list=[]
    for stage in stage_list:
        things=[]
        stage_things=stage.split('- ')[1:]
        #print(stage_things)
        for thing in stage_things:
            things.append(thing.split(':')[-1])
        things_list.append(things)
    #print(node_name)
    #print(things_list)
    
    dot = Digraph(comment=title,format='png',engine='neato') 
    #dot.graph_attr['rankdir'] = 'LR'
    #dot.graph_attr['labeljust'] = 'l'
    dot.graph_attr['splines'] = 'True'
    dot.attr('node', fontname='simhei', fontsize='12')  # 设置节点默认字体  
    dot.attr('edge', fontname='simhei', fontsize='10')  # 设置边默认字体（如果边上有标签）  
    #dot.node('r',root)
    for i,name in enumerate(node_name):
        dot.node(str(i), name,pos=f'{i*3+1},2!')
    for i in range(len(node_name)-1):
        dot.edges([str(i)+str(i+1)]) 
    p=0
    for i in range(len(node_name)):
        with dot.subgraph(name=f'cluster_{i}') as c:
            for j,thing in enumerate(things_list[i]):
                thing=prepare_text(thing.replace(' ',''),4)
                c.node(str(i)+str(j),thing,shape='box',pos=f'{i*3+j},1!')
                dot.edge(str(i),str(i)+str(j),color='red',arrowhead='none')
                p+=1
    dot.render(save_path, view=False,cleanup=True) 

def draw_Multi_Flow_Map(input,save_path='复流程图'):
    input=input.replace('<|im_end|>','').replace('\n\n','\n').replace('\n',' ')
    title='复流程图'
    dot = Digraph(comment=title,format='png',engine='dot') 
    dot.graph_attr['rankdir'] = 'LR' 
    dot.graph_attr['splines'] ='line'
    dot.graph_attr['labeljust'] = 'left'  
    dot.attr('node', fontname='simhei', fontsize='12')   
    dot.attr('edge', fontname='simhei', fontsize='6')  
    attribute_list=input.split(' ### ')
    root=attribute_list[0].split('## ')[-1]
    dot.node(root,root,shape='box')
    attribute_list=attribute_list[1:]
    for i,attribute in enumerate(attribute_list):
        description_list=attribute.split(' - ')[1:]
        for j,description in enumerate(description_list):
            description=prepare_text(description.strip())
            
            if i==0:
                dot.node(description,description,shape='box')
                dot.edge(description,root,color='red',tailport='e',headport='w',arrowsize='0.5')
            else:
                dot.node(description,description,shape='box')
                dot.edge(root,description,color='blue',tailport='e',headport='w',arrowsize='0.5')

    dot.render(save_path, view=False,cleanup=True)

draw_function_dict={
    'bubble_map':draw_Bubble_Map,
    'double_bubble_map':draw_double_Bubble_Map,
    'tree_map':draw_tree_map,
    'brace_map':draw_brace_map,
    'flow_map':draw_flow_map,
    'multi_flow_map':draw_Multi_Flow_Map
}

def read_file(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        data=f.read()
    return data
def draw_map(map_type,input_or_txt_path,save_path):
    if '.txt' in input_or_txt_path or '.md' in input_or_txt_path :
        input=read_file(input_or_txt_path)
    else:
        input=input_or_txt_path
    draw=draw_function_dict[map_type]
    draw(input,save_path)
    show_map(save_path)