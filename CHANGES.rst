Changes
=======

1.7 (unreleased)
----------------

- add borg_local roles
  [maartenkling]

1.6 (2013-02-14)
----------------

- Updated message and title to stringinterpolation,
  like in plone.app.contentrules [kingel]


1.5 (2012-10-18)
----------------

- Moved to
  https://github.com/collective/collective.contentrules.mailtorole
  [maurits]


1.4 (2012-01-23)
----------------

- Fix Plone3 compatibility [toutpt]
- Add french translation [toutpt]


1.3 (2011-12-23)
----------------

- Check if member exists before getting mailaddress [gborelli]


1.3a1 (2011-10-28)
------------------

- Add checkbox for including members with global roles in mail (fixes
  http://plone.org/products/collective-contentrules-mailtolocalrole/issues/4)
  [khink]
- Rename to `collective.contentrules.mailtorole`

.. Note::
   Prior to version 1.3, the product was called
   `collective.contentrules.mailtolocalrole`.
   That product's history is included below for completeness.

1.2 (2011-10-28)
----------------

- use z3c.autoinclude plugin
- Plone 4.1 compatibility (fixes
  http://plone.org/products/collective-contentrules-mailtolocalrole/issues/5)
  [khink]


1.1 (2011-01-07)
----------------

- Fix the email from header that is generated from the portal owner if no from
  address is specified. Backported from plone.app.contentrules 4.0.2
  [fredvd]

- Add subgroups support. If a group contains a subgroup that has members,
  these members will also be checked for having the local role.
  [lzdych]


1.0 (2010-12-04)
----------------

- Fixed error when used on Plone 4: passing 'From' to secureSend is
  not needed in Plone 3 and breaks in Plone 4.
  [maurits]


0.7 (2008-12-05 Sinterklaas)
----------------------------

- Added Italian localization [paulox]

- Added Owner to role's vocabulary [paulox]

- Add check for empty user email address [fredvd]

- If the localrole is added to a group, add all members of that group to
  the recipients list [Craig Swank]


0.6 (2008-10-02)
----------------

- Fixed and added tests [fredvd]

- Updated locales [fredvd]


0.5 unreleased
--------------

- Add locales [fredvd]

- Fix acquired roles checking & look up email addresses [fredvd]

- Add checking for acquired roles [fredvd]

- Import basic version from a client project [fredvd]
