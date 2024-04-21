import etcd3
import argparse
import streamlit as st

def get_all(etcd_client):
    all_list = list(etcd_client.get_all())
    keys = [metadata.key.decode('utf-8') for value,metadata in all_list]
    values = [value.decode('utf-8') for value,metadata in all_list]
    return {'key':keys,'value':values}

def get_value(etcd_client,key):
    value,metadata = etcd_client.get(key)
    if metadata==None:
        return None
    return {'key':[metadata.key.decode('utf-8')],'value':[value.decode('utf-8')]}

def put_kv(etcd_client,key,value):
    return etcd_client.put(key,value)

def delete_kv(etcd_client,key):
    return etcd_client.delete(key)


parser = argparse.ArgumentParser(description="ETCD Key Value Store Client")
parser.add_argument("--client-port", type=int, help="Port for etcd client")
args = parser.parse_args()

if __name__ == "__main__":
    if args.client_port:
        client_port = args.client_port
    else:
        print("Error: Please provide a client port using --client-port argument")
        exit()

    st.title("ETCD - Key Value Store Client")

    try:
        etcd_client = etcd3.client(host='localhost',port=8080)
        st.header("Members:")
        members = list(etcd_client.members)
        col_list = st.columns(len(members))
        for i in range(len(members)):
            with col_list[i]:
                st.write(f"Member: {members[i].name}")
                st.write(f"ID: {members[i].id}")
                st.write(f"Peer URLs: {members[i].peer_urls}")
                st.write(f"Client URLs: {members[i].client_urls}")
        st.divider()

        col1,col2 = st.columns(2)

        option_list = ("Get all keys in store","Get value for a key","Put a key value pair","Delete a key value pair")

        with col1:
            option = st.selectbox("What would you like to do?",
            option_list,
            index=None,
            placeholder="Select an operation",
            key="option"
            )
            if option == option_list[1] or st.session_state.option==option_list[3]:
                st.text_input("Enter the key:",key="key")
                st.button("Enter",type="primary",key="submit")
            if option == option_list[2]:
                st.text_input("Enter the key:",key="key")
                st.text_input("Enter the value:",key="value")
                st.button("Enter",type="primary",key="submit")


        with col2:
            st.subheader("Result:")
            if st.session_state.option==option_list[0]:
                kv_dict = get_all(etcd_client)
                st.table(kv_dict)
            if st.session_state.option==option_list[1]:
                if st.session_state.key and st.session_state.submit:
                    result = get_value(etcd_client,st.session_state.key)
                    if result: 
                        st.table(result)
                    else:
                        st.error("Error: Key does not exist")
            if st.session_state.option==option_list[2]:
                if st.session_state.submit:
                    if not st.session_state.key:
                        st.error("Error: Enter Key")
                    elif not st.session_state.value:
                        st.error("Error: Enter Value")
                    else:
                        put_kv(etcd_client,st.session_state.key,st.session_state.value)
                        st.success("Key entered successfully")
            if st.session_state.option==option_list[3]:
                if st.session_state.submit:
                    if not st.session_state.key:
                        st.error("Error: Enter Key")
                    elif delete_kv(etcd_client,st.session_state.key):
                        st.success("Key deleted succesfully")
                    else:
                        st.error("Error: Key does not exist")

    except:
        st.error("Error: Server Not Found")