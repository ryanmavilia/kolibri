<template>

  <CoreBase
    :immersivePage="false"
    :appBarTitle="coachStrings.$tr('coachLabel')"
    :authorized="userIsAuthorized"
    authorizedRole="adminOrCoach"
    :showSubNav="true"
  >

    <TopNavbar slot="sub-nav" />

    <div class="new-coach-block">
      <p>
        <BackLink
          :to="classRoute('ReportsGroupLearnerReportPage', {})"
          text="Julie"
        />
      </p>
      <h1>
        {{ coachStrings.$tr('combinedLabel', {firstItem: 'Julie', secondItem: 'Some lesson'}) }}
      </h1>
      <HeaderTable>
        <HeaderTableRow>
          <template slot="key">{{ coachStrings.$tr('statusLabel') }}</template>
          <template slot="value"><LessonActive :active="true" /></template>
        </HeaderTableRow>
        <HeaderTableRow>
          <template slot="key">{{ coachStrings.$tr('recipientsLabel') }}</template>
          <template slot="value">Group 1, Group 2</template>
        </HeaderTableRow>
        <HeaderTableRow>
          <template slot="key">{{ coachStrings.$tr('descriptionLabel') }}</template>
          <template slot="value">Ipsum lorem</template>
        </HeaderTableRow>
      </HeaderTable>

      <h2>{{ coachStrings.$tr('numberOfResources', {value: 4}) }}</h2>
      <table class="new-coach-table">
        <thead>
          <tr>
            <td>{{ coachStrings.$tr('titleLabel') }}</td>
            <td>{{ coachStrings.$tr('progressLabel') }}</td>
            <td>{{ coachStrings.$tr('timeSpentLabel') }}</td>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <KRouterLink
                text="Some exercise"
                :to="classRoute(
                  'ReportsGroupLearnerReportLessonExercisePage',
                  { exerciseId: '___' }
                )"
              />
            </td>
            <td>
              <LearnerProgressLabel
                :verbosity="1"
                :count="1"
                verb="needHelp"
                icon="help"
              />
            </td>
            <td><TimeDuration :seconds="360" /></td>
          </tr>
          <tr>
            <td>
              Some video
            </td>
            <td>
              <LearnerProgressLabel
                :verbosity="1"
                :count="1"
                verb="completed"
                icon="star"
              />
            </td>
            <td><TimeDuration :seconds="120" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </CoreBase>

</template>


<script>

  import commonCoach from '../common';

  export default {
    name: 'ReportsGroupLearnerReportLessonPage',
    components: {},
    mixins: [commonCoach],
    $trs: {
      lessonProgressLabel: "'{lesson}' progress",
    },
  };

</script>


<style lang="scss" scoped></style>
