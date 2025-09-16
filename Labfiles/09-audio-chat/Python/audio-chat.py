import os
import requests
import base64
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_endpoint = os.getenv("AC_PROJECT_ENDPOINT")
        model_deployment =  os.getenv("AC_MODEL_DEPLOYMENT")

        # Initialize the project client
        project_client = AIProjectClient(            
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            ),
            endpoint=project_endpoint,
        )


        # Get a chat client
        openai_client = project_client.get_openai_client(api_version="2024-10-21")
        

        # Initialize prompts
        #system_message = "You are an AI assistant for a produce supplier company."
        system_message = "You are an AI assistant with a charter to clearly analyse the customer enquiry."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the audio\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")

                # Encode the audio file
                # file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
                # response = requests.get(file_path)
                # #if response.raise_for_status() == 200:
                # if response.status_code == 200:
                #     audio_data = base64.b64encode(response.content).decode('utf-8')
                # else:
                #     print("Error: Unable to fetch the audio file.")
                #     continue   

                audio_folder = 'data/'
                path = os.path.dirname(os.path.abspath(__file__))
                data_folder = os.path.join(path, audio_folder)
                if not os.path.exists(data_folder):
                    print(f"data folder '{data_folder}' does not exist.")
                    return
                for file_name in os.listdir(data_folder):
                    # Read the file contents
                    print('\n-------------\n' + file_name)
                    audio_file = open(os.path.join(data_folder, file_name), "rb")
                    audio_data = encode_audio(audio_file)

                    # Get a response to audio input
                    response = openai_client.chat.completions.create(
                        model=model_deployment,
                        messages=[
                            {"role": "system", "content": system_message},
                            { "role": "user",
                                "content": [
                                { 
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "input_audio",
                                    "input_audio": {
                                        "data": audio_data,
                                        "format": "mp3"
                                    }
                                }
                            ] }
                        ]
                    )
                    print(response.choices[0].message.content)
                


    except Exception as ex:
        print(ex)

def encode_audio(audio_file):
        """Encode audio files in the specified folder to base64."""
        audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        audio_file.close()
        return audio_data


if __name__ == '__main__': 
    main()