# To install & run
1. Create `.env` file and put `OPENAI_API_KEY=<key>` in it.
2. Create an environment by running `python -m venv .venv` and activating it with `.\.venv\Scripts\activate`
3. Download the dependencies by running `pip install -r requirements.txt`.
4. Run with `python main.py`

# Classes
* Candy - a class with a number of useful ways to automate and simplify openai api queries.
`candy.py`
* Nougat - a class for interacting and querying sqlite db for similar concepts.
`nougat.py`