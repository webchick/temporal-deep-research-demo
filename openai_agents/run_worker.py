from __future__ import annotations

import os
import asyncio
import logging
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env',override=True)

logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("openai.agents").setLevel(logging.CRITICAL)

from temporalio.client import Client
from temporalio.common import RetryPolicy
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin, ModelActivityParameters

from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.worker import Worker
from openai_agents.workflows.image_generation_activity import generate_image
from openai_agents.workflows.interactive_research_workflow import (
    InteractiveResearchWorkflow,
)
from openai_agents.workflows.pdf_generation_activity import generate_pdf


async def main():
    logging.basicConfig(level=logging.INFO)
    print("Starting worker...")
    print(f"Connecting to Temporal at {os.getenv('TEMPORAL_ENDPOINT')} in namespace {os.getenv('TEMPORAL_NAMESPACE')}")

    # Create client connected to server at the given address
    client = await Client.connect(
        os.getenv('TEMPORAL_ENDPOINT'),
        namespace= os.getenv('TEMPORAL_NAMESPACE'),
        api_key=os.getenv('TEMPORAL_API_KEY'),
        tls=True,
        plugins=[
            OpenAIAgentsPlugin(
                model_params=ModelActivityParameters(
                    start_to_close_timeout=timedelta(seconds=90),
                    schedule_to_close_timeout=timedelta(seconds=500),
                    retry_policy=RetryPolicy(
                        backoff_coefficient=2.0,
                        initial_interval=timedelta(seconds=1),
                        maximum_interval=timedelta(seconds=5),
                    ),
                )
            ),
        ],
        data_converter=pydantic_data_converter,
    )

    print("Client created, creating worker...")
    worker = Worker(
        client,
        task_queue="research-queue",
        workflows=[
            InteractiveResearchWorkflow,
        ],
        activities=[
            generate_pdf,
            generate_image
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
