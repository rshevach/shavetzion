# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def listing():
    response.title = "web2py sample listing"

    # define header and footers:
    head = THEAD(TR(TH("Header 1", _width="50%"), 
                    TH("Header 2", _width="30%"),
                    TH("Header 3", _width="20%"), 
                    _bgcolor="#A0A0A0"))
    foot = TFOOT(TR(TH("Footer 1", _width="50%"), 
                    TH("Footer 2", _width="30%"),
                    TH("Footer 3", _width="20%"),
                    _bgcolor="#E0E0E0"))

    # create several rows:
    rows = []
    for i in range(1000):
        col = i % 2 and "#F0F0F0" or "#FFFFFF"
        rows.append(TR(TD("Row %s" %i),
                       TD("something", _align="center"),
                       TD("%s" % i, _align="right"),
                       _bgcolor=col)) 

    # make the table object
    body = TBODY(*rows)
    table = TABLE(*[head, foot, body], 
                  _border="1", _align="center", _width="100%")

    if request.extension == "pdf":
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin

        # define our FPDF class (move to modules if it is reused frequently)
        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, response.title, 1, 0, 'C')
                self.ln(20)

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0, 10, txt, 0, 0, 'C')

        pdf = MyFPDF()
        # first page:
        pdf.add_page()
        pdf.write_html(str(XML(table, sanitize=False)))
        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')
    else:
        # normal html view:
        return dict(table=table)


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

def show_tfila():
    form = SQLFORM.smartgrid( db.tfila,
                              editable  = auth.has_membership('managers'),
                              deletable = auth.has_membership('managers')
                            )
    return locals()


def show_parashot():
    db.parashot.id.readable = False
    db.neder.id.readable = False
    form = SQLFORM.smartgrid( db.parashot,
                              editable  = auth.has_membership('managers'),
                              deletable = auth.has_membership('managers')
                            ) #, fields = [db.parashot.name, db.parashot.parash, db.parashot.image])
    return locals()

def show_fellow():
    rows = db(db.fellow).select(orderby=db.fellow.name)
    form = None #SQLFORM.smartgrid( db.fellow)
    return locals()

def edit_fellow():
    db.fellow.id.readable = False
    form = SQLFORM.smartgrid(db.fellow,
                             editable = auth.has_membership('managers'),
                             deletable = auth.has_membership('managers'))
    return locals()

def mitpalel():
    form = SQLFORM.factory(db.fellow)
    return locals()

def validCast(num):
    if num is None:
        return 0
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
    txt = txt + "<th>הערה</th>"
    txt = txt + "</tr>"
    itra = 0
    txt_lines = ''
    for row in rows:
        txt_line = ''
        p = db.parashot[row.parasha]
        t = db.tfila[row.tefila]
        itra = itra - validCast(row.debit) + validCast(row.credit)
        txt_line = txt_line + "<tr>"
        txt_line = txt_line + "<td dir='ltr'>" + str(p.parash.strftime("%d-%m-%y")) + "</td>"
        txt_line = txt_line + "<td>" + str(p.name) + "</td>"
        txt_line = txt_line + "<td>" + str(t.name) + "</td>"
        txt_line = txt_line + "<td>" + str(row.debit) + "</td>"
        txt_line = txt_line + "<td>" + str(row.credit) + "</td>"
        txt_line = txt_line + "<td dir='ltr'>" + str(int(itra)) + "</td>"
        if row.comment != None:
            txt_line = txt_line + "<td dir='ltr'>" + row.comment + "</td>"
        else:
            txt_line = txt_line + "<td dir='ltr'></td>"
        txt_line = txt_line + "</tr>"
        txt_lines = txt_line + txt_lines
    txt = txt + txt_lines + "</table>"
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
    all_debt = 0
    rows = db(db.fellow).select(orderby=db.fellow.name)
    s = []
    for row in rows:
        f_bill = fellow_bill(row.id)
        all_debt = all_debt + int(f_bill)
        s.append([row.name,f_bill])
    if len(s)%2 == 1:
        s.append([" "," "])
    dd = []
    l = len(s)/2
    for i in range(l):
        dd.append(s[i]+s[l+i])
    parashot_rows = db(db.parashot).select(orderby=db.parashot.parash)
    last_parasha = parashot_rows[len(parashot_rows)-1].name
    str_all_debt = str(all_debt)
    return locals()

def daf_sicum3():
    all_debt = 0
    rows = db(db.fellow).select(orderby=db.fellow.name)
    s = []
    for row in rows:
        f_bill = fellow_bill(row.id)
        all_debt = all_debt + int(f_bill)
        s.append([row.name,f_bill])
    if len(s)%3 == 1:
        s.append([" "," ", " "])
    if len(s)%3 == 2:
        s.append([" "," ", " "])
    dd = []
    l = len(s)/3
    for i in range(l):
        dd.append(s[i]+s[l+i]+s[2*l+i])
    parashot_rows = db(db.parashot).select(orderby=db.parashot.parash)
    last_parasha = parashot_rows[len(parashot_rows)-1].name
    str_all_debt = str(all_debt)
    return locals()

def daf_sicum4():
    all_debt = 0
    rows = db(db.fellow).select(orderby=db.fellow.name)
    s = []
    for row in rows:
        f_bill = fellow_bill(row.id)
        all_debt = all_debt + int(f_bill)
        s.append([row.name,f_bill])
    if len(s)%4 == 1:
        s.append([" "," ", " ", " "])
    if len(s)%4 == 2:
        s.append([" "," ", " ", " "])
    if len(s)%4 == 3:
        s.append([" "," ", " ", " "])
    dd = []
    l = len(s)/4
    for i in range(l):
        dd.append(s[i]+s[l+i]+s[2*l+i]+s[3*l+i])
    parashot_rows = db(db.parashot).select(orderby=db.parashot.parash)
    last_parasha = parashot_rows[len(parashot_rows)-1].name
    str_all_debt = str(all_debt)
    return locals()

def daf_hadpasa():
    all_debt = 0
    rows = db(db.fellow).select(orderby=db.fellow.name)
    s = []
    for row in rows:
        f_bill = fellow_bill(row.id)
        all_debt = all_debt + int(f_bill)
        s.append([row.name,f_bill])
    if len(s)%4 == 1:
        s.append([" "," ", " ", " "])
    if len(s)%4 == 2:
        s.append([" "," ", " ", " "])
    if len(s)%4 == 3:
        s.append([" "," ", " ", " "])
    dd = []
    l = len(s)/4
    for i in range(l):
        dd.append(s[i]+s[l+i]+s[2*l+i]+s[3*l+i])
    parashot_rows = db(db.parashot).select(orderby=db.parashot.parash)
    last_parasha = parashot_rows[len(parashot_rows)-1].name
    str_all_debt = str(all_debt)

    response.title = last_parasha + " דף סיכום עד פרשת"

    T.force('he-he')
    # define header and footers:
    head = THEAD(TR(TH("שם", _width="50%"),
                    TH("סכום", _width="30%"),
                    TH("הערות", _width="20%"),
                    TH("שם", _width="50%"),
                    TH("סכום", _width="30%"),
                    TH("הערות", _width="20%"),
                    TH("שם", _width="50%"),
                    TH("סכום", _width="30%"),
                    TH("הערות", _width="20%"),
                    TH("שם", _width="50%"),
                    TH("סכום", _width="30%"),
                    TH("הערות", _width="20%"),
                    _bgcolor="#A0A0A0", _dir="rtl"))
    rows = []
    i = 0
    for row in dd:
        col = i % 2 and "#F0F0F0" or "#FFFFFF"
        i=i+1
        rows.append(TR(TD(""),
                       TD(row[7],  _align="center"),
                       TD(row[6], _align="right"),
                       TD(""),
                       TD(row[5],  _align="center"),
                       TD(row[4], _align="right"),
                       TD(""),
                       TD(row[3],  _align="center"),
                       TD(row[2], _align="right"),
                       TD("  "),
                       TD(row[1], _align="center"),
                       TD(row[0], _align="right"),
                       _bgcolor=col, _dir="rtl"))

    # make the table object
    body = TBODY(*rows)
    table = TABLE(*[head, body],
                  _border="1", _align="center", _width="100%")

    if request.extension == "pdf":
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin

        DEFAULT_LANGUAGE = 'he'
        DEFAULT_LANGUAGE_NAME = 'Hebrew'

        # define our FPDF class (move to modules if it is reused frequently)
        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, response.title, 1, 0, 'C')
                self.ln(20)

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0, 10, txt, 0, 0, 'C')

        pdf = MyFPDF()
        # first page:
        pdf.add_page()
        pdf.write_html(str(XML(table, sanitize=False)))
        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')
    else:
        # normal html view:
        return dict(table=table)    

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
