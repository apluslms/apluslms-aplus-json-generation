FROM apluslms/service-base:python3-1.5

ARG BRANCH=milestone0.3

RUN :\
    && mkdir /srv/roman \
    && cd /srv/roman \
    # get yaml_validator.whl
#    && git clone --quiet --single-branch --branch $BRANCH https://github.com/QianqianQ/roman.git .\
    && git clone https://github.com/apluslms/roman.git .\
    && git checkout $BRANCH \
    && rm -rf .git \
    && pip3 install -r requirements_build.txt \
    &&  ./scripts/build_wheels.sh \
    &&  pip3 install `find dist -name "apluslms_yamlidator-*.whl"` \
    && mkdir -p /srv/update_yaml/schemas \
    && mkdir -p /srv/update_yaml/index_instance

COPY validate.py /srv/update_yaml
COPY index_instance/index.yaml /srv/update_yaml/index_instancew
