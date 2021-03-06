import datetime

from rest_framework import pagination
from rest_framework import permissions
from rest_framework import viewsets

from .serializers import LearnerNotificationSerializer
from .serializers import LessonReportSerializer
from kolibri.core.auth.constants import collection_kinds
from kolibri.core.auth.constants import role_kinds
from kolibri.core.auth.models import Collection
from kolibri.core.auth.models import FacilityUser
from kolibri.core.decorators import query_params_required
from kolibri.core.lessons.models import Lesson
from kolibri.core.notifications.models import LearnerProgressNotification
from kolibri.core.notifications.models import NotificationsLog

collection_kind_choices = tuple([choice[0] for choice in collection_kinds.choices] + ['user'])


class OptionalPageNumberPagination(pagination.PageNumberPagination):
    """
    Pagination class that allows for page number-style pagination, when requested.
    To activate, the `page_size` argument must be set. For example, to request the first 20 records:
    `?page_size=20&page=1`
    """
    page_size = None
    page_size_query_param = "page_size"


class KolibriReportPermissions(permissions.BasePermission):

    # check if requesting user has permission for collection or user
    def has_permission(self, request, view):
        if isinstance(view, LessonReportViewset):
            report_pk = view.kwargs.get('pk', None)
            if report_pk is None:
                # If requesting list view, check if requester has coach/admin permissions on whole facility
                collection_kind = 'facility'
                collection_or_user_pk = request.user.facility_id
            else:
                # If requesting detail view, only check if requester has permissions on the Classroom
                collection_kind = 'classroom'
                collection_or_user_pk = Lesson.objects.get(pk=report_pk).collection.id

        else:
            if isinstance(view, ClassroomNotificationsViewset):
                collection_kind = 'classroom'
            else:
                collection_kind = view.kwargs.get('collection_kind', 'user')
            collection_or_user_pk = view.kwargs.get('collection_id', view.kwargs.get('pk'))

        allowed_roles = [role_kinds.ADMIN, role_kinds.COACH]
        try:
            if 'user' == collection_kind:
                return request.user.has_role_for(allowed_roles, FacilityUser.objects.get(pk=collection_or_user_pk))
            else:
                return request.user.has_role_for(allowed_roles, Collection.objects.get(pk=collection_or_user_pk))
        except (FacilityUser.DoesNotExist, Collection.DoesNotExist, ValueError):
            return False


class LessonReportViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated, KolibriReportPermissions,)
    serializer_class = LessonReportSerializer
    queryset = Lesson.objects.all()


@query_params_required(collection_id=str)
class ClassroomNotificationsViewset(viewsets.ReadOnlyModelViewSet):

    permission_classes = (KolibriReportPermissions,)
    serializer_class = LearnerNotificationSerializer
    pagination_class = OptionalPageNumberPagination
    pagination_class.page_size = 10

    def check_after(self):
        """
        Check if after parameter must be used for the query
        """
        notifications_after = self.request.query_params.get('after', None)
        after = None
        if notifications_after:
            try:
                after = int(notifications_after)
            except ValueError:
                pass  # if after has not a valid format, let's not use it
        return after

    def apply_learner_filter(self, query):
        """
        Filter the notifications by learner_id if applicable
        """
        learner_id = self.request.query_params.get('learner_id', None)
        if learner_id:
            return query.filter(user_id=learner_id)
        return query

    def get_queryset(self):
        """
        Returns the notifications in reverse-chronological order, filtered by the query parameters.
        By default it sends only notifications from the past day.
        If a 'page_size' parameter is used, that sets a maximum number of results.
        If a 'page' parameter is used, the past day limit is not applied.

        Some url examples:
        /coach/api/notifications/?collection_id=9da65157a8603788fd3db890d2035a9f
        /coach/api/notifications/?collection_id=9da65157a8603788fd3db890d2035a9f&after=8&page=2
        /coach/api/notifications/?page_size=5&page=2&collection_id=9da65157a8603788fd3db890d2035a9f&learner_id=94117bb5868a1ef529b8be60f17ff41a
        /coach/api/notifications/?collection_id=9da65157a8603788fd3db890d2035a9f&page=2

        :param: collection_id uuid: classroom or learner group identifier (mandatory)
        :param: learner_id uuid: user identifier
        :param: after integer: all the notifications after this id will be sent.
        :param: page_size integer: sets the number of notifications to provide for pagination (defaults: 10)
        :param: page integer: sets the page to provide when paginating.
        """
        classroom_id = self.kwargs['collection_id']

        if classroom_id:
            try:
                Collection.objects.get(pk=classroom_id)
            except (Collection.DoesNotExist, ValueError):
                return []

        notifications_query = LearnerProgressNotification.objects.filter(classroom_id=classroom_id)
        notifications_query = self.apply_learner_filter(notifications_query)
        after = self.check_after()

        if after:
            notifications_query = notifications_query.filter(id__gt=after)
        elif self.request.query_params.get('page', None) is None:
            today = datetime.datetime.combine(datetime.datetime.now(), datetime.time(0))
            notifications_query = notifications_query.filter(timestamp__gte=today)

        return notifications_query.order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        It provides the list of ClassroomNotificationsViewset from DRF.
        Then it fetches and saves the needed information to know how many coaches
        are requesting notificatios in the last five minutes
        """
        response = super(viewsets.ReadOnlyModelViewSet, self).list(request, *args, **kwargs)

        # L
        logging_interval = datetime.datetime.now() - datetime.timedelta(minutes=5)
        logged_notifications = (
            NotificationsLog.objects.filter(timestamp__gte=logging_interval).values('coach_id').distinct().count()
        )
        # if there are more than 10 notifications we limit the answer to 10
        if logged_notifications < 10:
            notification_info = NotificationsLog()
            notification_info.coach_id = request.user.id
            notification_info.save()
            NotificationsLog.objects.filter(timestamp__lt=logging_interval).delete()

        response.data['coaches_polling'] = logged_notifications
        return response
