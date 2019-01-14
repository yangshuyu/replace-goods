#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from api.app import create_app


application = create_app()


if __name__ == '__main__':
    application.run()
