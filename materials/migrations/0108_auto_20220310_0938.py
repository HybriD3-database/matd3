# Generated by Django 3.1.12 on 2022-03-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0107_auto_20220308_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='derived_to_from',
            field=models.ManyToManyField(blank=True, related_name='_system_derived_to_from_+', to='materials.System'),
        ),
    ]
