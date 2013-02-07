from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements
from zope.formlib import form
from zope import schema

from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable
from plone.stringinterp.interfaces import IStringInterpolator

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

# import the default messagefactory as _plone. These strings will not be put in
# the locales .po file by i18ndude
from Products.CMFPlone import PloneMessageFactory as _plone
from collective.contentrules.mailtorole import mailtoroleMessageFactory as _


class IMailRoleAction(Interface):
    """Definition of the configuration available for a mail action
    """
    subject = schema.TextLine(
        title=_plone(u"Subject"),
        description=_plone(u"Subject of the message"),
        required=True)
    source = schema.TextLine(
        title=_plone(u"Email source"),
        description=_plone("The email address that sends the \
email. If no email is provided here, it will use the portal from address."),
        required=False)
    role = schema.Choice(
        title=_(u'field_role_title', default=u"Role"),
        description=_(u'field_role_description', default="Select a role. \
The action will look up the all Plone site users who explicitly have this \
role on the object and send a message to their email address."),
        vocabulary="collective.contentrules.mailtorole.roles",
        required=True)
    acquired = schema.Bool(
        title=_(u'field_acquired_title', default=u"Acquired Roles"),
        description=_(u'field_acquired_description',
            default=u"Should users that have this \
role as an acquired role also receive this email?"),
        required=False)
    global_roles = schema.Bool(
        title=_(u'field_global_roles_title', default=u"Global Roles"),
        description=_(u'field_global_roles_description',
            default=u"Should users that have this \
role as a role in the whole site also receive this email?"),
        required=False)
    message = schema.Text(
        title=_plone(u"Message"),
        description=_(u'field_message_description',
            default=u"Type in here the message that you \
want to mail. Some defined content can be replaced: ${title} will be replaced \
by the title of the newly created item. ${url} will be replaced by the \
URL of the newly created item."),
        required=True)


class MailRoleAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(IMailRoleAction, IRuleElementData)

    subject = u''
    source = u''
    role = u''
    message = u''
    acquired = False
    global_roles = False
    element = 'plone.actions.MailRole'

    @property
    def summary(self):
        return _((u"Email report to users with role ${role} on "
                  u"the object"),
                 mapping=dict(role=self.role))

class MailActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IMailRoleAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        mailhost = getToolByName(aq_inner(self.context), "MailHost")

        if not mailhost:
            raise ComponentLookupError(
                'You must have a Mailhost utility to execute this action')

        source = self.element.source
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        membertool = getToolByName(aq_inner(self.context), "portal_membership")

        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        if not source:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                raise ValueError("You must provide a source address for this \
action or enter an email in the portal properties")
            from_name = portal.getProperty('email_from_name').strip('"')
            source = '"%s" <%s>' % (from_name, from_address)

        obj = self.event.object

        interpolator = IStringInterpolator(obj)

        event_title = safe_unicode(obj.Title())
        event_url = obj.absolute_url()

        # search through all local roles on the object, and add
        # users's email to the recipients list if they have the local
        # role stored in the action
        local_roles = obj.get_local_roles()
        if len(local_roles) == 0:
            return True
        recipients = set()
        for user, roles in local_roles:
            rolelist = list(roles)
            if self.element.role in rolelist:
                recipients.add(user)

        # check for the acquired roles
        if self.element.acquired:
            sharing_page = obj.unrestrictedTraverse('@@sharing')
            acquired_roles = sharing_page._inherited_roles()
            acquired_users = [r[0] for r in acquired_roles
                              if self.element.role in r[1]]
            recipients.update(acquired_users)

        # check for the global roles
        if self.element.global_roles:
            pas = getToolByName(self.event.object, 'acl_users')
            rolemanager = pas.portal_role_manager
            global_role_ids = [ p[0] for p in \
                rolemanager.listAssignedPrincipals(self.element.role) ]
            recipients.update(global_role_ids)

        # check to see if the recipents are users or groups
        group_recipients = []
        new_recipients = []
        group_tool = portal.portal_groups

        def _getGroupMemberIds(group):
            """ Helper method to support groups in groups. """
            members = []
            for member_id in group.getGroupMemberIds():
                subgroup = group_tool.getGroupById(member_id)
                if subgroup is not None:
                    members.extend(_getGroupMemberIds(subgroup))
                else:
                    members.append(member_id)
            return members

        for recipient in recipients:
            group = group_tool.getGroupById(recipient)
            if group is not None:
                group_recipients.append(recipient)
                [new_recipients.append(user_id)
                 for user_id in _getGroupMemberIds(group)]

        for recipient in group_recipients:
            recipients.remove(recipient)

        for recipient in new_recipients:
            recipients.add(recipient)

        # look up e-mail addresses for the found users
        recipients_mail = set()
        for user in recipients:
            member = membertool.getMemberById(user)
            # check whether user really exists
            # before getting its email address
            if not member:
                continue
            recipient_prop = member.getProperty('email')
            if recipient_prop != None and len(recipient_prop) > 0:
                recipients_mail.add(recipient_prop)

        message = "\n%s" % interpolator(self.element.message)
        subject = interpolator(self.element.subject)

        for recipient in recipients_mail:
            mailhost.secureSend(message.encode(email_charset), recipient, source,
                                subject=subject, subtype='plain',
                                charset=email_charset, debug=False)
        return True


class MailRoleAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IMailRoleAction)
    label = _plone(u"Add Mail Action")
    description = _(u'form_description',
        default=u"A mail action that can mail plone users who have "
                u"a role on the object")
    form_name = _plone(u"Configure element")

    def create(self, data):
        a = MailRoleAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class MailRoleEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IMailRoleAction)
    label = _plone(u"Edit Mail Role Action")
    description = _plone(u"A mail action that can mail plone users who have "
                         u"a role on the object")
    form_name = _plone(u"Configure element")
