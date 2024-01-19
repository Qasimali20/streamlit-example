from django.shortcuts import render
from django.http import HttpResponse
import openai
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api.service_pb2 import GetModelRequest
import openai
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai.client.model import Model
from clarifai.client.input import Inputs
from dotenv import load_dotenv
from decouple import config
from decouple import config
from django.http import HttpResponse
from django.shortcuts import render
import base64
from django.shortcuts import render
from django.http import JsonResponse
import os

CLARIFAI_PAT = config('CLARIFAI_PAT')
DEBUG = config('DEBUG', default=True, cast=bool)
openai.api_key ='7a721760203b47449d49d281dd2f3c9c'
CLARIFAI_PAT = os.getenv('CLARIFAI_PAT')

def index(request):
    return render(request, 'main.html')

def page(request):
    # Your logic for processing the form data and making API calls goes here
    if request.method == 'POST':
        picture = request.FILES.get('picture')
        description = request.POST.get('description')

        
        ######################################################################################################
        # In this section, we set the user authentication, user and app ID, model details, and the URL of
        # the text we want as an input. Change these strings to run your own example.
        ######################################################################################################
        CLARIFAI_PAT = os.getenv('CLARIFAI_PAT')

        # Your PAT (Personal Access Token) can be found in the portal under Authentification
        PAT = '7a721760203b47449d49d281dd2f3c9c'
        # Specify the correct user_id/app_id pairings
        # Since you're making inferences outside your app's scope
        USER_ID = 'openai'
        APP_ID = 'chat-completion'
        # Change these to whatever model and text URL you want to use
        MODEL_ID = 'GPT-4'
        MODEL_VERSION_ID = '5d7a50b44aec4a01a9c492c5a5fcf387'
        RAW_TEXT = description
        # To use a hosted text file, assign the url variable
        # TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
        # Or, to use a local text file, assign the url variable
        # TEXT_FILE_LOCATION = 'YOUR_TEXT_FILE_LOCATION_HERE'

        ############################################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
        ############################################################################

        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)

        metadata = (('authorization', 'Key ' + PAT),)

        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

        # To use a local text file, uncomment the following lines
        # with open(TEXT_FILE_LOCATION, "rb") as f:
        #    file_bytes = f.read()

        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=RAW_TEXT
                                # url=TEXT_FILE_URL
                                # raw=file_bytes
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0]




        IMAGE_FILE_LOCATION = picture  # Provide the actual file location if available, or keep it as an empty string
        prompt = "Write its description?"
        inference_params = dict(temperature=0.2, max_tokens=100)

        try:
            file_bytes = picture.read()


            model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(
                inputs=[Inputs.get_multimodal_input(input_id="", image_bytes=file_bytes, raw_text=prompt)],
                inference_params=inference_params
            )
            text_content = model_prediction.outputs[0].data.text.raw



        except FileNotFoundError:
            print("No image file provided.Make a prediction without an image.")
            text_content=''
        except Exception as e:
            print(f"An error occurred: {e}")
            text_content=''
        clarifai_pat = os.getenv("CLARIFAI_PAT")


        openai.api_key ='b2e1a805f4b7405d87dcd52f816f6328'

        ######################################################################################################
        # In this section, we set the user authentication, user and app ID, model details, and the URL of
        # the text we want as an input. Change these strings to run your own example.
        ######################################################################################################

        # Your PAT (Personal Access Token) can be found in the portal under Authentification
        PAT = "7a721760203b47449d49d281dd2f3c9c"
        # Specify the correct user_id/app_id pairings
        # Since you're making inferences outside your app's scope
        USER_ID = 'openai'
        APP_ID = 'chat-completion'
        # Change these to whatever model and text URL you want to use
        MODEL_ID = 'GPT-4'
        MODEL_VERSION_ID = '5d7a50b44aec4a01a9c492c5a5fcf387'
        RAW_TEXT = str(output) + " " + str(text_content)
        # To use a hosted text file, assign the url variable
        # TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
        # Or, to use a local text file, assign the url variable
        # TEXT_FILE_LOCATION = 'YOUR_TEXT_FILE_LOCATION_HERE'

        ############################################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
        ############################################################################

        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)

        metadata = (('authorization', 'Key ' + PAT),)

        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

        # To use a local text file, uncomment the following lines
        # with open(TEXT_FILE_LOCATION, "rb") as f:
        #    file_bytes = f.read()

        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=RAW_TEXT
                                # url=TEXT_FILE_URL
                                # raw=file_bytes
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0]


        prompt = output.data.text.raw


        inference_params = dict(quality="standard", size= '1024x1024')

        # Model Predict
        model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3", pat=PAT).predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)

        output_base64 = model_prediction.outputs[0].data.image.base64

        with open('image.png', 'wb') as f:
            f.write(output_base64)

    # Read the image file as base64
        with open('image.png', 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        return render(request, 'RESULT_PAGE.html', {'img_data': img_data, 'description': description})
    else:
        return render(request, 'secondPage.html')