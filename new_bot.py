# new_bot.py
import os
import discord
import generate

from discord.commands import Option
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Bot()

@bot.slash_command(guild_ids=['930209526362284042'])
async def generate_image(
        ctx: discord.ApplicationContext,
        prompts: Option(str, "Text prompts ex. (apple | surreal:0.5)", default=""),
        image_prompts: Option(str, "Image prompts/target image URL ex. (apple | surreal:0.5)", default=""),
        max_iterations: Option(int, "Number of iterations", default=500),
        display_freq: Option(int, "Save image iterations", default=50),
        width: Option(int, "Image width", default=256),
        height: Option(int, "Image height", default=256),
        init_image: Option(str, "Initial image URL", default=""),
        init_noise: Option(str, "Initial noise image", choices=["pixels", "gradient"], default=""),
        init_weight: Option(str, "Initial weight (float)", default="0"),
        clip_model: Option(str, "CLIP model (e.g. ViT-B/32, ViT-B/16)", choices=["ViT-B/32", "ViT-B/16"], default="ViT-B/32"),
        noise_prompt_seeds: Option(str, "Noise prompt seeds ex. (1|2|3)", default=""),
        noise_prompt_weights: Option(str, "Noise prompt weights ex. (1.0|.2|3.0)", default=""),
        step_size: Option(str, "Learning rate", default="0.1"),
        cut_method: Option(str, choices=['original','updated','nrupdated','updatedpooling','latest'], default='latest'),
        cutn: Option(int, "Number of cuts", default=32),
        cut_pow: Option(int, "Cut power", default="1"),
        seed: Option(int, "Seed", default=-1),
        optimiser: Option(str, "Optimiser", choices=['Adam','AdamW','Adagrad','Adamax','DiffGrad','AdamP','RAdam','RMSprop'], default='Adam'),
        output: Option(str, "Output image filename", default="output.png"),
    ):
  
    await ctx.respond("Generating image! Check back in a couple of minutes")
    final_args = {}
    final_args['prompts'] = prompts
    final_args['image_prompts'] = image_prompts
    final_args['max_iterations'] = max_iterations
    final_args['display_freq'] = display_freq
    final_args['size'] = [width, height]
    final_args['init_image'] = init_image
    final_args['init_noise'] = init_noise
    final_args['init_weight'] = float(init_weight)
    final_args['clip_model'] = clip_model
    final_args['vqgan_config'] = 'checkpoints/vqgan_imagenet_f16_16384.yaml'
    final_args['vqgan_checkpoint'] = 'checkpoints/vqgan_imagenet_f16_16384.ckpt'
    final_args['noise_prompt_seeds'] = [] if not noise_prompt_seeds else [int(x.strip()) for x in noise_prompt_seeds.split("|")]
    final_args['noise_prompt_weights'] = [] if not noise_prompt_weights else [float(x.strip()) for x in noise_prompt_weights.split("|")]
    final_args['step_size'] = float(step_size)
    final_args['cut_method'] = cut_method
    final_args['cutn'] = cutn
    final_args['cut_pow'] = float(cut_pow)
    final_args['seed'] = None if seed == -1 else seed
    final_args['optimiser'] = optimiser
    final_args['output'] = output

    final_args['make_video'] = False
    final_args['make_zoom_video'] = False
    final_args['zoom_start'] = 0
    final_args['zoom_frequency'] = 10
    final_args['zoom_scale'] = 0.99
    final_args['zoom_shift_x'] = 0
    final_args['zoom_shift_y'] = 0
    final_args['prompt_frequency'] = 0
    final_args['video_length'] = 10
    final_args['output_video_fps'] = 0
    final_args['input_video_fps'] = 15
    final_args['cudnn_determinism'] = False
    final_args['augments'] = [],
    final_args['video_style_dir'] = None
    final_args['cuda_device'] = 'cuda:0'

    



    # print(final_args)
    generate.generate_image(final_args)


    with open(output, "rb") as fh:
        f = discord.File(fh, filename="output.png")
    await ctx.respond(file=f)
    await ctx.respond(final_args)

print("VQGAN discord bot up and running!")
bot.run(TOKEN)