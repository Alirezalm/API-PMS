#!/bin/bash

echo -e "Seazone Challenge \nAuthor: Alireza Olama\nEmail: alireza.lm69@gmail.com\n\n"



DIR="./env"


if [ -d $DIR ]; then

    echo -e "Activating ... \n\n"

    source ./env/bin/activate
else

    echo -e " Creating virtual environment ... \n\n"
    python3 -m venv env
    echo -e "Activating ... \n\n"

    source ./env/bin/activate
fi


echo -e "Done!\n\n"

echo -e "installing requirements ... \n\n"

pip install -r requirements.txt

echo -e "Done!\n\n"

echo -e "Executing the main program ...  \n\n"

echo -e "---------------------------\n\n"

python main.py

echo -e "Done!"
