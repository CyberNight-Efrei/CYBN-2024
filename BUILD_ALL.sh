#!/bin/bash

# List of absolute paths to your scripts
scripts=(
"Crypto/Cascade/chall/build_docker.sh"
"Crypto/Shared Flag/chall/build_docker.sh"
"Crypto/Securechain 30.0/chall/build_docker.sh"
"Hardware/Laverie sans contact/chall/build_docker.sh"
"Misc/Ingénieur en phrase/chall/build_docker.sh"
"Misc/Pyjail/src/build_docker.sh"
"Reverse/M30W_Bot/build_docker.sh"
"System/Escabot/docker/build_docker.sh"
"System/Marche-pied/docker/build_docker.sh"
"System/Echelle/docker/build_docker.sh"
"Web/Coup de bol/web/build_docker.sh"
"Web/Co(mpressed)okies/web/build_docker.sh"
"Web/Mon Champion Prefere/chall/build_docker.sh"
"Web/Parseur Farceur/web/build_docker.sh"
"Web/JWT Kiddo/chall/build_docker.sh"
"Prog/Captcha 2/chall/build_docker.sh"
"Prog/Captcha 1/chall/build_docker.sh"
"Prog/Intro à la prog/chall/build_docker.sh"
)

# Loop through each script in the list
for script in "${scripts[@]}"
do
    echo "---------- $script ----------"
    # Extract the directory from the script path
    script_dir=$(pwd)/$(dirname "$script")

    # Change to the script's directory
    cd "$script_dir" || { echo "Failed to cd into $script_dir"; exit 1; }

    # Run the script or any other command you want to execute
    sudo bash $(basename "$script") || { echo "Failed to run $script"; exit 1; }

    # Optionally: go back to the original directory if needed
    cd - > /dev/null
done
