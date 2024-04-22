#! /usr/bin/bash

if ! command -v etcd &> /dev/null; then
    ETCD_VER=v3.5.13
    GOOGLE_URL=https://storage.googleapis.com/etcd
    GITHUB_URL=https://github.com/etcd-io/etcd/releases/download
    DOWNLOAD_URL=${GOOGLE_URL}

    rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
    rm -rf /tmp/etcd-download-test && mkdir -p /tmp/etcd-download-test

    curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
    tar xzvf /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz -C /tmp/etcd-download-test --strip-components=1
    rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz

    /tmp/etcd-download-test/etcd --version
    /tmp/etcd-download-test/etcdctl version
    /tmp/etcd-download-test/etcdutl version

    mv /tmp/etcd-download-test/etcd /usr/local/bin/
    mv /tmp/etcd-download-test/etcdctl /usr/local/bin/
    mv /tmp/etcd-download-test/etcdutl /usr/local/bin/
fi

echo $(etcd --version)
echo $(etcdctl version)
echo $(etcdutl version)
