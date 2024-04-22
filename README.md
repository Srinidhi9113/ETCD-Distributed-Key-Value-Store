# ETCD Distributed Key Value Store

## Introduction
This project aims to create a multi-node ETCD server for a reliable key-value store. It includes a server component and a client program with a GUI interface to interact with the server easily.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/your_username/etcd-project.git
   cd etcd-project
   ```
2. Run the installation script with root permission:
   ```
   sudo ./etcd_install.sh
   ```

## Running the Server
1. Run the server with the following arguments:
   ```
   ./etcd_run.sh <Number_of_nodes> "<List_of_peer_ports>" "<List_of_client_ports>"
   ```
   Example:
   ```
   ./etcd_run.sh 3 "2380 2381 2382" "2379 2383 2384"
   ```

## Running the Client
1. Make sure the server is running.
2. Install the `etcd3` module
   ```
   pip install etcd3
   ```
4. Run the client GUI interface with the following command:
   ```
   streamlit run etcd_client.py -- --client-port <Client_port>
   ```
   Example:
   ```
   streamlit run etcd_client.py -- --client-port 2383
   ```

## Running the Test File
1. Ensure the server is running.
2. Install the `unittest` module
   ```
   pip install unittest
   ```
4. Run the test file with Python:
   ```
   python etcd_test.py
   ```

## Notes
- Ensure all necessary dependencies are installed before running the scripts.
- Modify configuration files as needed for your specific setup.
- Replace `<Number_of_nodes>`, `<List_of_peer_ports>`, and `<List_of_client_ports>` with actual values when running the scripts.
- To navigate into the tmux session, use the command `tmux attach-session -t etcd_session`.
- *Important* : Remove the data directory inside the project folder each time you run the project with different number of nodes.

## References
- [ETCD Release](https://github.com/etcd-io/etcd/releases)
- [ETCD Quickstart Guide](https://etcd.io/docs/v3.5/quickstart/).
- [Python Client Module Documentation](https://python-etcd3.readthedocs.io/en/latest/readme.html)
