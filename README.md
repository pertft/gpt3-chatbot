# gpt3-chatbot

## Setup
* python -m venv env
* *activate env*
* pip install -r requirement.txt


## Delete files and Finetune
curl https://api.openai.com/v1/files/\<FILE\> -X DELETE -H 'Authorization: Bearer \<API KEY\>'

curl https://api.openai.com/v1/fine-tunes -X POST -H "Content-Type: application/json" -H "Authorization: Bearer \<API KEY\>" -d '{"training_file": "\<FILE\>"}'
