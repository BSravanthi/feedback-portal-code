
# -*- coding: utf-8 -*-
from runtime.objects.entities import *
from runtime.config.config import Config
from runtime.exceptions.custom_exceptions import *
import datetime
class ObjectDelegate():
    def __init__(self):
        self.role_set = []
        self.user_set = []
        self.active_user_set = []
        self.institute_set = []
        self.oc_set = []
        self.nc_set = []
        self.workshop_set = []
        self.artefact_set = []
        self.role_set = self.initialize_role_set()
        self.user_set = self.initialize_user_set()

    def initialize_role_set(self):
        Role_admin = Role(name="admin", centre_oc=None, centre_nc=None)
        Role_guest = Role(name="guest", centre_oc=None, centre_nc=None)
        Role_noc = Role(name="noc", centre_oc=None, centre_nc=None)
        Role_reviewer = Role(name="reviewer", centre_oc=None, centre_nc=None)                
        self.role_set = [Role.admin, Role.guest, Role.noc, Role.reviewer]
        return self.role_set


    def initialize_user_set(self):

        admin_user = User(name=Name(name=Config.admin_name),
                          email=Email(email=Config.admin_email),
                          roles=[Role.admin, Role.guest], user_status="active")
        self.user_set = [admin_user]
        return self.user_set

    def user_exists(self, user):
        active_users = self.get_active_users()
        if user in active_users:
            return True
        else:
            return False

    def add_user(self, user):
        self.user_set.append(user)
        return user

    def update_user(self, name, email, user):
        user.set(name=name)
        user.set(email=email)
        return user

    def delete_user(self, user):
        user.set(user_status="inactive")
        return user
    def add_role_to_user(self, user, role):
        user.append_role(role)
        return user
    def get_users(self):
        return self.get_active_users()

    def role_exists(self, role):
        if role in self.role_set:
            return True
        else:
            return False

    def add_role(self, role):
        self.role_set.append(role)
        return role

    def get_roles(self):
        return self.role_set

    def institute_exists(self, institute):
        if institute in self.institute_set:
            return True
        else:
            return False

    def add_institute(self, institute):
        self.institute_set.append(institute)
        return institute

    def update_institute(self, institute, name, address):
        institute.set(name=name)
        institute.set(address=address)
        return institute
    def get_institutes(self):
        return self.institute_set

    def oc_exists(self, oc):
        if oc in self.oc_set:
            return True
        else:
            return False

    def add_occ_role(self, name, new_oc, centre_nc):
        self.role = Role(name=name,centre_oc=new_oc,centre_nc=centre_nc)
        self.role_set.append(self.role)
        return self.role
    def add_ncc_role(self, name, centre_oc, new_nc):
        self.role = Role(name=name,centre_oc=centre_oc,centre_nc=new_nc)
        self.role_set.append(self.role)
        return self.role
    def add_oc(self, institute, spokes, oc_target):
        self.new_oc = OC(institute=institute, spokes=spokes, oc_target = oc_target)
        self.oc_set.append(self.new_oc)
        return self.new_oc
    def get_ocs(self):
        return self.oc_set

    def nc_exists(self, nc):
        if nc in self.nc_set:
            return True
        else:
            return False

    def add_nc(self, institute, oc, nc_target, workshops):
        self.new_nc = NC(institute=institute, hub=oc, nc_target=nc_target,
                         workshops=workshops)
        oc.append_spoke(self.new_nc)
        self.nc_set.append(self.new_nc)
        return self.new_nc
    def get_ncs(self):
        return self.nc_set

    def workshop_exists(self, workshop):
        if workshop in self.workshop_set:
            return True
        else:
            return False

    def add_workshop(self, institute, name, ws_target, artefacts, status, nc):
        new_workshop = Workshop(institute = institute,
                                name = name,
                                ws_target = ws_target,
                                artefacts = artefacts,
                                status = status,
                                nc = nc,
                                a_date = None,
                                a_participants = 0,
                                a_experiments = 0,
                                a_usage = 0)
        self.workshop_set.append(new_workshop)
        return new_workshop

    def cancel_workshop(self, workshop):
        workshop.set(status = Status.cancelled)
        return workshop
    def reschedule_workshop(self, workshop, wstarget):
        workshop.set(status = Status.pending)
        workshop.set(ws_target = wstarget)
        return workshop

    def conduct_workshop(self, workshop):
        workshop.set(status = Status.completed)
        return workshop
    def upload_artefact(self, workshop, new_artefact):
        artefacts = workshop.get("artefacts")
        artefacts.append(new_artefact)
        workshop.set(artefacts = artefacts)
        workshop.set(status = Status.pending_approval)
        return workshop
    def approve_workshop(self, workshop):
        workshop.set(status = Status.approved)
        return workshop
    def reject_workshop(self, workshop):
        workshop.set(status = Status.rejected)
        return workshop
    def delete_artefact(self, workshop, artefact):
        artefact_set = workshop.get("artefacts")
        new_set = filter(lambda art: not art.get("name") ==
                         artefact.get("name"), artefact_set)

        workshop.set(artefacts = new_set)
        workshop.set(status = Status.pending_approval)
        return workshop
    def get_artefacts_of_a_workshop(self, workshop):
        self.artefact_set = workshop.get("artefacts")
        return self.artefact_set     
    def get_artefacts(self):
        return self.artefact_set

    def get_workshops(self):
        return self.workshop_set

    def get_active_users(self): 
        active_user_set = filter(lambda x: x.get("user_status")=="active",
                                self.user_set)
        return active_user_set
