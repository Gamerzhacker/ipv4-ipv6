# Dockerfile
FROM ubuntu:22.04

RUN apt update && \
    apt install -y openssh-server sudo && \
    mkdir /var/run/sshd

RUN useradd -m vpsuser && echo 'vpsuser:password' | chpasswd && \
    echo 'vpsuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

EXPOSE 22 443 80 8080 2022 5080 3001

CMD ["/usr/sbin/sshd", "-D"]
