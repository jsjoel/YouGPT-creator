import os
# from apikey import apikey
import streamlit as st
from langchain_community.llms import OpenAI, HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
# from langchain.utilities import wikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
os.environ['HUGGINGFACE_API_TOKEN'] = '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'

#app framework
st.title('🦜️🔗 YouGPTube Creator')
prompt = st.text_input("Plug in your input here","")

# Prompt tempolate
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = ' write me a youtube video title about {topic}'

)

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'],
    template = ' write me a youtube video script based on this tile TITLE: {title} while leveraging this wkipedia research:{wikipedia_research}'
    

)

# Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')



#LLMS
# llm = OpenAI(temperature=0.9)
llm = HuggingFaceHub(repo_id = "google/flan-t5-base", model_kwargs={"temperature":0.9, "max_length":512},  huggingfacehub_api_token="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")
title_chain = LLMChain(llm=llm, prompt= title_template, verbose=True, output_key='title', memory=title_memory )
script_chain = LLMChain(llm=llm, prompt= script_template, verbose=True, output_key='script', memory=script_memory )

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# suquential_chain = SequentialChain(chains=[title_chain, script_chain],input_variables=['topic'], output_variables=['title', 'script'] verbose=True)

# output in the screen
if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain.run(title=title,wikipedia_research=wiki_research)
    st.write(title)
    st.write(script)

    with st.expander('Title History'):
        st.info(title_memory.buffer)

    
    with st.expander('Script History'):
        st.info(script_memory.buffer)

    
    with st.expander('Wikipedia Research'):
        st.info(wiki_research)