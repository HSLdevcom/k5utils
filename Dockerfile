# k5utils
FROM alpine:latest

LABEL maintainer="dev@starck.fi"

RUN set -x \
  && apk add --no-cache --update bash build-base curl git jq libffi-dev \
         linux-headers openssl-dev py-pip python-dev \
  && pip install git+https://github.com/openstack/python-openstackclient.git

RUN set -x \
  && pip install git+https://github.com/openstack/python-heatclient.git \
  && pip install git+https://github.com/openstack/python-novaclient.git \
  && pip install git+https://github.com/openstack/python-swiftclient.git

COPY bashrc /root/.bashrc
COPY inputrc /etc/inputrc
COPY utils/ /usr/local/bin/
COPY unannoy.patch /tmp/unannoy.patch

RUN set -x \
  && patch /usr/lib/python2.7/site-packages/keystoneauth1/identity/generic/base.py /tmp/unannoy.patch \
  && chmod -c 755 /usr/local/bin/k5-*

CMD ["/bin/bash"]
