from turbogears.database import session
from turbogears import controllers, expose, flash, widgets, validate, error_handler, validators, redirect, paginate, url
from turbogears.widgets import AutoCompleteField
from turbogears import identity, redirect
from cherrypy import request, response
from tg_expanding_form_widget.tg_expanding_form_widget import ExpandingForm
from kid import Element
from bkr.server.xmlrpccontroller import RPCRoot
from bkr.server.helpers import *
from bkr.server.widgets import AlphaNavBar, myPaginateDataGrid
from bkr.server.admin_page import AdminPage

import cherrypy

from BasicAuthTransport import BasicAuthTransport
import xmlrpclib

# from bkr.server import json
# import logging
# log = logging.getLogger("bkr.server.controllers")
#import model
from model import *
import string

# Validation Schemas

class OSVersions(AdminPage):
    # For XMLRPC methods in this class.
    exposed = False

    id      = widgets.HiddenField(name="id")
    alias   = widgets.TextField(name="alias")
    arches  = widgets.CheckBoxList(name="arches", label="Arches",
                                      options=[(arch.id, arch.arch) for arch in Arch.query()],
                                      validator=validators.Int())

    osmajor_form = widgets.TableForm(
        fields      = [id, alias],
        action      = "edit osmajor",
        submit_text = _(u"Edit OSMajor"),
    )

    osversion_form = widgets.TableForm(
        fields      = [id, arches],
        action      = "edit osversion",
        submit_text = _(u"Edit OSVersion"),
    )
 
    def __init__(self,*args,**kw):
        kw['search_name'] = 'osversion' 
        kw['search_url'] = url("/osversions/by_name?anywhere=1")
        super(OSVersions,self).__init__(*args,**kw) 

        self.search_col = OSMajor.osmajor
        self.join = ['osmajor']
        self.search_mapper = OSVersion
        self.add = False
     
    @identity.require(identity.in_group("admin"))
    @expose(template="bkr.server.templates.form")
    def edit(self, id=None, *args, **kw):
        try:
            osversion = OSVersion.by_id(id)
        except InvalidRequestError:
            flash(_(u"Invalid OSVersion ID %s" % id))
            redirect(".")
        return dict(title   = "OSVersion",
                    value   = dict(id     = osversion.id,
                                   arches = [arch.id for arch in osversion.arches]),
                    form    = self.osversion_form,
                    action  = "./save",
                    options = None)

    @identity.require(identity.in_group("admin"))
    @expose(template="bkr.server.templates.form")
    def edit_osmajor(self, id=None, *args, **kw):
        try:
            osmajor = OSMajor.by_id(id)
        except InvalidRequestError:
            flash(_(u"Invalid OSMajor ID %s" % id))
            redirect(".")
        return dict(title   = "OSMajor",
                    value   = dict(id     = osmajor.id,
                                   alias  = osmajor.alias),
                    form    = self.osmajor_form,
                    action  = "./save_osmajor",
                    options = None)

    @identity.require(identity.in_group("admin"))
    @expose()
    @validate(form=osversion_form)
    def save_osmajor(self, id=None, alias=None, *args, **kw):
        try:
            osmajor = OSMajor.by_id(id)
        except InvalidRequestError:
            flash(_(u"Invalid OSMajor ID %s" % id))
            redirect(".")
        if osmajor.alias != alias:
            osmajor.alias = alias
            flash(_(u"Changes Saved for %s" % osmajor))
        else:
            flash(_(u"No Changes for %s" % osmajor))
        redirect(".")

    @identity.require(identity.in_group("admin"))
    @expose()
    @validate(form=osversion_form)
    def save(self, id=None, arches=None, *args, **kw):
        try:
            osversion = OSVersion.by_id(id)
        except InvalidRequestError:
            flash(_(u"Invalid OSVersion ID %s" % id))
            redirect(".")
        arch_objects = [Arch.by_id(arch) for arch in arches]
        if osversion.arches != arch_objects:
            osversion.arches = arch_objects
            flash(_(u"Changes Saved for %s" % osversion))
        else:
            flash(_(u"No Changes for %s" % osversion))
        redirect(".")

    
    @expose(format='json')
    def by_name(self, input,*args,**kw):
        input = input.lower()
        if 'anywhere' in kw:
            search = OSVersion.list_osmajor_by_name(input, find_anywhere=True)
        else:
            search = OSVersion.list_osmajor_by_name(input)

        osmajors =  ["%s" % (match.osmajor.osmajor) for match in search] 
        osmajors = list(set(osmajors))
        return dict(matches=osmajors)

    @expose(template="bkr.server.templates.admin_grid")
    @paginate('list',limit=50, default_order='osmajor.osmajor', max_limit=None)
    def index(self,*args,**kw):
        osversions = session.query(OSVersion)
        list_by_letters = []
        for elem in osversions:
            osmajor_name = elem.osmajor.osmajor
            if osmajor_name:
                list_by_letters.append(osmajor_name[0].capitalize())
        list_by_letters = set(list_by_letters)
        results = self.process_search(**kw)
        if results:
            osversions = results
        log.debug(osversions)
        osversions_grid = myPaginateDataGrid(fields=[
                                  myPaginateDataGrid.Column(name='osmajor.osmajor', getter=lambda x: make_link(url = './edit_osmajor?id=%s' % x.osmajor.id, text = x.osmajor), title='OS Major', options=dict(sortable=True)),
                                  myPaginateDataGrid.Column(name='osmajor.alias', getter=lambda x: x.osmajor.alias, title='Alias', options=dict(sortable=True)),
                                  myPaginateDataGrid.Column(name='osminor', getter=lambda x: make_link(url  = './edit?id=%s' % x.id, text = x.osminor), title='OS Minor', options=dict(sortable=True)),
                                  myPaginateDataGrid.Column(name='arches', getter=lambda x: " ".join([arch.arch for arch in x.arches]), title='Arches', options=dict(sortable=True)),
                              ])

        if kw.get('grid'): 
            osversions_grid = kw['grid']
        return dict(title="OS Versions", 
                    grid = osversions_grid, 
                    search_widget = self.search_widget_form,
                    alpha_nav_bar = AlphaNavBar(list_by_letters,self.search_name),
                    object_count = osversions.count(),
                    addable = self.add,
                    list = osversions)

    default = index
