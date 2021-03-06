Feature: Super admin edits users
    Super admin needs to be able to edit user's full name and username, reset the passwords, change the user types, and delete them from the facility

  Background:
    Given I am signed in to Kolibri as a super admin
      And I am on the *Facility > Users* page

  Scenario: Edit user's full name
    When I click on *Options* button for the user I want to edit
      And I select *Edit details* option
    Then I see *Edit user details* modal
    When I click or tab into *Full name* field
      And I edit the full name as needed
      And I click the *Save* button
    Then the modal closes
      And I see the user with edited full name

  Scenario: Edit user's username
    When I click on *Options* button for the user I want to edit
      And I select *Edit details* option
    Then I see *Edit user details* modal
    When I click or tab into *Username* field
      And I edit the username as needed
      And I click the *Save* button
    Then the modal closes
      And I see the user with edited username

  Scenario: Change user type
    When I click on *Options* button for the user I want to edit
      And I select *Edit details* option
    Then I see *Edit user details* modal
    When I click or tab into *User type*
    Then the dropdown opens
    When I select the new role
      And I click the *Save* button
    Then the modal closes
      And I see the user with edited type (label or no label depending on the change)

  Scenario: Change class coach user to facility coach user
    Given there is class coach <username> in the facility
    When I click on *Options* button for the user <username>
      And I select *Edit details* option
    Then I see *Edit user details* modal
      And I see the *Class coach* radio button active under the *User type*
    When I click and make the *Facility coach* radio button active
      And I click the *Save* button
    Then the modal closes
      And I see the user <username> with the *Facility coach* label

  Scenario: Reset user's password
    When I click on *Options* button of the user I want to reset password for
      And I select *Reset password* option
    Then I see *Reset user password* modal
    When I click or tab into *New password* field
      And I enter the new password
      And I click or tab into *Confirm new password* field
      And I re-enter the new password
      And I click the *Save* button
    Then the modal closes
      And I see the *Facility > Users* page again # no confirmation that the password has been reset

  Scenario: Super admin can see the label *Super admin* next to their full name, not their facility role
      When I see my name in the user list
      Then I see a label *Super admin* next to my full name

  Scenario: Super admin cannot delete themselves
      When I see my name in the user list
        And I click on the *Options* dropdown button
      Then I see that the *Delete* option is disabled

  Scenario: Super admin cannot change their own user type from the *Edit user details* modal
    When I click on *Options* button for my own <username>
      And I select *Edit details* option
    Then I see *Edit user details* modal
    When I look at the field for *User type*
    Then I see that I am a Super admin
      And I see I cannot change my user type
      And I see the *View details in Device permissions* link
    When I click on the link *View details in Device permissions*
      Then I am redirected to my permissions page in *Device > Permissions*

  Scenario: Super admin cannot change the user type of other super admin users in the *Edit user details* modal
    When I click on *Options* button for another super admin
      And I select *Edit details* option
    Then I see *Edit user details* modal
    When I look at the field for *User type*
    Then I see the *Super admin* label
      And I see I cannot change the user type
      And I see the *Go to Device permissions to change this* link
    When I click on the link *Go to Device permissions to change this*
    Then I am redirected to their permissions page in *Device > Permissions*
