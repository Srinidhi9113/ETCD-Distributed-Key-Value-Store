#! /usr/bin/bash

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <number_of_nodes> <peer_ip_ports> <client_ip_ports>"
    exit 1
fi

NUM_NODES=$1
PEER_IP_PORTS=($2)
CLIENT_IP_PORTS=($3)
DATA_DIR="$PWD/data"

if [ "${#PEER_IP_PORTS[@]}" -ne "$NUM_NODES" ] || [ "${#CLIENT_IP_PORTS[@]}" -ne "$NUM_NODES" ]; then
    echo "Number of peer and client IP ports should match the number of nodes."
    exit 1
fi

mkdir -p "$DATA_DIR"

tmux new-session -d -s etcd_session

NUM_PANES=$((NUM_NODES - 1))

for ((i=0; i<NUM_PANES; i++)); do
    tmux split-window -h -l $((100/NUM_NODES))%
done

INITIAL_CLUSTER=""
STATUS_INFO=""
for ((j=0; j<NUM_NODES; j++)); do
    INITIAL_CLUSTER+="node$j=http://localhost:${PEER_IP_PORTS[$j]},"
    STATUS_INFO+="localhost:${CLIENT_IP_PORTS[$j]},"
done
INITIAL_CLUSTER=${INITIAL_CLUSTER%,}
STATUS_INFO=${STATUS_INFO%,}

for ((i=0; i<NUM_NODES; i++)); do
    tmux select-pane -t etcd_session:0.$i

    NODE_PEER_PORT=${PEER_IP_PORTS[$i]}
    NODE_CLIENT_PORT=${CLIENT_IP_PORTS[$i]}

    tmux send-keys "etcd --name node$i --initial-advertise-peer-urls http://localhost:$NODE_PEER_PORT \
                    --listen-peer-urls http://localhost:$NODE_PEER_PORT \
                    --advertise-client-urls http://localhost:$NODE_CLIENT_PORT \
                    --listen-client-urls http://localhost:$NODE_CLIENT_PORT \
                    --initial-cluster $INITIAL_CLUSTER \
                    --initial-cluster-token etcd-cluster \
                    --initial-cluster-state new \
                    --data-dir $DATA_DIR/node$i" C-m
done

tmux attach-session -t etcd_session

tmux detach -s etcd_session

etcdctl -w table --endpoints=$STATUS_INFO endpoint status
