from django.db import migrations, models
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]
    def create_initial_users(apps, schema_editor):
        Users = apps.get_model('pesheysms', 'Users')
    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('email', models.EmailField()),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.RunPython(create_initial_users),
    ]
