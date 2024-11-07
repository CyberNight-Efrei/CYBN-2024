CAT="reverse"
CHALL="meowbot-c2"
NAME="${CAT}_${CHALL}"
PORT=8080
HOST_PORT=8080

docker rm -f $NAME
docker image prune -f
docker build --tag=$NAME .

RUN=false
PRIV=false

while getopts "pr" option; do
   case $option in
      r) # run container
         RUN=true
         ;;
      p) # set privileged flag
         PRIV=true
         ;;
   esac
done

if [ $RUN = true ] ; then
    if [ $PRIV = true ] ; then
        echo "RUN PRIV"
        docker run -d --privileged -p $HOST_PORT:$PORT --rm --name=$NAME $NAME
    else
        echo "RUN"
        docker run -d -p $HOST_PORT:$PORT --rm --name=$NAME $NAME
    fi
else
    echo "NO RUN"
fi