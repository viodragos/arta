FROM odoo:18
USER root
RUN pip install --break-system-packages qifparse
USER odoo