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

      <ReportsGroupReportLessonExerciseHeader />

      <table class="new-coach-table">
        <thead>
          <tr>
            <td>{{ coachStrings.$tr('questionLabel') }}</td>
            <td>{{ coachStrings.$tr('helpNeededLabel') }}</td>
            <td>{{ coachStrings.$tr('avgTimeSpentLabel') }}</td>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><KRouterLink text="Question 1" :to="questionLink" /></td>
            <td>
              <LearnerProgressCount
                :count="3"
                :verbosity="1"
                verb="needHelp"
                icon="help"
            /></td>
            <td><TimeDuration :seconds="60*15" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </CoreBase>

</template>


<script>

  import commonCoach from '../common';
  import ReportsGroupReportLessonExerciseHeader from './ReportsGroupReportLessonExerciseHeader';

  export default {
    name: 'ReportsGroupReportLessonExerciseQuestionListPage',
    components: {
      ReportsGroupReportLessonExerciseHeader,
    },
    mixins: [commonCoach],
    data() {
      return {
        lessonName: 'Lesson A',
      };
    },
    computed: {
      questionLink() {
        return this.classRoute('ReportsGroupReportLessonExerciseQuestionPage', {});
      },
    },
    methods: {
      goTo(page) {
        this.$router.push({ name: 'NEW_COACH_PAGES', params: { page } });
      },
    },
    $trs: {},
  };

</script>


<style lang="scss" scoped>

  .stats {
    margin-right: 16px;
  }

</style>
