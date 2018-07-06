# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = db.tables()
    return dict(message=T('Welcome to web2py!!!'), name="יוסי")

def show():
    form = SQLFORM.smartgrid( db.neder, linked_tables=['fellow','parashot','tfila'])
    return locals()

def show_parashot():
    form = SQLFORM.smartgrid( db.parashot) #, fields = [db.parashot.name, db.parashot.parash, db.parashot.image])
    return locals()

def show_fellow():
    rows = db(db.fellow).select(orderby=db.fellow.name)
    form = None #SQLFORM.smartgrid( db.fellow)
    return locals()

def edit_fellow():
    form = SQLFORM.smartgrid(db.fellow)
    return locals()

def mitpalel():
    form = SQLFORM.factory(db.fellow)
    return locals()

def validCast(num):
    try:
        n = float(num)
        return n
    except ValueError:
        return 0

def bill():
    query=db.neder.name == request.vars.mitpalel
    form = SQLFORM.smartgrid( db.neder, linked_tables=['fellow','parashot','tfila'], constraints = dict(neder=query),
                              orderby=db.neder.parasha)
    #form = len(db(db.neder.name == request.vars.mitpalel).select())
    #form = 10 #len(db(db.neder).select())
    rows = db((db.neder.name == request.vars.mitpalel)).select().sort(lambda row: db.parashot[row.parasha].parash)
    deb = (validCast(line.debit) for line in rows)
    cre = (validCast(line.credit) for line in rows)
    txt = '<table dir="rtl">\n'
    txt = txt + "<tr>"
    txt = txt + "<th>תאריך</th>"
    txt = txt + "<th>פרשה</th>"
    txt = txt + "<th>תפילה</th>"
    txt = txt + "<th>חובה</th>"
    txt = txt + "<th>זכות</th>"
    txt = txt + "<th>יתרה</th>"
    txt = txt + "</tr>"
    itra = 0
    for row in rows:
        p = db.parashot[row.parasha]
        t = db.tfila[row.tefila]
        itra = itra - validCast(row.debit) + validCast(row.credit)
        txt = txt + "<tr>"
        txt = txt + "<td dir='ltr'>" + str(p.parash.strftime("%d-%m-%y")) + "</td>"
        txt = txt + "<td>" + str(p.name) + "</td>"
        txt = txt + "<td>" + str(t.name) + "</td>"
        txt = txt + "<td>" + row.debit + "</td>"
        txt = txt + "<td>" + row.credit + "</td>"
        txt = txt + "<td dir='ltr'>" + str(int(itra)) + "</td>"
        txt = txt + "</tr>"
    txt = txt + "</table>"
    txt = txt + "<p>"
    summation = sum(cre)-sum(deb)
    if summation == int(summation):
        txt = txt + "<h3>"+str(int(summation))+" :יתרה</h3>"
    else:
        txt = txt +  "<h3>"+str(summation)+" :יתרה</h3>"
    return txt

def fellow_bill(f_id):
    rows = db((db.neder.name == f_id)).select()
    deb = (validCast(line.debit) for line in rows)
    cre = (validCast(line.credit) for line in rows)
    summation = sum(cre)-sum(deb)
    if summation == int(summation):
        return str(int(summation))
    return str(summation)

def daf_sicum():
    rows = db(db.fellow).select(orderby=db.fellow.name)
    s = []
    for row in rows:
        s.append([row.name,fellow_bill(row.id)])
    dd = []
    l = len(s)/2
    for i in range(l):
        dd.append(s[i]+s[l+i])
    if len(s)%2 == 1:
        dd.append(s[len(s)/2] + [" "," "])
    parashot_rows = db(db.parashot).select(orderby=db.parashot.parash)
    last_parasha = parashot_rows[len(parashot_rows)-1].name
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
