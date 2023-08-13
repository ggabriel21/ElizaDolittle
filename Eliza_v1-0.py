import streamlit as st

import openai

API_STRING_PREFIX="sk-"
EXPECTED_API_KEY_LENGTH = len(API_STRING_PREFIX)

WhoYouAre="Psicologa"
Roles2Play={"Psicologa":"Psicologia", "Medica":"Medicina",  "Advogada":"Advocacia" }
WhatYouDo = Roles2Play[WhoYouAre]

st.set_page_config(page_title=" \U0001f99cChatBot\U0001f99c  \U0001f4ac  I2A2 -  ElizaBoth ")


if "api_key" not in st.session_state.keys():
    st.session_state.api_key=False
   
with st.sidebar:
    st.title(" \U0001f99c Chat I2A2 \U0001f99c  - ElizaBoth")
    api_key = st.sidebar.text_input("Entre sua API Key", type="password")
    
    st.session_state.api_key=False

    if api_key.startswith(API_STRING_PREFIX) and len(api_key) > EXPECTED_API_KEY_LENGTH:
        st.sidebar.success("API Key em formato valido!")
        # st.sidebar.info(api_key)
        openai.api_key=api_key
        st.session_state.api_key=api_key
        st.success('Pode iniciar o chat escrevendo prompts ao lado ==>', icon='\U0001f449')

    elif api_key:
        if not api_key.startswith("sk-"):
            st.sidebar.error("API Key Invalida! Deve comecar com 'sk-'")
        if len(api_key) <= EXPECTED_API_KEY_LENGTH:
            st.sidebar.error(f"API Key tamanho invalido! ")
        st.session_state.api_key=False
    
    st.warning("\n\nEliza \u00e9 muito conversadeira!!\nSe ela se desviar do assunto apenas diga: Isso n\u00e3o \u00e9 psicologia!!!")

    # st.write("\n\n")    
    # st.info("Eliza por default \u00e9 Psic\u00f3loga!")
    WhoYouAre="Psicologa"    
    # WhoYouAre = st.radio("Mas ela tambem pode ser:", ('Psicologa', 'Medica', 'Advogada'))
    WhatYouDo = Roles2Play[WhoYouAre]
    # print(WhoYouAre, WhatYouDo)

    
# Funcao para gerar resposta da OPENAI

def generate_response(prompt_input_all):
    try:
        chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt_input_all
        )
    except:
        st.sidebar.error("Verifique sua conexao ou APIKey. Algo errado na comunicacao")
        return ("Erro na comunicacao")
    response = chat.choices[0].message.content
    return (response)


def verificar_prompt(prompt):
    return(True)
       

msg_condicionamento=f"Voc\u00ea \u00e9 uma Assistente virtual de psicologia. Voc\u00ea vai ser chamada de Eliza. Mas quero que voc\u00ea responda como {WhoYouAre}.  Voc\u00ea s\u00f3 DEVE responder quest\u00f5es relativas a {WhatYouDo} ou fazer afirmac\u00f5es sobre {WhatYouDo}. Nao responda sobre outros assuntos. Para outros assuntos que nao forem de {WhatYouDo} responda APENAS que o assunto est\u00e1 fora de escopo e NADA mais! "

# Guardar informacoes de LLM

if "consultas" not in st.session_state.keys():
    st.session_state.consultas = [{"role": "system", "content": msg_condicionamento}]
	    

#if "check_msg" not in st.session_state.keys():
#    st.session_state.check_msg = [{"role": "system", "content": "Voce e um psicologo. Responda #POSITIVO se a questao a seguir e relativa a psicologia. Responda NEGATIVO no caso contrario."}]
    
# Mostrar todas as mensagens da area de chat
# Não mostrar as 2 primeiras (sistema e resposta)

if len(st.session_state.consultas) >2:
    for message in st.session_state.consultas[2:]:
        if st.session_state.consultas[-1]["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])



# print(msg_condicionamento)   
    
# prompt do usuario

if prompt := st.chat_input(disabled=not (st.session_state.api_key)):
    if verificar_prompt(prompt):
        st.session_state.consultas.append({"role": "user", "content":prompt})
        with st.chat_message("user"):
            st.write(prompt)
    else:
        st.sidebar.info("Prompt n\u00e3o \u00e9 relativo a assuntos requeridos!!!")


# Gera uma nova mensagem. se a ultima nao foi de assistant. Tem que ter key valida
# mandamos  mensagem de condicionamento juntamente com a input do usuario
# mas essa mensagem não é enviada para a tela

if (st.session_state.api_key) and st.session_state.consultas[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            x= msg_condicionamento + str(prompt)
            prompt_condicio = st.session_state.consultas.copy()
            prompt_condicio[-1]["content"]=x
            print("\n\n"+x+"\n")
            response = generate_response(st.session_state.consultas) 
            # response = "Acesso ao gtp bypassado!"
            prompt_condicio[-1]["content"]=str(prompt)
            if len(st.session_state.consultas) >2:
                st.write(response)
            else:
                st.write("Estou aqui para ajudar com perguntas relacionadas \u00e0 Psicologia. Como posso auxili\u00e1-lo hoje?") 
            message = {"role": "assistant", "content": response}
            st.session_state.consultas.append(message)
  



