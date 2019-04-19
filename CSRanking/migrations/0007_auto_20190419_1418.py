# Generated by Django 2.1.7 on 2019-04-19 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CSRanking', '0006_auto_20190419_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conference_area',
            options={'ordering': ['area', 'conf_id'], 'verbose_name': '会议-领域信息', 'verbose_name_plural': '会议-领域信息'},
        ),
        migrations.AlterModelOptions(
            name='scholar_area',
            options={'ordering': ['area', 'scholar_name'], 'verbose_name': '作者-领域信息', 'verbose_name_plural': '作者-领域信息'},
        ),
        migrations.AlterModelOptions(
            name='scholar_paper',
            options={'ordering': ['paper_title', 'scholar_name'], 'verbose_name': '作者-论文信息', 'verbose_name_plural': '作者-论文信息'},
        ),
    ]
