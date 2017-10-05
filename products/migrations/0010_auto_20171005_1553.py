# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_productfeatured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productfeatured',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='productfeatured',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 5, 10, 23, 39, 705000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
