import streamlit as st
from PIL import Image
from chemcrow.agents import ChemCrow


from langchain.callbacks import wandb_tracing_enabled
from chemcrow.agents import ChemCrow, make_tools
from chemcrow.frontend.streamlit_callback_handler import \
    StreamlitCallbackHandlerChem
from dotenv import load_dotenv

load_dotenv()
ss = st.session_state
ss.prompt = None   

with st.sidebar:
    
    chemcrow_logo = Image.open('icon/chemcrow.png')
    st.image(chemcrow_logo)
openai = st.text_input("OpenAI API Key", type="password")
#111    
def response(input_text):
    model = ChemCrow(model="gpt-4-0613", temp=0.1, streaming=False)
    # model.run("What is the molecular weight of tylenol?")
    response = model.run(input_text)
    return response
    


input_text = st.text_input()
if not openai.startswith("sk-"):
    st.warning("Please enter your OpenAI API key!", icon="⚠")
else:
    response(input_text)

# user_input = st.chat_input()
# st.markdown(user_input)

#222
agent = ChemCrow(
    model='gpt-4-0613',
    tools_model='gpt-4-turbo-preview',
    temp=0.1,
    openai_api_key=ss.get('api_key'),
    api_keys={
        'RXN4CHEM_API_KEY': st.secrets['RXN4CHEM_API_KEY'],
        'CHEMSPACE_API_KEY': st.secrets['CHEMSPACE_API_KEY']
    }
).agent_executor
def run_prompt(prompt):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandlerChem(
            st.container(),
            max_thought_containers = 3,
            collapse_completed_thoughts = False,
            output_placeholder=ss
        )
        try:
            with wandb_tracing_enabled():
                response = agent.run(prompt, callbacks=[st_callback])
                st.write(response)
        except openai.error.AuthenticationError:
            st.write("Please input a valid OpenAI API key")
        except openai.error.APIError:
            # Handle specific API errors here
            print("OpenAI API error, please try again!")
