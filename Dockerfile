FROM jupyter/scipy-notebook

MAINTAINER Ben Evans <b.d.evans@gmail.com>

USER $NB_USER

RUN conda config --add channels brian-team
# RUN conda config --add channels menpo
# 'mayavi=4.5.*'

# Install Python 3 packages
RUN conda install --quiet --yes \
    'brian2=2.0.*' \
    'brian2tools=0.2.*' && \
    conda clean -tipsy

# Install Python 2 packages
RUN conda install --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 \
    'brian2=2.0.*' \
    'brian2tools=0.2.*' \
    'mayavi=4.5.*' && \
    conda clean -tipsy

ENV DISPLAY :0
