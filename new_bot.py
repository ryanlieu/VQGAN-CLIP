# new_bot.py
# import asyncio
import os
import discord
from discord.ext import commands
import generate

from discord.commands import Option
from dotenv import load_dotenv
from types import SimpleNamespace

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(
    command_prefix="/",
    description="FWB VQGAN BOT",
    intents=discord.Intents.default()
)

@bot.slash_command(name="generate_image", description="Creates a VQGAN+CLIP generated image, see options for details", guild_ids=['930209526362284042'])
@commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
async def generate_image(
        ctx: discord.ApplicationContext,
        prompts: Option(str, "Text prompts ex. (apple | surreal:0.5)", default=""),
        image_prompts: Option(str, "Image prompts/target image URL ex. (https://fwb.com/image.png)", default=""),
        max_iterations: Option(int, "Number of iterations", default=300),
        display_freq: Option(int, "Save image iterations", default=50),
        width: Option(int, "Image width", default=256),
        height: Option(int, "Image height", default=256),
        init_image: Option(str, "Initial image URL ex. (https://fwb.com/image.png)", default=""),
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
  
    await ctx.respond("Generating image! Check back in a couple of minutes.")
    final_args = SimpleNamespace()
    setattr(final_args, 'prompts', prompts)
    setattr(final_args, 'image_prompts', image_prompts)
    setattr(final_args, 'max_iterations', max_iterations)
    setattr(final_args, 'display_freq', display_freq)
    setattr(final_args, 'size', [width, height])
    setattr(final_args, 'init_image', init_image)
    setattr(final_args, 'init_noise', init_noise)
    setattr(final_args, 'init_weight', float(init_weight))
    setattr(final_args, 'clip_model', clip_model)
    setattr(final_args, 'vqgan_config', 'checkpoints/vqgan_imagenet_f16_16384.yaml')
    setattr(final_args, 'vqgan_checkpoint', 'checkpoints/vqgan_imagenet_f16_16384.ckpt')
    setattr(final_args, 'noise_prompt_seeds', [] if not noise_prompt_seeds else [int(x.strip()) for x in noise_prompt_seeds.split("|")])
    setattr(final_args, 'noise_prompt_weights', [] if not noise_prompt_weights else [float(x.strip()) for x in noise_prompt_weights.split("|")])
    setattr(final_args, 'step_size', float(step_size))
    setattr(final_args, 'cut_method', cut_method)
    setattr(final_args, 'cutn', cutn)
    setattr(final_args, 'cut_pow', float(cut_pow))
    setattr(final_args, 'seed', None if seed == -1 else seed)
    setattr(final_args, 'optimiser', optimiser)
    setattr(final_args, 'output', output)
    setattr(final_args, 'make_video', False)
    setattr(final_args, 'make_zoom_video', False)
    setattr(final_args, 'zoom_start', 0)
    setattr(final_args, 'zoom_frequency', 10)
    setattr(final_args, 'zoom_scale', 0.99)
    setattr(final_args, 'zoom_shift_x', 0)
    setattr(final_args, 'zoom_shift_y', 0)
    setattr(final_args, 'prompt_frequency', 0)
    setattr(final_args, 'video_length', 10)
    setattr(final_args, 'output_video_fps', 0)
    setattr(final_args, 'input_video_fps', 15)
    setattr(final_args, 'cudnn_determinism', False)
    setattr(final_args, 'augments', [])
    setattr(final_args, 'video_style_dir', None)
    setattr(final_args, 'cuda_device', 'cuda:0')

    final_output = await generate.generate_image(final_args)
    with open(final_output, "rb") as fh:
        f = discord.File(fh, filename=final_output)
    await ctx.respond(file=f)
    # await ctx.respond(final_args)

@generate_image.error
async def on_command_error(ctx,error):
    if isinstance(error, commands.MaxConcurrencyReached):
        await ctx.respond('Bot is currently generating an image! Check back in a couple of minutes.')
    else:
        await ctx.respond('Bot ran into an error, try again or have someone reset the bot.')

print("VQGAN discord bot up and running!")
bot.run(TOKEN)