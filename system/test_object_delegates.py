
## -*- coding: utf-8 -*-
#import unittest
#from unittest import TestCase
#from object_delegates import *
#import datetime
#class TestObjectDelegate(TestCase):
#    TESTING = True
#    object_delegate = None
#    
#    def setUp(self):
#        self.obj_delegate = ObjectDelegate()
#    
#    def tearDown(self):
#        self.obj_delegate = None
#   
#    def test_initialize_object_delegate(self):
#         print "test_initialize_object_delegate"
#         self.assertEqual(len(self.obj_delegate.role_set), 4)
#         self.assertEqual(self.obj_delegate.role_set[0].get("name"), "admin")
#         self.assertEqual(len(self.obj_delegate.user_set), 1)
#         self.assertEqual(self.obj_delegate.user_set[0].get("roles")[0].get("name"),
#                          "admin")
#         self.assertEqual(self.obj_delegate.user_set[0].get("roles")[1].get("name"),
#                          "guest")
#
#    def test_user_exists(self):
#         print "test_user_exists"
#         user = self.obj_delegate.user_set[0]
#         self.assertEqual(self.obj_delegate.user_exists(user), True)
#
#    def test_add_user(self):
#        print "test_add_user"
#        user = User(name=Name(name="some user"),
#                        email=Email(email="tt@kk.com"),
#                        roles=[Role.admin], user_status="active")
#        user = self.obj_delegate.add_user(user)
#        self.assertEqual(self.obj_delegate.user_exists(user), True)
#
#
#    def test_update_user(self):
#        print "test_update_user"
#        name=Name(name="test")
#        email=Email(email="test@gmail.com")
#        user = User(name=name, email=email, roles= [Role.guest],
#                user_status="active")
#        user = self.obj_delegate.add_user(user)
#        user_name1=Name(name="alaska")
#        user_email1=Email(email="alaska@gmail.com")
#        user = self.obj_delegate.update_user(user_name1, user_email1, user)
#        self.assertEqual(user.get("name").get("name"), "alaska")
#        
#    def test_delete_user(self):
#        print "test_delete_user"
#        name = Name(name="test")
#        email = Email(email="test@gmail.com")
#        user = User(name=name, email=email, roles= [Role.guest],
#                user_status="active")
#        new_user = self.obj_delegate.add_user(user)
#        del_user = self.obj_delegate.delete_user(new_user)
#        self.assertEqual(del_user.get("user_status") , "inactive")
#    def test_get_users(self):
#         print "test_get_users"
#         self.assertEqual(len(self.obj_delegate.get_users()), 1)
#
#    def test_role_exists(self):
#         print "test_role_exists"
#         role = self.obj_delegate.role_set[0]
#         self.assertEqual(self.obj_delegate.role_exists(role), True)
#
#    def test_add_role_to_user(self):
#        print "test_add_role_to_user"
#        name = Name(name="test")
#        email = Email(email="test@gmail.com")
#        user = User(name=name, email=email, roles= [Role.guest],
#                user_status="active")
#        new_user = self.obj_delegate.add_user(user)
#        user_with_new_role = self.obj_delegate.add_role_to_user(new_user, Role.noc)
#        self.assertTrue(len(user_with_new_role.get('roles'))==2)
#    def test_add_role(self):
#         print "test_add_role"
#         role = Role(name='user',centre_oc=None,centre_nc=None)
#         role = self.obj_delegate.add_role(role)
#         self.assertEqual(self.obj_delegate.role_exists(role), True)
#
#    def test_get_roles(self):
#         print "test_get_roles"
#         self.assertEqual(len(self.obj_delegate.get_roles()), 4)
#
#    def test_institute_exists(self):
#         print "test_institute_exists"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         inst = self.obj_delegate.add_institute(ins)
#         self.assertEqual(self.obj_delegate.institute_exists(inst), True)
#
#    def test_add_institute(self):
#         print "test_add_institute"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         inst = self.obj_delegate.add_institute(ins)
#         self.assertEqual(self.obj_delegate.institute_exists(inst), True)
#
#    def test_get_institutes(self):
#         print "test_get_institutes"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         inst = self.obj_delegate.add_institute(ins)
#         self.assertEqual(len(self.obj_delegate.get_institutes()), 1)
#
#    def test_oc_exists(self):
#         print "test_oc_exists"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         spokes=[]
#         oc_target = None
#         oc = self.obj_delegate.add_oc(ins, spokes, oc_target)
#         self.assertEqual(self.obj_delegate.oc_exists(oc), True)
#    def test_add_occ_role(self):
#         print "test_add_occ_role"
#         role = self.obj_delegate.add_occ_role('OCC',None,None)
#         self.assertEqual(self.obj_delegate.role_exists(role), True)
#
#    def test_add_ncc_role(self):
#         print "test_ncc_occ_role"
#         role = self.obj_delegate.add_occ_role('NCC',None,None)
#         self.assertEqual(self.obj_delegate.role_exists(role), True)
#
#    def test_add_oc(self):
#         print "test_object_add_oc"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         spokes=[]
#         oc_target = None
#         oc = self.obj_delegate.add_oc(ins, spokes, oc_target)
#         self.assertEqual(self.obj_delegate.oc_exists(oc), True)
#
#    def test_get_ocs(self):
#         print "test_get_ocs"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         spokes=[]
#         oc_target = None
#         oc = self.obj_delegate.add_oc(ins, spokes, oc_target)
#
#         self.assertEqual(len(self.obj_delegate.get_ocs()), 1)
#
#    def test_nc_exists(self):
#         print "test_object_nc_exists"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         spokes=[]
#         oc_target = None
#         oc = self.obj_delegate.add_oc(ins, spokes, oc_target)
#         nc_target=None
#         workshops=[]
#         nc = self.obj_delegate.add_nc(ins, oc, nc_target, workshops)
#         self.assertEqual(self.obj_delegate.nc_exists(nc), True)
#
#    def test_add_nc(self):
#         print "test_object_add_nc"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         spokes=[]
#         oc_target = None
#         oc = self.obj_delegate.add_oc(ins, spokes, oc_target)
#         nc_target=None
#         workshops=[]
#         nc = self.obj_delegate.add_nc(ins, oc, nc_target, workshops)
#         self.assertEqual(self.obj_delegate.nc_exists(nc), True)
#    def test_get_ncs(self):
#         print "test_get_ncs"
#         ins = Institute(name='IIIT',address='Hyderabad')
#         spokes=[]
#         oc_target = None
#         oc = self.obj_delegate.add_oc(ins, spokes, oc_target)
#         nc_target=None
#         workshops=[]
#         nc = self.obj_delegate.add_nc(ins, oc, nc_target, workshops)
#         self.assertEqual(len(self.obj_delegate.get_ncs()), 1)
#    def test_get_active_users(self):
#         print "test_get_active_users"
#         user = User(name=Name(name="some user"),
#                          email=Email(email="tt@kk.com"),
#                          roles=[Role.admin], user_status="active")
#
#         self.obj_delegate.add_user(user)
#         active_user_list = self.obj_delegate.get_active_users()
#         self.assertEqual(len(active_user_list), 2)
#
#    def test_workshop_exists(self):
#        print "test_workshop_exists"
#        ins = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        workshop_name = Name(name = "New Workshop")
#        ws_status = Status(name = "pending")
#        artefacts = []
#        workshop = self.obj_delegate.add_workshop(ins, workshop_name, ws_target, artefacts, ws_status, nc)
#        self.assertEqual(self.obj_delegate.workshop_exists(workshop), True)
#
#    def test_add_workshop(self):
#        print "test_add_workshop"
#        ins = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        workshop_name = Name(name = "New Workshop")
#        ws_status = Status(name = "pending")
#        artefacts = []
#        workshop = self.obj_delegate.add_workshop(ins, workshop_name, ws_target, artefacts, ws_status, nc)
#        self.assertEqual(self.obj_delegate.workshop_exists(workshop), True)
#
#    def test_get_all_workshops(self):
#        print "test_get_all_workshops"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#        self.assertEqual(self.obj_delegate.workshop_exists(workshop), True)
#        self.assertEqual(len(self.obj_delegate.get_workshops()), 1)
#    def test_cancel_workshop(self):
#        print "test_cancel_workshop"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#
#        cancelled_workshop = self.obj_delegate.cancel_workshop(workshop)
#
#        self.assertEqual(cancelled_workshop.get("status"), Status.cancelled)
#    def test_get_all_workshops(self):
#        print "test_get_all_workshops"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#        self.assertEqual(self.obj_delegate.workshop_exists(workshop), True)
#        self.assertEqual(len(self.obj_delegate.get_workshops()), 1)
#    def test_reschedule_workshop(self):
#        print "test_reschedule_workshop"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#        ws_new_target = WSTarget(usage = 5000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        rescheduled_workshop = self.obj_delegate.reschedule_workshop(workshop, ws_new_target)
#
#        self.assertEqual(rescheduled_workshop.get("status"), Status.pending)
#        self.assertEqual(rescheduled_workshop.get("ws_target").get("usage"), 5000)
#    def test_conduct_workshop(self):
#        print "test_conduct_workshop"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#
#        conducted_workshop = self.obj_delegate.conduct_workshop(workshop)
#
#        self.assertEqual(conducted_workshop.get("status"), Status.completed)
#    def test_upload_artefact(self):
#        print "test_upload_artefact"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#        new_artefact = Artefact(name = "Photo", path = "/main/photos",
#                                a_type = Type.photo)
#
#        workshop = self.obj_delegate.upload_artefact(workshop, new_artefact)
#
#        self.assertEqual(workshop.get("status"), Status.pending_approval)
#        self.assertEqual(len(self.obj_delegate.get_artefacts_of_a_workshop(workshop)), 1)
#        self.assertEqual(len(self.obj_delegate.get_artefacts()), 1)
#
#    def test_get_artefacts(self):
#        new_artefact = Artefact(name = "Photo", path = "/main/photos",
#                                a_type = Type.photo)
#        self.obj_delegate.artefact_set.append(new_artefact)
#        self.assertEqual(len(self.obj_delegate.get_artefacts()), 1)
#
#    def test_approve_workshop(self):
#        print "test_approve_workshop"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#
#        approved_workshop = self.obj_delegate.approve_workshop(workshop)
#
#        self.assertEqual(approved_workshop.get("status"), Status.approved)
#    def test_reject_workshop(self):
#        print "test_reject_workshop"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#
#        rejected_workshop = self.obj_delegate.reject_workshop(workshop)
#
#        self.assertEqual(rejected_workshop.get("status"), Status.rejected)
#    def test_delete_artefact(self):
#        print "test_delete_artefact"
#        institute = Institute(name='IIIT',address='Hyderabad')
#        oc = OC(institute=Institute(name="IIITH",address="Hyderabad"), spokes=[], oc_target = None)
#        nc = NC(institute=Institute(name="IIITH",address="Hyderabad"), hub=oc, nc_target = None, workshops=None)
#        target_date = datetime.datetime.strptime("30-06-2016", '%d-%m-%Y').date()
#        oc_target = OCTarget(usage = 400, date = target_date, nctargets = [])
#        nc_target = NCTarget(usage = 200, date = target_date, oc_target = oc_target, wstargets = [])
#        ws_target = WSTarget(usage = 4000, participants = 200, experiments = 20, date = target_date, nc_target = nc_target )
#        name = Name(name = "New Workshop")
#        status = Status(name = "pending")
#        artefacts = []
#
#        workshop = self.obj_delegate.add_workshop(institute, name, ws_target, artefacts, status, nc)
#        new_artefact = Artefact(name = "Photo", path = "/main/photos",
#                                a_type = Type.photo)
#
#        artefact_upload_workshop = self.obj_delegate.upload_artefact(workshop, new_artefact)
#        artefact_delete_workshop = self.obj_delegate.delete_artefact(workshop, new_artefact)
#
#        self.assertEqual(artefact_delete_workshop.get("status"), Status.pending_approval)
#        self.assertEqual(len(self.obj_delegate.get_artefacts_of_a_workshop(artefact_delete_workshop)), 0)
#
#if __name__ == '__main__':
#    unittest.main()
#
