
async def startup(ctx):
    print('Worker is alive. Waiting for job')

async def shutdown(ctx):
    print('disconnecting')

async def before_process(ctx):
    print('about to do task')

async def after_process(ctx):
    print('Finished task')