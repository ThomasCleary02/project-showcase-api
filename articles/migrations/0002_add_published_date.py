
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='img_url',
            field=models.URLField(blank=True),
        ),
    ]