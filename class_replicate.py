import replicate
import os
os.environ['REPLICATE_API_TOKEN'] = "47f8ffa2bb04f8a6e67cb1cf9e3f89ce78f384cb"

class Replicate_API:
    
    def __init__(self,input,model_name="cjwbw/anything-v3-better-vae",model_version="09a5805203f4c12da649ec1923bb7729517ca25fcac790e640eaa9ed66573b65"):
        self.model = replicate.models.get(model_name)
        self.version = self.model.versions.get(model_version)
        self.input = input
    def get_result(self):
        inputs = {
            # Input prompt
            'prompt': self.input,

            # Specify things to not see in the output
            # 'negative_prompt': ...,

            # Width of output image. Maximum size is 1024x768 or 768x1024 because
            # of memory limits
            'width': 512,

            # Height of output image. Maximum size is 1024x768 or 768x1024 because
            # of memory limits
            'height': 512,

            # Prompt strength when using init image. 1.0 corresponds to full
            # destruction of information in init image
            'prompt_strength': 0.8,

            # Number of images to output.
            # Range: 1 to 4
            'num_outputs': 1,

            # Number of denoising steps
            # Range: 1 to 500
            'num_inference_steps': 11,

            # Scale for classifier-free guidance
            # Range: 1 to 20
            'guidance_scale': 7,

            # Choose a scheduler.
            'scheduler': "DPMSolverMultistep",

            # Random seed. Leave blank to randomize the seed
            # 'seed': ...,
        }
       
        output = self.version.predict(**inputs)
        return output
