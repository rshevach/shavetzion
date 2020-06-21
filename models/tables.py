# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

db.define_table( "fellow", Field('name', label='שם פרטי + ומשפחה'), format='%(name)s')
db.define_table( "parashot", Field('name', label='פרשה'), Field('parash', 'datetime',label='זמן'), Field('image', 'upload'), format='%(name)s')
db.define_table( "tfila", Field('name', label='תפילה'), format='%(name)s')
db.define_table( "person", Field('name'))

db.define_table( "neder",
                Field('name', 'reference fellow', label='שם'),
                Field('tefila', 'reference tfila', label='תפילה'),
                Field('parasha', 'reference parashot', label='פרשה'),
                Field('debit', 'integer', label='חוב'),
                Field('credit', 'integer', label='זכות'),
                Field('comment', label='הערה'),
                auth.signature
               )
db.neder._singular ='נדר'
db.neder._plural='נדרים'
