# Labeling Facebook comments with an LLM

In this repository we use a LLM to label facebook comments as racist or not. There's two basic tools here: a script that uses the raw html of comments on Facebook and puts them into a csv. The other script uses a LLM to label them.

N.B.: This repo was quickly created as part of an AI course. It is by _no means_ a tool for comment moderation. It's just a little inquiry into the effectiveness of LLM's when it comes to detecting racism in social media comments.

## Prerequisites

The code is written in python, you'll also need pip/conda to install some packages. Try and use a virtual environment for that. Install the needed packages with `pip install -r requirements.txt`.

For the labeling part, [AIMLAPI](https://aimlapi.com/) is used. This allows quickly switching between models. You can easily swap this with Open AI or any other provider that uses OpenAI's python library for communication with LLM's. Note: this library and AIMLAPI do not communicate with OpenAI's server unless you choose one of their models.

You should create a `secrets.json` file with your API key or load it in some other way where you do not commit it to the repo directly.
