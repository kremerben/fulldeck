# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Card'
        db.create_table(u'cards_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('suit', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'cards', ['Card'])


    def backwards(self, orm):
        # Deleting model 'Card'
        db.delete_table(u'cards_card')


    models = {
        u'cards.card': {
            'Meta': {'object_name': 'Card'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'suit': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['cards']