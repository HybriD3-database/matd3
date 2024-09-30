# Generated by Django 3.1.14 on 2024-09-30 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0132_auto_20240930_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='System_Stoichiometry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stoichiometry', models.CharField(default='N/A', help_text='Please provide the stoichiometry value in the format: C:6,H:12,O:1', max_length=255)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.system')),
            ],
        ),
        migrations.CreateModel(
            name='Stoichiometry_Elements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.CharField(max_length=1000)),
                ('string_value', models.CharField(default='0', max_length=1000)),
                ('float_value', models.FloatField(default=0.0)),
                ('system_stoichiometry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.system_stoichiometry')),
            ],
        ),
    ]
