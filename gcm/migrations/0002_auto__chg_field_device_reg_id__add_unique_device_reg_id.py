# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Device.reg_id'
        db.alter_column(u'gcm_device', 'reg_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))
        # Adding unique constraint on 'Device', fields ['reg_id']
        db.create_unique(u'gcm_device', ['reg_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Device', fields ['reg_id']
        db.delete_unique(u'gcm_device', ['reg_id'])


        # Changing field 'Device.reg_id'
        db.alter_column(u'gcm_device', 'reg_id', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        u'gcm.device': {
            'Meta': {'ordering': "['-modified_date']", 'object_name': 'Device'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dev_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reg_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['gcm']