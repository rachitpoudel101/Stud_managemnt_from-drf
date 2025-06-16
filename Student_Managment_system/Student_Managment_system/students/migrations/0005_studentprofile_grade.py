# Generated manually

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_subject_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='grade',
            field=models.CharField(choices=[('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3'), ('4', 'Grade 4'), ('5', 'Grade 5'), ('6', 'Grade 6'), ('7', 'Grade 7'), ('8', 'Grade 8'), ('9', 'Grade 9'), ('10', 'Grade 10'), ('11', 'Grade 11'), ('12', 'Grade 12')], default='1', max_length=2),
        ),
    ]
