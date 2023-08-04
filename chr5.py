import streamlit as st
from chatapi_key import apikey
import openai

openai.api_key = apikey


st.set_page_config(page_title=" \U0001f99cChatBot\U0001f99c  \U0001f4ac  I2A2 ")

if "escopo" not in st.session_state:
    st.session_state.escopo = "Internet"
    
with st.sidebar:
    st.title('\U0001f99c I2A2 Chat')
    if (apikey != None ) :
        st.success('GPT3 API KEY already provided!', icon='\u2705')
        hf_apikey = apikey
        st.success('Proceed to entering your prompt message!', icon='\U0001f449')
        st.radio('Escolher escopo',['Internet','Diretorio'], key="escopo")
    else:
        hf_apikey = st.text_input('Enter APIKEY:', type='password')

        if not (hf_apikey):
            st.warning('Please enter your credentials!', icon='\u26a0\ufe0f')
        else:
            st.success('Proceed to entering your prompt message!', icon='\U0001f449')
            st.radio('Escolher escopo',['Internet','Diretorio'], key="escopo")
    if st.session_state.escopo == "Diretorio":
        dir_files = st.text_input('Diretorio dos arquivos de busca => ', value="/diret/xyz/", max_chars=30)
        st.warning("Importing required modules")
        from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper,ServiceContext,StorageContext,load_index_from_storage
        from langchain import OpenAI
        import sys
        import os

@st.cache_data
def create_index(path):
	max_input = 4096
	tokens = 200
	chunk_size = 600 #for LLM, we need to define chunk size
	max_chunk_overlap = 20
	#define prompt
	promptHelper = PromptHelper(max_input,tokens,chunk_overlap_ratio=0.1,chunk_size_limit=chunk_size)
	#define LLM \u2014 there could be many models we can use, but in this example, let\u2019s go with OpenAI
	llmPredictor = LLMPredictor(llm=OpenAI(temperature=0,openai_api_key=apikey, model_name="text-ada-001", max_tokens=tokens))
	#load data \u2014 it will take all the .txtx files, if there are more than 1
	docs = SimpleDirectoryReader(path).load_data()
	#create vector index
	service_context = ServiceContext.from_defaults(llm_predictor=llmPredictor,prompt_helper=promptHelper)
	vectorIndex = GPTVectorStoreIndex.from_documents(documents=docs,service_context=service_context)
	vectorIndex.storage_context.persist(persist_dir = 'Store')
	return vectorIndex


def answerMe(question):
	storage_context = StorageContext.from_defaults(persist_dir = 'Store')
	index = load_index_from_storage(storage_context)
	query_engine = index.as_query_engine()
	response = query_engine.query(question)
	return response.reponse
		
	
def DiretorioSearch():
	if st.session_state.escopo == "Diretorio":
		if dir_files == "/diret/xyz/":
			with st.sidebar:
				st.warning("Waiting forPath in format /dir/subdi/ !!!")
		else:
			create_index(dir_files)
			with st.sidebar:
				st.warning("index executed !!!")
	if "messages" not in st.session_state.keys():
		st.session_state.messages = [{"role": "system", "content": "Qual a sua Query =>"}]

	# Display chat messages
	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.write(message["content"])

	if prompt := st.chat_input(disabled=not (hf_apikey)):
		st.session_state.messages.append({"role": "user", "content": prompt})
		with st.chat_message("user"):
			st.write(prompt)

	if st.session_state.messages[-1]["role"] != "assistant":
		with st.chat_message("assistant"):
			with st.spinner("Thinking..."):
			# response = generate_response(st.session_state.messages) 
				response = "Acesso ao query bypassado!"
				st.write(response) 
		message = {"role": "assistant", "content": response}
		st.session_state.messages.append(message)

			
	return

	
def InternetSearch():
	# Store LLM generated responses
	if "messages" not in st.session_state.keys():
	    st.session_state.messages = [{"role": "system", "content": "You are a kind helpful assistant."}]


	# Display chat messages
	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.write(message["content"])


	# Function for generating LLM response
	#def generate_response(prompt_input_all):
	#    chat = openai.ChatCompletion.create(
	#            model="gpt-3.5-turbo", messages=prompt_input_all
	#        )
	#    response = chat.choices[0].message.content
	#    return (response)
	#

	# User-provided prompt
	if prompt := st.chat_input(disabled=not (hf_apikey)):
		st.session_state.messages.append({"role": "user", "content": prompt})
		with st.chat_message("user"):
			st.write(prompt)


	# Generate a new response if last message is not from assistant
	if st.session_state.messages[-1]["role"] != "assistant":
		with st.chat_message("assistant"):
			with st.spinner("Thinking..."):
			# response = generate_response(st.session_state.messages) 
				response = "Acesso ao gtp bypassado!"
				st.write(response) 
		message = {"role": "assistant", "content": response}
		st.session_state.messages.append(message)
	return
	    
  

    
    


if st.session_state.escopo == "Diretorio":
	DiretorioSearch()
else: 
	InternetSearch()


