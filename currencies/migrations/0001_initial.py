# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Currency'
        db.create_table('currencies', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('factor', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=4)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('currencies', ['Currency'])

        # Adding model 'CountryCurrency'
        db.create_table('currencies_countrycurrency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['countries.Country'], unique=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['currencies.Currency'])),
        ))
        db.send_create_signal('currencies', ['CountryCurrency'])


    def backwards(self, orm):
        
        # Deleting model 'Currency'
        db.delete_table('currencies')

        # Deleting model 'CountryCurrency'
        db.delete_table('currencies_countrycurrency')


    models = {
        'countries.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country', 'db_table': "'countries'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'})
        },
        'currencies.countrycurrency': {
            'Meta': {'ordering': "('country',)", 'object_name': 'CountryCurrency'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Country']", 'unique': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['currencies.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'currencies.currency': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Currency', 'db_table': "'currencies'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'factor': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '4'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['currencies']
